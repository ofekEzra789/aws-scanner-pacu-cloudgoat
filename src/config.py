"""
Configuration for safe enumeration profiles and basic settings.

This file defines a few *named profiles* (basic/iam/network). Each profile is
just a list of Pacu module names to run sequentially.
"""

from dataclasses import dataclass, field


@dataclass
class ScanProfile:
    name: str
    description: str
    pacu_modules: list[str] = field(default_factory=list)


# enumeration-only profiles.
# Note: Module names may vary by Pacu version; tweak these to match your install.
PROFILES = {
    "basic": ScanProfile(
        name="basic",
        description="Core account info, IAM, and S3 enumeration.",
        pacu_modules=[
            "enum__aws_region_services",
            "iam__enum_users_roles_policies",
            "s3__enum_buckets",
        ],
    ),
    "iam": ScanProfile(
        name="iam",
        description="IAM-focused enumeration.",
        pacu_modules=[
            "iam__enum_users_roles_policies",
            "iam__enum_permissions",
        ],
    ),
    "network": ScanProfile(
        name="network",
        description="EC2, security groups, and VPC enumeration.",
        pacu_modules=[
            "ec2__enum_instances",
            "vpc__enum",
            "ec2__enum_security_groups",
        ],
    ),
}


DEFAULT_PROFILE_NAME = "basic"

# Directories / paths
DEFAULT_REPORTS_DIR = "reports"

# Timeouts (seconds) for each module run
DEFAULT_MODULE_TIMEOUT = 600  # 10 minutes

