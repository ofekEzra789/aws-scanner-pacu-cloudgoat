## AWS Pacu Enumeration Console

A beginner-friendly Python CLI that accepts AWS account details, runs **only Pacu enumeration modules** (no exploitation), and outputs simple JSON summaries.

### What are “profiles”?

Profiles are just **pre-defined lists of Pacu modules** you can run by name:

- `basic`: general discovery (IAM + S3)
- `iam`: IAM-focused enumeration
- `network`: EC2/VPC/security-groups enumeration

Pick one with `--profile basic|iam|network`.

### Prerequisites

- Python 3.10+ (recommended)
- Pacu installed and available on your PATH as `pacu`
- AWS credentials you are allowed to test

### Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run

```bash
python -m src.cli \
  --access-key YOUR_ACCESS_KEY \
  --secret-key YOUR_SECRET_KEY \
  --region YOUR_REGION \
  --profile basic
```

Make sure you know which region you deployed cloudgoat

Reports are saved under `reports/` as JSON.

### Notes on safety

This project is intended for **enumeration only**. Do not add exploitation modules unless you fully understand the impact and have explicit permission.

### Testing with CloudGoat

Use CloudGoat to spin up a safe, permissioned AWS scenario for practice:

1. Deploy a CloudGoat scenario (follow CloudGoat docs).
2. Collect the AWS credentials (access key, secret key, region) provided for that scenario.
3. Run an enumeration profile against it, for example:

```bash
python -m src.cli \
  --access-key CLOUDGOAT_ACCESS_KEY \
  --secret-key CLOUDGOAT_SECRET_KEY \
  --region YOUR_REGION \
  --profile basic
```

4. Open the generated JSON report in `reports/` to inspect discovered IAM users/roles, S3 buckets, and other resources depending on the profile you chose.
