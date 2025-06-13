#!/usr/bin/env python
"""
Custom test runner script for FitTrack backend.
Provides convenient commands for running different types of tests.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, description=""):
    """Run a shell command and return the result."""
    if description:
        print(f"\n🔄 {description}")
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Success!")
        if result.stdout:
            print(result.stdout)
    else:
        print("❌ Failed!")
        if result.stderr:
            print(result.stderr)
        if result.stdout:
            print(result.stdout)
    
    return result


def test_unit():
    """Run unit tests only."""
    cmd = ["python", "manage.py", "test", "--keepdb"]
    return run_command(cmd, "Running unit tests with Django test runner")


def test_pytest():
    """Run tests with pytest."""
    cmd = ["pytest", "-v", "--tb=short"]
    return run_command(cmd, "Running tests with pytest")


def test_coverage():
    """Run tests with coverage report."""
    commands = [
        (["coverage", "run", "--source=.", "manage.py", "test"], "Running tests with coverage"),
        (["coverage", "report"], "Generating coverage report"),
        (["coverage", "html"], "Generating HTML coverage report")
    ]
    
    for cmd, desc in commands:
        result = run_command(cmd, desc)
        if result.returncode != 0:
            return result
    
    print("\n📊 Coverage report generated in htmlcov/index.html")
    return result


def test_specific_app(app_name):
    """Run tests for a specific app."""
    cmd = ["python", "manage.py", "test", app_name, "--keepdb"]
    return run_command(cmd, f"Running tests for {app_name} app")


def test_specific_file(file_path):
    """Run tests for a specific test file."""
    if file_path.endswith('.py'):
        file_path = file_path[:-3]  # Remove .py extension
    
    file_path = file_path.replace('/', '.')
    cmd = ["python", "manage.py", "test", file_path, "--keepdb"]
    return run_command(cmd, f"Running tests in {file_path}")


def test_api_only():
    """Run API tests only."""
    cmd = ["pytest", "-v", "-m", "api", "--tb=short"]
    return run_command(cmd, "Running API tests only")


def test_integration_only():
    """Run integration tests only."""
    cmd = ["pytest", "-v", "-m", "integration", "--tb=short"]
    return run_command(cmd, "Running integration tests only")


def test_fast():
    """Run fast tests only (unit tests, no slow tests)."""
    cmd = ["pytest", "-v", "-m", "not slow", "--tb=short"]
    return run_command(cmd, "Running fast tests only")


def test_all():
    """Run all tests with comprehensive output."""
    commands = [
        (["python", "manage.py", "test", "--keepdb"], "Running Django tests"),
        (["pytest", "-v", "--tb=short"], "Running pytest tests")
    ]
    
    for cmd, desc in commands:
        result = run_command(cmd, desc)
        if result.returncode != 0:
            print(f"❌ {desc} failed!")
            return result
    
    print("\n🎉 All tests passed!")
    return result


def lint_code():
    """Run code linting."""
    commands = [
        (["flake8", ".", "--max-line-length=100", "--exclude=venv,migrations"], "Running flake8 linting"),
        (["black", ".", "--check", "--exclude=venv"], "Checking code formatting with black"),
        (["isort", ".", "--check-only", "--skip=venv"], "Checking import sorting with isort")
    ]
    
    for cmd, desc in commands:
        result = run_command(cmd, desc)
        if result.returncode != 0:
            print(f"❌ {desc} failed!")
    
    return result


def format_code():
    """Format code automatically."""
    commands = [
        (["black", ".", "--exclude=venv"], "Formatting code with black"),
        (["isort", ".", "--skip=venv"], "Sorting imports with isort")
    ]
    
    for cmd, desc in commands:
        run_command(cmd, desc)


def show_test_structure():
    """Show the test directory structure."""
    print("\n📁 Test Structure:")
    
    test_dirs = [
        "core/tests",
        "accounts/tests", 
        "workouts/tests",
        "nutrition/tests",
        "tests"
    ]
    
    for test_dir in test_dirs:
        if os.path.exists(test_dir):
            print(f"\n📂 {test_dir}/")
            for file in os.listdir(test_dir):
                if file.endswith('.py'):
                    print(f"  📄 {file}")


def main():
    """Main function to parse arguments and run appropriate tests."""
    parser = argparse.ArgumentParser(description="FitTrack Test Runner")
    
    subparsers = parser.add_subparsers(dest='command', help='Test commands')
    
    # Test commands
    subparsers.add_parser('unit', help='Run unit tests with Django test runner')
    subparsers.add_parser('pytest', help='Run tests with pytest')
    subparsers.add_parser('coverage', help='Run tests with coverage report')
    subparsers.add_parser('api', help='Run API tests only')
    subparsers.add_parser('integration', help='Run integration tests only')
    subparsers.add_parser('fast', help='Run fast tests only')
    subparsers.add_parser('all', help='Run all tests')
    
    # Specific test commands
    app_parser = subparsers.add_parser('app', help='Run tests for specific app')
    app_parser.add_argument('app_name', help='Name of the app to test')
    
    file_parser = subparsers.add_parser('file', help='Run tests for specific file')
    file_parser.add_argument('file_path', help='Path to the test file')
    
    # Code quality commands
    subparsers.add_parser('lint', help='Run code linting')
    subparsers.add_parser('format', help='Format code automatically')
    
    # Utility commands
    subparsers.add_parser('structure', help='Show test directory structure')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Change to the directory containing this script
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Execute the appropriate command
    if args.command == 'unit':
        test_unit()
    elif args.command == 'pytest':
        test_pytest()
    elif args.command == 'coverage':
        test_coverage()
    elif args.command == 'api':
        test_api_only()
    elif args.command == 'integration':
        test_integration_only()
    elif args.command == 'fast':
        test_fast()
    elif args.command == 'all':
        test_all()
    elif args.command == 'app':
        test_specific_app(args.app_name)
    elif args.command == 'file':
        test_specific_file(args.file_path)
    elif args.command == 'lint':
        lint_code()
    elif args.command == 'format':
        format_code()
    elif args.command == 'structure':
        show_test_structure()


if __name__ == '__main__':
    main()