import argparse
import subprocess

# 1. Get aws creds from the command-line
def parse_args():
    parser = argparse.ArgumentParser(
        description="Aws Pacue enumeration console"
    )

    parser.add_argument("--access-key", help="AWS access key ID (required for new session)")
    parser.add_argument("--secret-key", help="AWS secret key (required for new session)")
    parser.add_argument("--session-name", required=True, help="Session name for pacu")
    parser.add_argument("--region", default="us-east-1", help="AWS region")
    parser.add_argument("--create-new", action="store_true", help="When you create new session add this argument, if you want to reuse the same session - dont provide it")

    return parser.parse_args()


# 2. Create subprocess and send to pacu
def pacu_subprocess(args):
    if args.create_new:
        if not args.access_key or not args.secret_key:
            print("Error: --access-key and --secret-key are required when using --create-new")
            return 1

        cmd = ['pacu',
               '--new-session', args.session_name,
               '--set-keys', f'None,{args.access_key},{args.secret_key}',
               '--module-name', 'lambda__enum',
               '--exec',
               '--module-args', f'--regions {args.region}']
    else:
        cmd = ['pacu',
               '--session', args.session_name,
               '--module-name', 'lambda__enum',
               '--exec',
               '--module-args', f'--regions {args.region}']
        
    
    print(f"Running command: {' '.join(cmd)}")
    


    result = subprocess.run(cmd, capture_output=True, text=True)

    print("STDOUT:", result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    return result.returncode


def main():
    args = parse_args()
    pacu_subprocess(args)

    return 0


if __name__== "__main__":
    raise SystemExit(main())