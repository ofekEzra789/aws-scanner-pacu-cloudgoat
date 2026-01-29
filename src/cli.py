import argparse
import subprocess

# Available modules and their region requirements
AVAILABLE_MODULES = {
    'lambda__enum': True,      # needs regions
    'ec2__enum': True,         # needs regions
    'route53__enum': True,     # needs regions
    'iam__enum_users_roles_policies_groups': False,  # doesn't need regions
}

# Get aws creds from the command-line
def parse_args():
    parser = argparse.ArgumentParser(
        description="Aws Pacu enumeration console"
    )

    parser.add_argument("--access-key", help="AWS access key ID (required for new session)")
    parser.add_argument("--secret-key", help="AWS secret key (required for new session)")
    parser.add_argument("--session-name", required=True, help="Session name for pacu")
    parser.add_argument("--region", default="us-east-1", help="AWS region")
    parser.add_argument("--create-new", action="store_true", help="If you create new session add this argument, if you want to reuse the same session - dont provide it")
    parser.add_argument("--modules", nargs='+',
                       help=f"Specific modules to run (space-separated). Available: {', '.join(AVAILABLE_MODULES.keys())}. If not specified, runs lambda__enum and ec2__enum by default.")
    parser.add_argument("--query-data", choices=['ec2', 'lambda', 'iam', 'route53', 'all'],
                       help="Query enumerated data from Pacu database without running modules. Options: ec2, lambda, iam, route53, all")

    return parser.parse_args()


# Create subprocess and send to pacu
def pacu_subprocess(args):

    # Determine which modules to run
    if args.modules:
        # Validate user-specified modules
        invalid_modules = [m for m in args.modules if m not in AVAILABLE_MODULES]
        if invalid_modules:
            print(f"Error: Invalid modules: {', '.join(invalid_modules)}")
            print(f"Available modules: {', '.join(AVAILABLE_MODULES.keys())}")
            return 1

        modules_to_run = {m: AVAILABLE_MODULES[m] for m in args.modules}
    else:
        # Default modules to run if none specified
        default_modules = ['lambda__enum', 'ec2__enum']
        modules_to_run = {m: AVAILABLE_MODULES[m] for m in default_modules}

    if args.create_new:
        if not args.access_key or not args.secret_key:
            print("Error: --access-key and --secret-key are required when using --create-new")
            return 1

        create_cmd = ['pacu',
                     '--new-session', args.session_name,
                     '--set-keys', f'None,{args.access_key},{args.secret_key}']

        result = subprocess.run(create_cmd, capture_output=True, text=True)
        print("Session created:", result.stdout.strip())
        print()

    for module, needs_region in modules_to_run.items():
        print(f"\n{'='*70}")
        print(f"Running module: {module}")
        print(f"{'='*70}\n")

        cmd = ['pacu',
               '--session', args.session_name,
               '--module-name', module,
               '--exec']

        if needs_region:
            cmd.extend(['--module-args', f'--regions {args.region}'])

        print(f"Command: {' '.join(cmd)}\n")

        result = subprocess.run(cmd, capture_output=True, text=True)

        print("STDOUT:", result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        print(f"\n{module} completed with return code: {result.returncode}")
    
    return 0


# Query data from Pacu database
def query_pacu_data(args):
    print(f"\n{'='*70}")
    print(f"Querying Pacu data for session: {args.session_name}")
    print(f"Service: {args.query_data}")
    print(f"{'='*70}\n")

    cmd = ['pacu', '--session', args.session_name, '--data', args.query_data]

    print(f"Command: {' '.join(cmd)}\n")

    result = subprocess.run(cmd, capture_output=True, text=True)

    print("STDOUT:", result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)

    print(f"\nQuery completed with return code: {result.returncode}")

    return 0


def main():
    args = parse_args()

    # If query-data is specified, query the database instead of running enumeration
    if args.query_data:
        return query_pacu_data(args)
    else:
        return pacu_subprocess(args)


if __name__== "__main__":
    raise SystemExit(main())