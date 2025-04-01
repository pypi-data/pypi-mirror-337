import ipaddress
import json

from Kathara.exceptions import MachineNotRunningError
from Kathara.model.Lab import Lab

from ..foundation.checks.AbstractCheck import AbstractCheck
from ..foundation.model.CheckResult import CheckResult
from ..model.FailedCheck import FailedCheck
from ..model.SuccessfulCheck import SuccessfulCheck
from ..utils import key_exists


class InterfaceIPCheck(AbstractCheck):

    def __init__(self, lab: Lab, description: str = None):
        super().__init__(lab, description=description, priority=50)

    def check(self, device_name: str, interface_number: int, ip: str, dumped_iface: dict) -> CheckResult:
        interface_name = f"eth{interface_number}" if interface_number.isnumeric() else interface_number
        self.description = f"Verifying the IP address ({ip}) assigned to {interface_name} of {device_name}"

        try:
            iface_info = next(filter(lambda x: x["ifname"] == f"{interface_name}", dumped_iface))
        except StopIteration:
            return FailedCheck(self.description, f"Interface `{interface_name}` not found on `{device_name}`")

        ip_address = ipaddress.ip_interface(ip)

        prefix_len = int(ip_address.with_prefixlen.split("/")[1])

        assigned_ips = []
        if iface_info and "addr_info" in iface_info:
            for addr_info in iface_info["addr_info"]:
                assigned_ips.append(f"{addr_info['local']}/{addr_info['prefixlen']}")
                if addr_info["local"] == str(ip_address.ip):
                    if addr_info["prefixlen"] == prefix_len:
                        return SuccessfulCheck(self.description)
                    else:
                        reason = f"The IP address has a wrong netmask ({addr_info['prefixlen']})"
                        return FailedCheck(self.description, reason)

        reason = (
            f"The interface `{iface_info['ifname']}` of `{device_name}` "
            f"has the following IP addresses: {assigned_ips}`."
        )
        return FailedCheck(self.description, reason)

    def run(self, ip_mapping: dict) -> list[CheckResult]:
        results = []
        for device_name, iface_to_ips in ip_mapping.items():
            self.logger.info(f"Checking IPs for `{device_name}`...")
            try:
                dumped_iface = self.get_interfaces_addresses(device_name)
                for interface_number, ip in iface_to_ips.items():
                    check_result = self.check(device_name, interface_number, ip, dumped_iface)
                    results.append(check_result)
            except MachineNotRunningError:
                self.logger.warning(f"`{device_name}` is not running. Skipping checks...")
        return results

    def get_interfaces_addresses(self, device_name: str) -> dict:

        stdout, _, _ = self.kathara_manager.exec(
            machine_name=device_name, command=f"ip -j address", lab_hash=self.lab.hash, stream=False
        )

        return json.loads(stdout)

    def run_from_configuration(self, configuration: dict) -> list[CheckResult]:
        results = []
        if key_exists(["test", "ip_mapping"], configuration):
            self.logger.info("Verifying the IP addresses assigned to devices...")
            results.extend(self.run(configuration["test"]["ip_mapping"]))
        return results
