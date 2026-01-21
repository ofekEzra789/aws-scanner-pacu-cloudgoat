"""
Pacu enumeration runner: runs a curated list of safe enumeration modules.
"""

import subprocess
from dataclasses import dataclass
from typing import Optional

from .config import DEFAULT_MODULE_TIMEOUT


@dataclass
class ModuleResult:
    module_name: str
    return_code: int
    stdout: str
    stderr: str
    error: Optional[str] = None


def run_module(
    session_name: str,
    module_name: str,
    env: dict,
    timeout: int = DEFAULT_MODULE_TIMEOUT,
) -> ModuleResult:
    """
    Run a single Pacu module using the Pacu CLI.

    Assumes a `pacu` command exists on PATH and supports:
      pacu --session <name> --run-module <module_name>

    If your Pacu uses different flags, adjust `cmd` below.
    """
    cmd = ["pacu", "--session", session_name, "--run-module", module_name]

    try:
        proc = subprocess.run(
            cmd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
        )
        return ModuleResult(
            module_name=module_name,
            return_code=proc.returncode,
            stdout=proc.stdout,
            stderr=proc.stderr,
            error=None if proc.returncode == 0 else "non-zero exit code",
        )
    except subprocess.TimeoutExpired as e:
        return ModuleResult(
            module_name=module_name,
            return_code=-1,
            stdout=e.stdout or "",
            stderr=e.stderr or "",
            error=f"timeout after {timeout} seconds",
        )
    except FileNotFoundError:
        return ModuleResult(
            module_name=module_name,
            return_code=-1,
            stdout="",
            stderr="",
            error="pacu command not found on PATH. Is Pacu installed?",
        )
    except Exception as e:
        return ModuleResult(
            module_name=module_name,
            return_code=-1,
            stdout="",
            stderr=str(e),
            error="unexpected error running module",
        )


def run_enumeration_profile(
    session_name: str,
    modules: list[str],
    env: dict,
    timeout_per_module: int = DEFAULT_MODULE_TIMEOUT,
) -> list[ModuleResult]:
    """
    Run all enumeration modules sequentially.
    """
    results: list[ModuleResult] = []

    for module_name in modules:
        print(f"[+] Running Pacu module: {module_name} ...")
        res = run_module(
            session_name=session_name,
            module_name=module_name,
            env=env,
            timeout=timeout_per_module,
        )
        if res.error:
            print(f"[!] Module {module_name} finished with error: {res.error}")
        else:
            print(f"[+] Module {module_name} completed successfully.")
        results.append(res)

    return results

