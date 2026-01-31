import os
import requests
from datetime import datetime
from .config import OLLAMA_API_URL, DEFAULT_MODEL


def call_ollama(prompt, model=DEFAULT_MODEL):
    """
    Send prompt to Ollama and get AI-generated response.

    Args:
        prompt: The prompt to send to the model
        model: Ollama model name

    Returns:
        Generated text response or None if error occurs
    """
    print(f"\n{'='*70}")
    print(f"Generating report using {model}...")
    print(f"{'='*70}\n")

    try:
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False
        }

        response = requests.post(OLLAMA_API_URL, json=payload, timeout=300)

        if response.status_code == 200:
            result = response.json()
            return result.get('message', {}).get('content', '')
        else:
            print(f"Error: Ollama API returned status code {response.status_code}")
            print(f"Response: {response.text}")
            return None

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Ollama. Make sure Ollama is running.")
        print("Start Ollama with: ollama serve")
        return None
    except requests.exceptions.Timeout:
        print("Error: Request to Ollama timed out. The model might be too large or the prompt too complex.")
        return None
    except Exception as e:
        print(f"Error calling Ollama: {str(e)}")
        return None


def generate_security_prompt(pacu_data):
    """
    Create a penetration testing focused analysis prompt with Pacu enumeration data.

    Args:
        pacu_data: Raw output from Pacu data query

    Returns:
        Formatted prompt string for security analysis
    """
    prompt = f"""You are an AWS penetration tester. Analyze this Pacu enumeration data and create an offensive security report.

**ENUMERATION DATA:**
{pacu_data}

**REPORT FORMAT (Markdown):**

# AWS Penetration Test Report

## Executive Summary
Brief overview of access level, attack surface, and critical findings.

## Privilege Escalation Paths
Identify IAM policies and permissions that enable privilege escalation (iam:PutUserPolicy, iam:AttachRolePolicy, AssumeRole chains, etc.).

## Attack Chains
Document exploitable attack paths with step-by-step techniques to achieve objectives (data access, lateral movement, persistence).

## High-Value Targets
- Publicly accessible resources (S3 buckets, snapshots, databases)
- Overprivileged roles and users
- Credential harvesting opportunities (EC2 metadata, Lambda env vars, Secrets Manager)
- Sensitive data exposure risks

## Lateral Movement
Service-to-service access paths, cross-account possibilities, network pivoting opportunities.

## Defensive Gaps
Missing security controls (CloudTrail, GuardDuty, encryption, network segmentation).

## Recommendations
Prioritized remediation steps with specific commands/policy changes.

**INSTRUCTIONS:**
- Focus on exploitability and attack paths, not just misconfigurations
- Reference actual resource names, ARNs, and specific configurations
- Provide technical exploitation details and commands
- Think like an attacker"""
    return prompt


def save_report(report_content, session_name):
    """
    Save security report to reports/ directory in project root.

    Args:
        report_content: The generated report content
        session_name: Pacu session name

    Returns:
        Path to saved report file
    """
    # Get project root directory (parent of src/)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    reports_dir = os.path.join(project_root, "reports")

    # Create reports directory if it doesn't exist
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{session_name}_{timestamp}.md"
    filepath = os.path.join(reports_dir, filename)

    # Write report to file
    with open(filepath, 'w') as f:
        f.write(report_content)

    return filepath


def generate_report(pacu_data, session_name, model=DEFAULT_MODEL, custom_prompt=None):
    """
    Generate and save security report from Pacu data.

    Args:
        pacu_data: Raw output from Pacu data query
        session_name: Pacu session name
        model: Ollama model to use
        custom_prompt: Optional custom prompt (use {pacu_data} as placeholder)

    Returns:
        Path to saved report file, or None if generation failed
    """
    if not pacu_data or len(pacu_data.strip()) == 0:
        print("Warning: No data provided. Skipping report generation.")
        return None

    # Use custom prompt or default
    if custom_prompt:
        prompt = custom_prompt.replace("{pacu_data}", pacu_data)
    else:
        prompt = generate_security_prompt(pacu_data)

    report = call_ollama(prompt, model)

    if report:
        filepath = save_report(report, session_name)
        print(f"\n{'='*70}")
        print("Report successfully generated!")
        print(f"Saved to: {filepath}")
        print(f"{'='*70}\n")
        return filepath
    else:
        print("\nError: Failed to generate report.")
        return None
