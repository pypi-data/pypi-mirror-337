import jc
from Kathara.model.Lab import Lab

from ..foundation.checks.AbstractCheck import AbstractCheck
from ..foundation.model.CheckResult import CheckResult
from ..model.FailedCheck import FailedCheck
from ..model.SuccessfulCheck import SuccessfulCheck
from ..utils import get_output, key_exists


class ReachabilityCheck(AbstractCheck):

    def __init__(self, lab: Lab, description: str = None):
        super().__init__(lab, description=description, priority=70)

    def check(self, device_name: str, destination: str) -> CheckResult:

        if destination.startswith("!"):
            destination = destination[1:]
            self.description = f"Verifying `{destination}` not reachable from device `{device_name}`"
            invert = True
        else:
            self.description = f"Verifying `{destination}` reachable from device `{device_name}`"
            invert = False

        try:
            exec_output_gen = self.kathara_manager.exec(
                machine_name=device_name,
                command=f"bash -c 'ping -q -n -c 1 {destination}'",
                lab_hash=self.lab.hash,
            )
        except Exception as e:
            return CheckResult(self.description, invert ^ False, str(e))

        output = get_output(exec_output_gen).replace("ERROR: ", "")

        try:
            parsed_output = jc.parse("ping", output, quiet=True)
            if int(parsed_output["packets_received"]) > 0:
                if invert:
                    return FailedCheck(self.description, f"`{device_name}` can reach `{destination}`.")
                else:
                    return SuccessfulCheck(self.description)
            else:
                if invert:
                    return SuccessfulCheck(self.description)
                else:
                    return FailedCheck(self.description,
                                       f"`{device_name}` does not receive any answer from `{destination}`.")
        except Exception:
            return CheckResult(self.description, invert ^ False, output.strip())

    def run(self, devices_to_destinations: dict[str, list[str]]) -> list[CheckResult]:
        results = []
        for device_name, destinations in devices_to_destinations.items():
            for destination in destinations:
                check_result = self.check(device_name, destination)
                results.append(check_result)
        return results

    def run_from_configuration(self, configuration: dict) -> list[CheckResult]:
        results = []
        if key_exists(["test", "reachability"], configuration):
            self.logger.info(f"Starting reachability test...")
            results.extend(self.run(configuration["test"]["reachability"]))
        return results
