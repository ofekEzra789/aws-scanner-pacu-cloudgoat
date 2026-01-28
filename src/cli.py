import argparse
import subprocess

# Get aws creds from the command-line
def parse_args():
    parser = argparse.ArgumentParser(
        description="Aws Pacue enumeration console"
    )

    parser.add_argument("--access-key", help="AWS access key ID (required for new session)")
    parser.add_argument("--secret-key", help="AWS secret key (required for new session)")
    parser.add_argument("--session-name", required=True, help="Session name for pacu")
    parser.add_argument("--region", default="us-east-1", help="AWS region")
    parser.add_argument("--create-new", action="store_true", help="If you create new session add this argument, if you want to reuse the same session - dont provide it")

    return parser.parse_args()


# Create subprocess and send to pacu
def pacu_subprocess(args):

    modules = {
        'lambda__enum': True,      # needs regions
        'ec2__enum': True,         # needs regions
        'route53__enum': False,     # needs regions
        'iam__enum_users_roles_policies_groups': False ,  # doesn't need regions
        # 'iam__enum_permissions': False --> Add later
    }

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

    for module, needs_region in modules.items():
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


def main():
    args = parse_args()
    pacu_subprocess(args)

    return 0


if __name__== "__main__":
    raise SystemExit(main())