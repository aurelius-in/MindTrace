#!/usr/bin/env python3
"""
Test runner for Enterprise Employee Wellness AI application
"""
import os
import sys
import subprocess
import argparse
import time
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(command)}")
    print(f"{'='*60}")
    
    start_time = time.time()
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        end_time = time.time()
        print(f"✅ {description} completed successfully in {end_time - start_time:.2f} seconds")
        if result.stdout:
            print("Output:")
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        end_time = time.time()
        print(f"❌ {description} failed after {end_time - start_time:.2f} seconds")
        print(f"Error code: {e.returncode}")
        if e.stdout:
            print("Stdout:")
            print(e.stdout)
        if e.stderr:
            print("Stderr:")
            print(e.stderr)
        return False


def run_unit_tests(verbose=False, coverage=False):
    """Run unit tests."""
    command = ["python", "-m", "pytest", "tests/unit/"]
    if verbose:
        command.append("-v")
    if coverage:
        command.extend(["--cov=backend", "--cov-report=html", "--cov-report=term"])
    
    return run_command(command, "Unit Tests")


def run_api_tests(verbose=False, coverage=False):
    """Run API tests."""
    command = ["python", "-m", "pytest", "tests/api/"]
    if verbose:
        command.append("-v")
    if coverage:
        command.extend(["--cov=backend", "--cov-report=html", "--cov-report=term"])
    
    return run_command(command, "API Tests")


def run_integration_tests(verbose=False, coverage=False):
    """Run integration tests."""
    command = ["python", "-m", "pytest", "tests/integration/"]
    if verbose:
        command.append("-v")
    if coverage:
        command.extend(["--cov=backend", "--cov-report=html", "--cov-report=term"])
    
    return run_command(command, "Integration Tests")


def run_security_tests(verbose=False, coverage=False):
    """Run security tests."""
    command = ["python", "-m", "pytest", "tests/security/"]
    if verbose:
        command.append("-v")
    if coverage:
        command.extend(["--cov=backend", "--cov-report=html", "--cov-report=term"])
    
    return run_command(command, "Security Tests")


def run_performance_tests(verbose=False):
    """Run performance tests."""
    command = ["python", "-m", "pytest", "tests/performance/", "-m", "performance"]
    if verbose:
        command.append("-v")
    
    return run_command(command, "Performance Tests")


def run_all_tests(verbose=False, coverage=False, parallel=False):
    """Run all tests."""
    command = ["python", "-m", "pytest", "tests/"]
    if verbose:
        command.append("-v")
    if coverage:
        command.extend(["--cov=backend", "--cov-report=html", "--cov-report=term"])
    if parallel:
        command.extend(["-n", "auto"])
    
    return run_command(command, "All Tests")


def run_specific_test(test_path, verbose=False):
    """Run a specific test file or test function."""
    command = ["python", "-m", "pytest", test_path]
    if verbose:
        command.append("-v")
    
    return run_command(command, f"Specific Test: {test_path}")


def run_tests_with_markers(markers, verbose=False, coverage=False):
    """Run tests with specific markers."""
    command = ["python", "-m", "pytest", "tests/", "-m", markers]
    if verbose:
        command.append("-v")
    if coverage:
        command.extend(["--cov=backend", "--cov-report=html", "--cov-report=term"])
    
    return run_command(command, f"Tests with markers: {markers}")


def run_linting():
    """Run code linting."""
    commands = [
        (["python", "-m", "flake8", "backend/"], "Flake8 Linting"),
        (["python", "-m", "black", "--check", "backend/"], "Black Format Check"),
        (["python", "-m", "isort", "--check-only", "backend/"], "Import Sort Check"),
        (["python", "-m", "mypy", "backend/"], "Type Checking")
    ]
    
    results = []
    for command, description in commands:
        results.append(run_command(command, description))
    
    return all(results)


def run_security_scanning():
    """Run security scanning tools."""
    commands = [
        (["bandit", "-r", "backend/"], "Bandit Security Scan"),
        (["safety", "check"], "Safety Dependency Check")
    ]
    
    results = []
    for command, description in commands:
        results.append(run_command(command, description))
    
    return all(results)


def generate_test_report():
    """Generate a comprehensive test report."""
    command = [
        "python", "-m", "pytest", "tests/",
        "--cov=backend",
        "--cov-report=html:htmlcov",
        "--cov-report=xml:coverage.xml",
        "--cov-report=term-missing",
        "--junitxml=test-results.xml",
        "--html=test-report.html",
        "--self-contained-html"
    ]
    
    return run_command(command, "Generate Test Report")


def main():
    """Main function to parse arguments and run tests."""
    parser = argparse.ArgumentParser(description="Test runner for Enterprise Employee Wellness AI")
    
    parser.add_argument("--unit", action="store_true", help="Run unit tests")
    parser.add_argument("--api", action="store_true", help="Run API tests")
    parser.add_argument("--integration", action="store_true", help="Run integration tests")
    parser.add_argument("--security", action="store_true", help="Run security tests")
    parser.add_argument("--performance", action="store_true", help="Run performance tests")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--lint", action="store_true", help="Run linting checks")
    parser.add_argument("--security-scan", action="store_true", help="Run security scanning")
    parser.add_argument("--report", action="store_true", help="Generate comprehensive test report")
    parser.add_argument("--test", type=str, help="Run specific test file or function")
    parser.add_argument("--markers", type=str, help="Run tests with specific markers")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
    parser.add_argument("--parallel", action="store_true", help="Run tests in parallel")
    
    args = parser.parse_args()
    
    # Change to project root directory
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print("🚀 Enterprise Employee Wellness AI - Test Runner")
    print(f"📁 Working directory: {os.getcwd()}")
    
    results = []
    
    # Run specific test types
    if args.unit:
        results.append(run_unit_tests(args.verbose, args.coverage))
    
    if args.api:
        results.append(run_api_tests(args.verbose, args.coverage))
    
    if args.integration:
        results.append(run_integration_tests(args.verbose, args.coverage))
    
    if args.security:
        results.append(run_security_tests(args.verbose, args.coverage))
    
    if args.performance:
        results.append(run_performance_tests(args.verbose))
    
    if args.all:
        results.append(run_all_tests(args.verbose, args.coverage, args.parallel))
    
    if args.lint:
        results.append(run_linting())
    
    if args.security_scan:
        results.append(run_security_scanning())
    
    if args.report:
        results.append(generate_test_report())
    
    if args.test:
        results.append(run_specific_test(args.test, args.verbose))
    
    if args.markers:
        results.append(run_tests_with_markers(args.markers, args.verbose, args.coverage))
    
    # If no specific tests were requested, run all tests
    if not any([args.unit, args.api, args.integration, args.security, args.performance, 
                args.all, args.lint, args.security_scan, args.report, args.test, args.markers]):
        print("\nNo specific tests requested. Running all tests...")
        results.append(run_all_tests(args.verbose, args.coverage, args.parallel))
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 Test Summary")
    print(f"{'='*60}")
    
    if results:
        passed = sum(results)
        total = len(results)
        print(f"✅ Passed: {passed}/{total}")
        print(f"❌ Failed: {total - passed}/{total}")
        
        if passed == total:
            print("🎉 All tests passed!")
            return 0
        else:
            print("💥 Some tests failed!")
            return 1
    else:
        print("⚠️  No tests were run!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
