from typing import Awaitable

from pipask.checks import Checker
from pipask.checks.types import CheckResult, CheckResultType
from pipask.infra.pip import InstallationReportItem
from pipask.infra.pypi import ReleaseResponse


# See https://pypi.org/classifiers/


class LicenseChecker(Checker):
    @property
    def description(self) -> str:
        return "Checking package license"

    async def check(
        self, package: InstallationReportItem, release_info_future: Awaitable[ReleaseResponse | None]
    ) -> CheckResult:
        pkg = package.pinned_requirement
        resolved_release_info = await release_info_future
        if resolved_release_info is None:
            return CheckResult(pkg, result_type=CheckResultType.FAILURE, message="No release information available")
        license = next((c for c in resolved_release_info.info.classifiers if c.startswith("License :: ")), None)
        if license:
            license = license.split(" :: ")[-1]
        if not license:
            license = resolved_release_info.info.license
        if license:
            return CheckResult(pkg, result_type=CheckResultType.NEUTRAL, message=f"Package is licensed under {license}")

        return CheckResult(
            pkg,
            result_type=CheckResultType.WARNING,
            message="No license found in PyPI metadata - you may need to check manually",
        )
