import argparse
from .config import AVAILABLE_MODULES, DEFAULT_REGION, DEFAULT_MODEL
from .pacu import run_enumeration, query_data
from .report import generate_report


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="AWS Pacu enumeration console"
    )

    parser.add_argument("--access-key", help="AWS access key ID (required for new session)")
    parser.add_argument("--secret-key", help="AWS secret key (required for new session)")
    parser.add_argument("--session-name", required=True, help="Session name for pacu")
    parser.add_argument("--region", default=DEFAULT_REGION, help=f"AWS region (default: {DEFAULT_REGION})")
    parser.add_argument("--create-new", action="store_true",
                       help="Create new session (requires --access-key and --secret-key)")
    parser.add_argument("--modules", nargs='+',
                       help=f"Modules to run. Available: {', '.join(AVAILABLE_MODULES.keys())}")
    parser.add_argument("--query-data", choices=['ec2', 'lambda', 'iam', 'route53', 'all'],
                       help="Query enumerated data from Pacu database")
    parser.add_argument("--generate-report", action="store_true",
                       help="Generate AI security report (requires --query-data)")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                       help=f"Ollama model for report generation (default: {DEFAULT_MODEL})")
    parser.add_argument("--prompt", help="Custom prompt string (use {pacu_data} as placeholder)")
    parser.add_argument("--prompt-file", help="Path to file containing custom prompt")

    return parser.parse_args()


def load_custom_prompt(args):
    """Load custom prompt from file or argument."""
    if args.prompt_file:
        try:
            with open(args.prompt_file, 'r') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Error: Prompt file not found: {args.prompt_file}")
            return None
        except Exception as e:
            print(f"Error reading prompt file: {e}")
            return None
    elif args.prompt:
        return args.prompt
    return None


def main():
    args = parse_args()

    # Validate prompt args require --query-data
    if (args.prompt or args.prompt_file) and not args.query_data:
        print("Error: --prompt and --prompt-file require --query-data")
        return 1

    if args.query_data:
        # Query data from Pacu database
        return_code, data, _ = query_data(args.session_name, args.query_data)

        if args.generate_report or args.prompt or args.prompt_file:
            if return_code != 0:
                print("\nWarning: Pacu query failed. Skipping report generation.")
                return 1

            # Load custom prompt if provided
            custom_prompt = load_custom_prompt(args)
            if (args.prompt or args.prompt_file) and custom_prompt is None:
                return 1  # Error already printed

            # Warn if {pacu_data} placeholder is missing
            if custom_prompt and "{pacu_data}" not in custom_prompt:
                print("Warning: Custom prompt missing {pacu_data} placeholder.")
                print("The enumeration data will not be included in the prompt.")

            result = generate_report(data, args.session_name, args.model, custom_prompt)
            return 0 if result else 1

        return return_code
    else:
        # Run enumeration modules
        return run_enumeration(
            session_name=args.session_name,
            modules=args.modules,
            region=args.region,
            access_key=args.access_key,
            secret_key=args.secret_key,
            create_new=args.create_new
        )


if __name__ == "__main__":
    raise SystemExit(main())
