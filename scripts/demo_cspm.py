#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo CSPM Python script for testing run_cspm_file.sh functionality.

This script demonstrates the capabilities of the CSPM script runner by:
1. Printing Python and environment information
2. Checking for environment variables from .env file
3. Accepting command line arguments
4. Simulating a CSPM check with mock results
"""

import os
import sys
import json
import platform
from pathlib import Path


def main():
    """Main function to demonstrate CSPM script functionality."""

    print("=" * 60)
    print("CSPM DEMO SCRIPT - Testing run_cspm_file.sh")
    print("=" * 60)

    # 1. Print system and Python information
    print("\n[1] SYSTEM INFORMATION:")
    print(f"  Python version: {sys.version}")
    print(f"  Platform: {platform.platform()}")
    print(f"  Working directory: {os.getcwd()}")
    print(f"  Script path: {os.path.abspath(__file__)}")

    # 2. Check for virtual environment
    venv_path = os.environ.get('VIRTUAL_ENV', None)
    if venv_path:
        print(f"\n[2] VIRTUAL ENVIRONMENT:")
        print(f"  Activated: Yes")
        print(f"  Path: {venv_path}")
    else:
        print(f"\n[2] VIRTUAL ENVIRONMENT: Not activated (running in global Python)")

    # 3. Check for environment variables from .env file
    print("\n[3] ENVIRONMENT VARIABLES (from .env if loaded):")
    env_vars_to_check = [
        'OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'AZURE_SUBSCRIPTION_ID',
        'AWS_ACCESS_KEY_ID', 'GCP_PROJECT_ID', 'CSPM_TEST_VAR'
    ]

    env_found = False
    for var in env_vars_to_check:
        value = os.environ.get(var)
        if value:
            # Mask sensitive values
            masked_value = value[:4] + '***' + value[-4:] if len(value) > 8 else '***'
            print(f"  {var}: {masked_value}")
            env_found = True

    if not env_found:
        print("  No .env variables detected (or .env file not loaded)")

    # 4. Process command line arguments
    print(f"\n[4] COMMAND LINE ARGUMENTS:")
    print(f"  Script name: {sys.argv[0]}")
    print(f"  Argument count: {len(sys.argv) - 1}")

    if len(sys.argv) > 1:
        for i, arg in enumerate(sys.argv[1:], 1):
            print(f"  Argument {i}: {arg}")
    else:
        print("  No arguments provided")

    # 5. Simulate a CSPM security check
    print("\n[5] SIMULATED CSPM SECURITY CHECK:")

    mock_checks = [
        {
            "id": "cspm-001",
            "name": "Storage Account Public Access",
            "status": "PASS",
            "severity": "HIGH",
            "description": "Storage accounts should not allow public access",
            "resource": "/subscriptions/xxx/resourceGroups/rg/providers/Microsoft.Storage/storageAccounts/mystorage"
        },
        {
            "id": "cspm-002",
            "name": "SQL Database Encryption",
            "status": "FAIL",
            "severity": "MEDIUM",
            "description": "SQL databases should have transparent data encryption enabled",
            "resource": "/subscriptions/xxx/resourceGroups/rg/providers/Microsoft.Sql/servers/myserver/databases/mydb"
        },
        {
            "id": "cspm-003",
            "name": "Network Security Groups",
            "status": "PASS",
            "severity": "LOW",
            "description": "NSG rules should not allow all inbound traffic",
            "resource": "/subscriptions/xxx/resourceGroups/rg/providers/Microsoft.Network/networkSecurityGroups/nsg"
        }
    ]

    for check in mock_checks:
        status_icon = "[PASS]" if check["status"] == "PASS" else "[FAIL]"
        print(f"  {status_icon} {check['name']} ({check['severity']}): {check['status']}")

    # 6. Check for required Python packages (simulate dependency check)
    print("\n[6] DEPENDENCY CHECK:")

    packages_to_check = ['requests', 'azure-identity', 'boto3', 'google-cloud']
    installed_packages = []

    for package in packages_to_check:
        try:
            __import__(package.replace('-', '_'))
            installed_packages.append((package, "[OK]"))
        except ImportError:
            installed_packages.append((package, "[MISSING]"))

    for package, status in installed_packages:
        print(f"  {package}: {status}")

    # 7. Generate mock report
    print("\n[7] GENERATING MOCK CSPM REPORT:")

    report = {
        "timestamp": platform.datetime.datetime.now().isoformat(),
        "script": os.path.basename(__file__),
        "system_info": {
            "python_version": sys.version.split()[0],
            "platform": platform.platform(),
            "cwd": os.getcwd()
        },
        "checks_performed": len(mock_checks),
        "results_summary": {
            "total_passed": sum(1 for c in mock_checks if c["status"] == "PASS"),
            "total_failed": sum(1 for c in mock_checks if c["status"] == "FAIL"),
            "by_severity": {
                "HIGH": sum(1 for c in mock_checks if c["severity"] == "HIGH"),
                "MEDIUM": sum(1 for c in mock_checks if c["severity"] == "MEDIUM"),
                "LOW": sum(1 for c in mock_checks if c["severity"] == "LOW")
            }
        }
    }

    print(f"  Report generated with {report['checks_performed']} checks")
    print(f"  Summary: {report['results_summary']['total_passed']} passed, "
          f"{report['results_summary']['total_failed']} failed")

    # 8. Check if output file argument provided
    output_file = None
    for i, arg in enumerate(sys.argv):
        if arg == "--output" and i + 1 < len(sys.argv):
            output_file = sys.argv[i + 1]
            break

    if output_file:
        try:
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"\n[8] REPORT SAVED TO: {output_file}")
        except Exception as e:
            print(f"\n[8] ERROR SAVING REPORT: {e}")
    else:
        print(f"\n[8] NO OUTPUT FILE SPECIFIED (use --output <filename> to save report)")

    print("\n" + "=" * 60)
    print("DEMO COMPLETED SUCCESSFULLY")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    # Handle import for platform.datetime
    if not hasattr(platform, 'datetime'):
        import datetime
        platform.datetime = datetime

    try:
        sys.exit(main())
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)