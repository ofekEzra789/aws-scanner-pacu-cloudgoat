# Available Pacu modules and their region requirements
AVAILABLE_MODULES = {
    'lambda__enum': True,      # needs regions
    'ec2__enum': True,         # needs regions
    'route53__enum': True,     # needs regions
    'iam__enum_users_roles_policies_groups': False,  # doesn't need regions
}

# Default modules to run if none specified
DEFAULT_MODULES = ['lambda__enum', 'ec2__enum']

# Ollama API configuration
OLLAMA_API_URL = "http://localhost:11434/api/chat"
DEFAULT_MODEL = "qwen2.5:14b"

# Default AWS region
DEFAULT_REGION = "us-east-1"
