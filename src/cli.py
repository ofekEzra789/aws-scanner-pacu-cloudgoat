"""
Main CLI entry point for the AWS Pacu Enumeration Console.
"""

import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "AWS Pacu Enumeration Console - run safe, read-only "
            "enumeration modules against an AWS account."
        )
    )

    parser.add_argument("--access-key", required=True, help="AWS access key ID.")
    parser.add_argument("--secret-key", required=True, help="AWS secret access key.")
    parser.add_argument("--region", required=True, help="AWS region (e.g., us-east-1).")

    parser.add_argument(
        "--session-token",
        help="Optional AWS session token (for temporary credentials).",
    )
    parser.add_argument(
        "--profile",
        help="Enumeration profile to run (safe, read-only module sets).",
    )
    parser.add_argument(
        "--session-name",
        help="Optional Pacu session name. If omitted, one is generated.",
    )

    return parser.parse_args()


def main(argv=None):
    args = parse_args(argv)

    print("[*] Starting AWS Pacu Enumeration Console (read-only).")

    # creds = AwsCredentials(
    #     access_key=args.access_key,
    #     secret_key=args.secret_key,
    #     region=args.region,
    #     session_token=args.session_token,
    #     session_name=args.session_name
    # )

    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

