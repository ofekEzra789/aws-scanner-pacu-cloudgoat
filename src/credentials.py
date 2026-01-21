"""
Credential handling for Pacu:
- accept AWS creds from the CLI
- prepare environment variables that Pacu (and AWS SDKs) will use
"""

import os
import uuid
from dataclasses import dataclass
from typing import Optional


@dataclass
class AwsCredentials:
    access_key: str
    secret_key: str
    region: str
    session_token: Optional[str] = None


def validate_credentials(creds: AwsCredentials) -> None:
    """
    Lightweight sanity checks to catch obvious mistakes early.
    """
    if not creds.access_key or not creds.secret_key:
        raise ValueError("AWS access key and secret key are required.")
    if len(creds.access_key) < 10:
        raise ValueError("AWS access key looks too short.")
    if len(creds.secret_key) < 20:
        raise ValueError("AWS secret key looks too short.")
    if not creds.region:
        raise ValueError("AWS region is required (e.g., us-east-1).")


def prepare_pacu_environment(creds: AwsCredentials) -> dict:
    """
    Return a copy of os.environ with AWS_* variables set.

    We keep it in-memory (no writing credentials to disk).
    """
    validate_credentials(creds)

    env = dict(os.environ)
    env["AWS_ACCESS_KEY_ID"] = creds.access_key
    env["AWS_SECRET_ACCESS_KEY"] = creds.secret_key
    env["AWS_DEFAULT_REGION"] = creds.region

    if creds.session_token:
        env["AWS_SESSION_TOKEN"] = creds.session_token

    return env


def generate_session_name(prefix: str = "pacu-enum") -> str:
    """
    Generate a short unique session name for Pacu runs.
    """
    suffix = uuid.uuid4().hex[:8]
    return f"{prefix}-{suffix}"

