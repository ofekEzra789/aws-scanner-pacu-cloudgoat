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

    return parser.parse_args()


def main():
    args = parse_args()

    if args.query_data:
        # Query data from Pacu database
        return_code, data, _ = query_data(args.session_name, args.query_data)

        if args.generate_report:
            if return_code != 0:
                print("\nWarning: Pacu query failed. Skipping report generation.")
                return 1

            result = generate_report(data, args.session_name, args.model)
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
