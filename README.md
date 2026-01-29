## AWS Pacu Enumeration Console

A Python CLI wrapper for [Pacu](https://github.com/RhinoSecurityLabs/pacu) that streamlines AWS security enumeration by running **enumeration-only modules** (no exploitation) and provides easy data querying capabilities.

### Features

- **Session Management**: Create and reuse Pacu sessions with AWS credentials
- **Module Selection**: Choose which enumeration modules to run
- **Data Querying**: Retrieve enumerated data from previous scans without re-running modules
- **Safety-First**: Designed for authorized enumeration only

### Available Modules

- `lambda__enum`: Enumerate Lambda functions (requires region)
- `ec2__enum`: Enumerate EC2 instances, security groups, VPCs (requires region)
- `route53__enum`: Enumerate Route53 DNS records (requires region)
- `iam__enum_users_roles_policies_groups`: Enumerate IAM resources (region-independent)

### Prerequisites

- Python 3.10+ (recommended)
- Pacu installed and available on your PATH as `pacu`
- AWS credentials you are authorized to test

### Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Usage

#### 1. Run Enumeration (Create New Session)

Run default modules (Lambda + EC2):
```bash
python -m src.cli \
  --session-name my-scan \
  --access-key YOUR_ACCESS_KEY \
  --secret-key YOUR_SECRET_KEY \
  --region us-east-1 \
  --create-new
```

Run specific modules:
```bash
python -m src.cli \
  --session-name my-scan \
  --access-key YOUR_ACCESS_KEY \
  --secret-key YOUR_SECRET_KEY \
  --region us-east-1 \
  --modules lambda__enum iam__enum_users_roles_policies_groups \
  --create-new
```

Run all available modules:
```bash
python -m src.cli \
  --session-name my-scan \
  --access-key YOUR_ACCESS_KEY \
  --secret-key YOUR_SECRET_KEY \
  --region us-east-1 \
  --modules lambda__enum ec2__enum route53__enum iam__enum_users_roles_policies_groups \
  --create-new
```

#### 2. Reuse Existing Session

Run modules on an existing session (no credentials needed):
```bash
python -m src.cli \
  --session-name my-scan \
  --modules ec2__enum route53__enum
```

#### 3. Query Enumerated Data

Query all data from a previous scan:
```bash
python -m src.cli \
  --session-name my-scan \
  --query-data all
```

Query specific service data:
```bash
# Query Lambda data
python -m src.cli --session-name my-scan --query-data lambda

# Query EC2 data
python -m src.cli --session-name my-scan --query-data ec2

# Query IAM data
python -m src.cli --session-name my-scan --query-data iam

# Query Route53 data
python -m src.cli --session-name my-scan --query-data route53
```

### Command-Line Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--session-name` | Yes | Name for the Pacu session |
| `--access-key` | Conditional | AWS access key ID (required with `--create-new`) |
| `--secret-key` | Conditional | AWS secret access key (required with `--create-new`) |
| `--region` | No | AWS region (default: us-east-1) |
| `--create-new` | No | Create a new session with provided credentials |
| `--modules` | No | Specific modules to run (default: lambda__enum, ec2__enum) |
| `--query-data` | No | Query data without running modules (choices: ec2, lambda, iam, route53, all) |

### Workflow Example

1. **Initial enumeration scan:**
```bash
python -m src.cli \
  --session-name my-scan \
  --access-key AKIA... \
  --secret-key ... \
  --region us-east-1 \
  --create-new
```

2. **Query the enumerated data:**
```bash
python -m src.cli \
  --session-name my-scan \
  --query-data all
```

3. **Run additional modules on same session:**
```bash
python -m src.cli \
  --session-name my-scan \
  --modules route53__enum
```

### Safety & Authorization

**IMPORTANT**: This tool is designed for **authorized security assessments only**. Only use it on:
- Your own AWS accounts
- AWS accounts where you have explicit written permission to perform security testing
- Authorized training/testing environments

Do not add exploitation modules or use this tool against unauthorized targets.

### Data Storage

Pacu stores enumerated data in a local SQLite database. The data persists across sessions and can be queried at any time using the `--query-data` argument without re-running enumeration modules.

### Future Enhancements

- AI-powered report generation using LLM analysis of enumerated data
- Structured report outputs (Markdown, HTML, JSON)
- Additional enumeration modules as they become available in Pacu
