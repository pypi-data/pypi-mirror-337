import json

from Kathara.exceptions import MachineNotRunningError
from Kathara.model.Lab import Lab

from ....foundation.checks.AbstractCheck import AbstractCheck
from ....foundation.model.CheckResult import CheckResult
from ....model.FailedCheck import FailedCheck
from ....model.SuccessfulCheck import SuccessfulCheck
from ....utils import get_output, key_exists


class VTEPCheck(AbstractCheck):

    def __init__(self, lab: Lab, description: str = None):
        super().__init__(lab, description=description, priority=1040)

    def check(self, device_name: str, vni: str, vtep_ip: str) -> CheckResult:
        try:
            exec_output_gen = self.kathara_manager.exec(
                machine_name=device_name, command="ip -d -j link show type vxlan", lab_hash=self.lab.hash
            )
        except MachineNotRunningError as e:
            return FailedCheck(self.description, str(e))

        output = get_output(exec_output_gen)

        if output.startswith("ERROR:") or "exec failed" in output:
            return FailedCheck(self.description, output)
        output = json.loads(output)

        for route in output:
            if route["linkinfo"]["info_data"]["id"] == int(vni):
                if route["linkinfo"]["info_data"]["local"] == vtep_ip:
                    return SuccessfulCheck(self.description)
                else:
                    reason = (
                        f"VNI `{vni}` configured on device `{device_name}` with wrong "
                        f"VTEP IP {route['linkinfo']['info_data']['local']} (instead of {vtep_ip})"
                    )
                    return FailedCheck(self.description, reason)
        return FailedCheck(self.description, f"VNI `{vni}` not configured on device `{device_name}`")

    def run(self, device_to_vnis_info: dict[str, dict]) -> list[CheckResult]:
        results = []
        for device_name, vnis_info in device_to_vnis_info.items():
            self.logger.info(f"Checking {device_name} VTEP configuration...")
            vnis = vnis_info["vnis"]
            vtep_ip = vnis_info["ip"]
            for vni in vnis:
                self.description = f"Checking that `{device_name}` VTEP has vni `{vni}` with VTEP IP `{vtep_ip}`"
                check_result = self.check(device_name, vni, vtep_ip)
                results.append(check_result)
        return results

    def run_from_configuration(self, configuration: dict) -> list[CheckResult]:
        results = []
        if key_exists(["test", "protocols", "bgpd", "vtep_devices"], configuration):
            self.logger.info("Checking VTEP devices configuration...")
            results.extend(self.run(configuration["test"]["protocols"]['bgpd']['vtep_devices']))
        return results
