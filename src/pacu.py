import subprocess
from .config import AVAILABLE_MODULES, DEFAULT_MODULES


def validate_modules(modules):
    """
    Validate that all specified modules are available.

    Args:
        modules: List of module names to validate

    Returns:
        Tuple of (valid: bool, invalid_modules: list)
    """
    invalid = [m for m in modules if m not in AVAILABLE_MODULES]
    return len(invalid) == 0, invalid


def create_session(session_name, access_key, secret_key):
    """
    Create a new Pacu session with AWS credentials.

    Args:
        session_name: Name for the Pacu session
        access_key: AWS access key ID
        secret_key: AWS secret access key

    Returns:
        subprocess.CompletedProcess result
    """
    cmd = [
        'pacu',
        '--new-session', session_name,
        '--set-keys', f'None,{access_key},{secret_key}'
    ]
    return subprocess.run(cmd, capture_output=True, text=True)


def run_module(session_name, module, region=None):
    """
    Run a single Pacu module.

    Args:
        session_name: Pacu session name
        module: Module name to run
        region: AWS region (required for some modules)

    Returns:
        subprocess.CompletedProcess result
    """
    cmd = [
        'pacu',
        '--session', session_name,
        '--module-name', module,
        '--exec'
    ]

    needs_region = AVAILABLE_MODULES.get(module, False)
    if needs_region and region:
        cmd.extend(['--module-args', f'--regions {region}'])

    return subprocess.run(cmd, capture_output=True, text=True)


def run_enumeration(session_name, modules=None, region=None, access_key=None, secret_key=None, create_new=False):
    """
    Run Pacu enumeration modules.

    Args:
        session_name: Pacu session name
        modules: List of modules to run (defaults to DEFAULT_MODULES)
        region: AWS region
        access_key: AWS access key (required if create_new=True)
        secret_key: AWS secret key (required if create_new=True)
        create_new: Whether to create a new session

    Returns:
        0 on success, 1 on error
    """
    modules_to_run = modules or DEFAULT_MODULES

    # Validate modules
    valid, invalid = validate_modules(modules_to_run)
    if not valid:
        print(f"Error: Invalid modules: {', '.join(invalid)}")
        print(f"Available modules: {', '.join(AVAILABLE_MODULES.keys())}")
        return 1

    # Create new session if requested
    if create_new:
        if not access_key or not secret_key:
            print("Error: --access-key and --secret-key are required when using --create-new")
            return 1

        result = create_session(session_name, access_key, secret_key)
        print("Session created:", result.stdout.strip())
        print()

    # Run each module
    for module in modules_to_run:
        print(f"\n{'='*70}")
        print(f"Running module: {module}")
        print(f"{'='*70}\n")

        result = run_module(session_name, module, region)

        print("STDOUT:", result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)

        print(f"\n{module} completed with return code: {result.returncode}")

    return 0


def query_data(session_name, service):
    """
    Query enumerated data from Pacu database.

    Args:
        session_name: Pacu session name
        service: Service to query (ec2, lambda, iam, route53, all)

    Returns:
        Tuple of (return_code, stdout, stderr)
    """
    print(f"\n{'='*70}")
    print(f"Querying Pacu data for session: {session_name}")
    print(f"Service: {service}")
    print(f"{'='*70}\n")

    cmd = ['pacu', '--session', session_name, '--data', service]
    print(f"Command: {' '.join(cmd)}\n")

    result = subprocess.run(cmd, capture_output=True, text=True)

    print("STDOUT:", result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)

    print(f"\nQuery completed with return code: {result.returncode}")

    return result.returncode, result.stdout, result.stderr
