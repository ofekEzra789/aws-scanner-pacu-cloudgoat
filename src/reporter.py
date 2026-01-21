"""
Simple JSON report generation for Pacu enumeration runs.
"""

import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Optional

from .config import DEFAULT_REPORTS_DIR
from .pacu_runner import ModuleResult


@dataclass
class SummaryReport:
    timestamp_utc: str
    region: str
    profile_name: str
    session_name: str
    account_id: Optional[str]
    modules_run: list[str]
    module_results: list[ModuleResult]


def build_summary_report(
    region: str,
    profile_name: str,
    session_name: str,
    module_results: list[ModuleResult],
    account_id: Optional[str] = None,
) -> SummaryReport:
    """
    Create an in-memory summary report.

    account_id is optional for now; you can enrich it later.
    """
    timestamp = datetime.utcnow().isoformat(timespec="seconds") + "Z"
    modules_run = [m.module_name for m in module_results]

    return SummaryReport(
        timestamp_utc=timestamp,
        region=region,
        profile_name=profile_name,
        session_name=session_name,
        account_id=account_id,
        modules_run=modules_run,
        module_results=module_results,
    )


def save_report(report: SummaryReport, reports_dir: str = DEFAULT_REPORTS_DIR) -> str:
    """
    Save the summary report as JSON. Returns the saved file path.
    """
    os.makedirs(reports_dir, exist_ok=True)

    filename = (
        f"pacu-enum-{report.profile_name}-"
        f"{report.region}-"
        f"{report.timestamp_utc.replace(':', '').replace('-', '')}.json"
    )
    path = os.path.join(reports_dir, filename)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(asdict(report), f, indent=2)

    return path

