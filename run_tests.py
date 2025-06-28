#!/usr/bin/env python3
"""
Test runner script for the MantisX Service project.
This script can be used to run tests with different configurations.
"""

import sys
import subprocess
from pathlib import Path


def run_tests(test_type="all", verbose=False, coverage=True):
    """Run tests with specified configuration"""
    cmd = ["python", "-m", "pytest"]

    if verbose:
        cmd.append("-v")

    if coverage:
        cmd.extend(["--cov=.", "--cov-report=term-missing"])

    if test_type == "unit":
        cmd.extend(["-m", "unit"])
    elif test_type == "integration":
        cmd.extend(["-m", "integration"])
    elif test_type != "all":
        cmd.append(f"tests/test_{test_type}.py")

    print(f"Running command: {' '.join(cmd)}")
    return subprocess.run(cmd, cwd=Path(__file__).parent)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run tests for MantisX Service")
    parser.add_argument("--type", choices=["all", "unit", "integration", "main", "utils", "models", "network"],
                       default="all", help="Type of tests to run")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--no-coverage", action="store_true", help="Disable coverage reporting")

    args = parser.parse_args()

    result = run_tests(
        test_type=args.type,
        verbose=args.verbose,
        coverage=not args.no_coverage
    )

    sys.exit(result.returncode)
