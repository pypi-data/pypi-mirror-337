import re

import jc
from Kathara.exceptions import MachineNotRunningError
from Kathara.model.Lab import Lab

from ....foundation.checks.AbstractCheck import AbstractCheck
from ....foundation.model.CheckResult import CheckResult
from ....model.FailedCheck import FailedCheck
from ....model.SuccessfulCheck import SuccessfulCheck
from ....utils import get_output, find_lines_with_string, find_device_name_from_ip, key_exists


class DNSAuthorityCheck(AbstractCheck):

    def __init__(self, lab: Lab, description: str = None):
        super().__init__(lab, description=description, priority=3010)

    def check(self, domain: str, authority_ip: str, device_name: str, device_ip: str) -> CheckResult:
        self.description = f"Checking on `{device_name}` that `{authority_ip}` is the authority for domain `{domain}`"

        try:
            exec_output_gen = self.kathara_manager.exec(
                machine_name=device_name, command=f"dig NS {domain} @{device_ip}", lab_hash=self.lab.hash
            )
        except MachineNotRunningError as e:
            return FailedCheck(self.description, str(e))

        output = get_output(exec_output_gen)
        if output.startswith("ERROR:"):
            return FailedCheck(self.description, output)

        result = jc.parse("dig", output)
        if result:
            result = result.pop()
            if result["status"] == "NOERROR" and "answer" in result:
                root_servers = list(map(lambda x: x["data"].split(" ")[0], result["answer"]))
                authority_ips = []
                for root_server in root_servers:
                    stdout, stderr, exit_code = self.kathara_manager.exec(
                        machine_name=device_name,
                        command=f"dig +short +time=5 +tries=1 {root_server} @{device_ip}",
                        lab_hash=self.lab.hash,
                        stream=False
                    )
                    ip = stdout.decode("utf-8").strip() if stdout else (
                        stderr.decode("utf-8").strip() if stderr else "")
                    if authority_ip == ip:
                        return SuccessfulCheck(self.description)
                    else:
                        authority_ips.append(ip)
                reason = f"The dns authorities for domain `{domain}` have the following IPs {authority_ips}"
                return FailedCheck(self.description, reason)
            else:
                reason = (
                    f"named on {device_name} is running but answered "
                    f"with {result['status']} when quering for {domain}"
                )
                return FailedCheck(self.description, reason)
        else:
            if self.lab.fs.exists(f"{device_name}.startup"):
                with self.lab.fs.open(f"{device_name}.startup", "r") as startup_file:
                    lines = startup_file.readlines()

                for line in lines:
                    line = line.strip()
                    if re.search(rf"^\s*systemctl\s*start\s*named\s*$", line):
                        stdout, stderr, exit_code = self.kathara_manager.exec(
                            machine_name=device_name,
                            command=f"timeout 2 named -d 5 -g",
                            lab_hash=self.lab.hash,
                            stream=False
                        )

                        output = stdout.decode("utf-8").strip() if stdout else (
                            stderr.decode("utf-8").strip() if stderr else "")

                        date_pattern = (
                            r"\d{2}-[Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec]{3}-\d{4} \d{2}:\d{2}:\d{2}\.\d{3}"
                        )

                        reason_list = find_lines_with_string(output, "could not")
                        reason_list.extend(find_lines_with_string(output, "/etc/bind/named.conf"))
                        reason_list_no_dates = [re.sub(date_pattern, "", line) for line in reason_list]
                        reason = "\n".join(reason_list_no_dates)

                        return FailedCheck(self.description, "Configuration Error:\n" + reason)

                reason = f"named not started in `{device_name}`.startup`"
                return FailedCheck(self.description, reason)
            else:
                reason = f"There is no `.startup` file for device `{device_name}`"
                return FailedCheck(self.description, reason)

    def run(
            self,
            zone_to_authoritative_ips: dict[str, list[str]],
            local_nameservers: list[str],
            ip_mapping: dict[str, dict[str, str]],
    ) -> list[CheckResult]:
        results = []
        for domain, name_servers in zone_to_authoritative_ips.items():
            self.logger.info(f"Checking authority ip for domain `{domain}`")
            for ns in name_servers:
                check_result = self.check(domain, ns, find_device_name_from_ip(ip_mapping, ns), ns)
                results.append(check_result)

                if domain == ".":
                    self.logger.info(
                        f"Checking if all the named servers can correctly resolve {ns} as the root nameserver..."
                    )
                    for generic_ns_ip in name_servers:
                        check_result = self.check(
                            domain, ns, find_device_name_from_ip(ip_mapping, generic_ns_ip), generic_ns_ip
                        )
                        results.append(check_result)

                    for local_ns in local_nameservers:
                        check_result = self.check(domain, ns, find_device_name_from_ip(ip_mapping, local_ns), local_ns)
                        results.append(check_result)
        return results

    def run_from_configuration(self, configuration: dict) -> list[CheckResult]:
        results = []
        if key_exists(["test", "applications", "dns", "authoritative"], configuration) and \
                key_exists(["test", "applications", "dns", "local_ns"], configuration) and \
                key_exists(["test", "ip_mapping"], configuration):
            self.logger.info("Checking DNS authorities...")
            results.extend(self.run(configuration["test"]["applications"]["dns"]["authoritative"],
                                    configuration["test"]["applications"]["dns"]["local_ns"].keys(),
                                    configuration["test"]["ip_mapping"]
                                    )
                           )
        return results
