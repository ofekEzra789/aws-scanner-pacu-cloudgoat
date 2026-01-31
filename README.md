## AWS Pacu Enumeration Console

A Python CLI wrapper for [Pacu](https://github.com/RhinoSecurityLabs/pacu) that streamlines AWS security enumeration with AI-powered report generation.

### Features

- **Session Management**: Create and reuse Pacu sessions
- **Module Selection**: Choose which enumeration modules to run
- **Data Querying**: Retrieve enumerated data without re-running modules
- **AI Reports**: Generate security reports using Ollama

### Available Modules

- `lambda__enum`: Lambda functions
- `ec2__enum`: EC2 instances, security groups, VPCs
- `route53__enum`: Route53 DNS records
- `iam__enum_users_roles_policies_groups`: IAM resources

### Prerequisites

- Python 3.10+
- [Pacu](https://github.com/RhinoSecurityLabs/pacu) installed
- [Ollama](https://ollama.ai) (for AI reports)

### Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# For AI reports
ollama pull qwen2.5:14b
ollama serve
```

### Usage

**Run enumeration:**
```bash
python -m src.cli \
  --session-name my-scan \
  --access-key YOUR_KEY \
  --secret-key YOUR_SECRET \
  --region us-east-1 \
  --create-new
```

**Query data:**
```bash
python -m src.cli --session-name my-scan --query-data all
```

**Generate AI report:**
```bash
python -m src.cli --session-name my-scan --query-data all --generate-report
```

**Custom prompt:**
```bash
python -m src.cli --session-name my-scan --query-data all \
  --prompt "Analyze for compliance: {pacu_data}"
```

### Command-Line Arguments

| Argument | Description |
|----------|-------------|
| `--session-name` | Name for the Pacu session (required) |
| `--access-key` | AWS access key ID |
| `--secret-key` | AWS secret access key |
| `--region` | AWS region (default: us-east-1) |
| `--create-new` | Create new session with credentials |
| `--modules` | Modules to run (default: lambda__enum, ec2__enum) |
| `--query-data` | Query data (ec2, lambda, iam, route53, all) |
| `--generate-report` | Generate AI security report |
| `--model` | Ollama model (default: qwen2.5:14b) |
| `--prompt` | Custom prompt (use `{pacu_data}` placeholder) |
| `--prompt-file` | Path to custom prompt file |

### Safety

**This tool is for authorized security assessments only.** Only use on accounts you own or have explicit permission to test.
