#!/usr/bin/env python3
"""
Comprehensive Test Runner - Executes all tests with coverage reporting
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path
from typing import Dict, List, Tuple


class ComprehensiveTestRunner:
    """Comprehensive test runner with coverage reporting"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.test_results = {}
        self.coverage_data = {}
        self.start_time = time.time()
    
    def log(self, message: str, level: str = "INFO"):
        """Log test execution messages"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def run_unit_tests(self) -> bool:
        """Run all unit tests"""
        self.log("Running unit tests...")
        
        unit_test_dirs = [
            "tests/unit",
            "tests/unit/test_agents.py",
            "tests/unit/test_integrations.py",
            "tests/unit/test_monitoring.py"
        ]
        
        success = True
        for test_path in unit_test_dirs:
            if os.path.exists(test_path):
                try:
                    result = subprocess.run([
                        "python", "-m", "pytest", test_path,
                        "-v", "--tb=short", "--cov=backend",
                        "--cov-report=term-missing", "--cov-report=html"
                    ], capture_output=True, text=True, cwd=self.project_root)
                    
                    if result.returncode == 0:
                        self.log(f"✅ Unit tests passed: {test_path}")
                        self.test_results[test_path] = {
                            "status": "passed",
                            "output": result.stdout
                        }
                    else:
                        self.log(f"❌ Unit tests failed: {test_path}", "ERROR")
                        self.log(result.stderr, "ERROR")
                        self.test_results[test_path] = {
                            "status": "failed",
                            "output": result.stdout,
                            "error": result.stderr
                        }
                        success = False
                except Exception as e:
                    self.log(f"❌ Error running unit tests {test_path}: {e}", "ERROR")
                    success = False
        
        return success
    
    def run_integration_tests(self) -> bool:
        """Run integration tests"""
        self.log("Running integration tests...")
        
        try:
            result = subprocess.run([
                "python", "-m", "pytest", "tests/integration",
                "-v", "--tb=short", "--cov=backend",
                "--cov-report=term-missing"
            ], capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode == 0:
                self.log("✅ Integration tests passed")
                self.test_results["integration"] = {
                    "status": "passed",
                    "output": result.stdout
                }
                return True
            else:
                self.log("❌ Integration tests failed", "ERROR")
                self.log(result.stderr, "ERROR")
                self.test_results["integration"] = {
                    "status": "failed",
                    "output": result.stdout,
                    "error": result.stderr
                }
                return False
        except Exception as e:
            self.log(f"❌ Error running integration tests: {e}", "ERROR")
            return False
    
    def run_api_tests(self) -> bool:
        """Run API tests"""
        self.log("Running API tests...")
        
        try:
            result = subprocess.run([
                "python", "-m", "pytest", "tests/api",
                "-v", "--tb=short", "--cov=backend",
                "--cov-report=term-missing"
            ], capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode == 0:
                self.log("✅ API tests passed")
                self.test_results["api"] = {
                    "status": "passed",
                    "output": result.stdout
                }
                return True
            else:
                self.log("❌ API tests failed", "ERROR")
                self.log(result.stderr, "ERROR")
                self.test_results["api"] = {
                    "status": "failed",
                    "output": result.stdout,
                    "error": result.stderr
                }
                return False
        except Exception as e:
            self.log(f"❌ Error running API tests: {e}", "ERROR")
            return False
    
    def run_security_tests(self) -> bool:
        """Run security tests"""
        self.log("Running security tests...")
        
        try:
            result = subprocess.run([
                "python", "-m", "pytest", "tests/security",
                "-v", "--tb=short", "--cov=backend",
                "--cov-report=term-missing"
            ], capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode == 0:
                self.log("✅ Security tests passed")
                self.test_results["security"] = {
                    "status": "passed",
                    "output": result.stdout
                }
                return True
            else:
                self.log("❌ Security tests failed", "ERROR")
                self.log(result.stderr, "ERROR")
                self.test_results["security"] = {
                    "status": "failed",
                    "output": result.stdout,
                    "error": result.stderr
                }
                return False
        except Exception as e:
            self.log(f"❌ Error running security tests: {e}", "ERROR")
            return False
    
    def run_performance_tests(self) -> bool:
        """Run performance tests"""
        self.log("Running performance tests...")
        
        try:
            result = subprocess.run([
                "python", "-m", "pytest", "tests/performance",
                "-v", "--tb=short"
            ], capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode == 0:
                self.log("✅ Performance tests passed")
                self.test_results["performance"] = {
                    "status": "passed",
                    "output": result.stdout
                }
                return True
            else:
                self.log("❌ Performance tests failed", "ERROR")
                self.log(result.stderr, "ERROR")
                self.test_results["performance"] = {
                    "status": "failed",
                    "output": result.stdout,
                    "error": result.stderr
                }
                return False
        except Exception as e:
            self.log(f"❌ Error running performance tests: {e}", "ERROR")
            return False
    
    def generate_coverage_report(self) -> Dict:
        """Generate comprehensive coverage report"""
        self.log("Generating coverage report...")
        
        try:
            result = subprocess.run([
                "python", "-m", "coverage", "run", "--source=backend",
                "-m", "pytest", "tests/", "--tb=no", "-q"
            ], capture_output=True, text=True, cwd=self.project_root)
            
            coverage_result = subprocess.run([
                "python", "-m", "coverage", "report", "--format=json"
            ], capture_output=True, text=True, cwd=self.project_root)
            
            if coverage_result.returncode == 0:
                coverage_data = json.loads(coverage_result.stdout)
                self.coverage_data = coverage_data
                
                # Calculate overall coverage
                total_lines = 0
                covered_lines = 0
                
                for file_data in coverage_data.get("files", {}).values():
                    total_lines += file_data.get("summary", {}).get("num_statements", 0)
                    covered_lines += file_data.get("summary", {}).get("covered_lines", 0)
                
                overall_coverage = (covered_lines / total_lines * 100) if total_lines > 0 else 0
                
                return {
                    "overall_coverage": overall_coverage,
                    "total_lines": total_lines,
                    "covered_lines": covered_lines,
                    "files": len(coverage_data.get("files", {}))
                }
            else:
                self.log("❌ Error generating coverage report", "ERROR")
                return {}
        except Exception as e:
            self.log(f"❌ Error generating coverage report: {e}", "ERROR")
            return {}
    
    def check_todo_comments(self) -> Dict:
        """Check for remaining TODO comments"""
        self.log("Checking for TODO comments...")
        
        try:
            result = subprocess.run([
                "grep", "-r", "-n", "TODO\\|FIXME\\|XXX\\|HACK",
                "--exclude-dir=node_modules",
                "--exclude-dir=.git",
                "--exclude=*.json",
                "--exclude=*.lock",
                "."
            ], capture_output=True, text=True, cwd=self.project_root)
            
            todo_count = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
            
            return {
                "todo_count": todo_count,
                "todos": result.stdout.strip().split('\n') if result.stdout.strip() else []
            }
        except Exception as e:
            self.log(f"❌ Error checking TODO comments: {e}", "ERROR")
            return {"todo_count": -1, "todos": []}
    
    def run_linting(self) -> bool:
        """Run code linting"""
        self.log("Running code linting...")
        
        try:
            result = subprocess.run([
                "python", "-m", "flake8", "backend/",
                "--max-line-length=120",
                "--ignore=E501,W503"
            ], capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode == 0:
                self.log("✅ Code linting passed")
                self.test_results["linting"] = {
                    "status": "passed",
                    "output": result.stdout
                }
                return True
            else:
                self.log("❌ Code linting failed", "ERROR")
                self.log(result.stdout, "ERROR")
                self.test_results["linting"] = {
                    "status": "failed",
                    "output": result.stdout
                }
                return False
        except Exception as e:
            self.log(f"❌ Error running linting: {e}", "ERROR")
            return False
    
    def run_type_checking(self) -> bool:
        """Run type checking"""
        self.log("Running type checking...")
        
        try:
            result = subprocess.run([
                "python", "-m", "mypy", "backend/",
                "--ignore-missing-imports",
                "--no-strict-optional"
            ], capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode == 0:
                self.log("✅ Type checking passed")
                self.test_results["type_checking"] = {
                    "status": "passed",
                    "output": result.stdout
                }
                return True
            else:
                self.log("❌ Type checking failed", "ERROR")
                self.log(result.stdout, "ERROR")
                self.test_results["type_checking"] = {
                    "status": "failed",
                    "output": result.stdout
                }
                return False
        except Exception as e:
            self.log(f"❌ Error running type checking: {e}", "ERROR")
            return False
    
    def generate_test_report(self) -> Dict:
        """Generate comprehensive test report"""
        end_time = time.time()
        duration = end_time - self.start_time
        
        # Count test results
        passed = sum(1 for result in self.test_results.values() if result["status"] == "passed")
        failed = sum(1 for result in self.test_results.values() if result["status"] == "failed")
        total = len(self.test_results)
        
        report = {
            "summary": {
                "total_tests": total,
                "passed": passed,
                "failed": failed,
                "success_rate": (passed / total * 100) if total > 0 else 0,
                "duration_seconds": duration
            },
            "test_results": self.test_results,
            "coverage": self.coverage_data,
            "todo_check": self.check_todo_comments(),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return report
    
    def save_report(self, report: Dict):
        """Save test report to file"""
        report_file = self.project_root / "test_reports" / f"test_report_{int(time.time())}.json"
        report_file.parent.mkdir(exist_ok=True)
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.log(f"Test report saved: {report_file}")
    
    def print_summary(self, report: Dict):
        """Print test summary"""
        summary = report["summary"]
        coverage = report.get("coverage", {})
        todo_check = report.get("todo_check", {})
        
        print("\n" + "="*80)
        print("COMPREHENSIVE TEST SUMMARY")
        print("="*80)
        
        print(f"Test Results:")
        print(f"  Total Test Suites: {summary['total_tests']}")
        print(f"  Passed: {summary['passed']}")
        print(f"  Failed: {summary['failed']}")
        print(f"  Success Rate: {summary['success_rate']:.1f}%")
        print(f"  Duration: {summary['duration_seconds']:.2f} seconds")
        
        if coverage:
            print(f"\nCode Coverage:")
            print(f"  Overall Coverage: {coverage.get('overall_coverage', 0):.1f}%")
            print(f"  Total Lines: {coverage.get('total_lines', 0)}")
            print(f"  Covered Lines: {coverage.get('covered_lines', 0)}")
            print(f"  Files: {coverage.get('files', 0)}")
        
        print(f"\nCode Quality:")
        print(f"  TODO Comments: {todo_check.get('todo_count', 0)}")
        
        print("\n" + "="*80)
        
        if summary['failed'] > 0:
            print("❌ SOME TESTS FAILED - Please review the results above")
            return False
        else:
            print("✅ ALL TESTS PASSED - Code is ready for production!")
            return True
    
    def run_all_tests(self) -> bool:
        """Run all tests and generate comprehensive report"""
        self.log("Starting comprehensive test suite...")
        
        # Run all test types
        unit_success = self.run_unit_tests()
        integration_success = self.run_integration_tests()
        api_success = self.run_api_tests()
        security_success = self.run_security_tests()
        performance_success = self.run_performance_tests()
        
        # Run code quality checks
        linting_success = self.run_linting()
        type_checking_success = self.run_type_checking()
        
        # Generate coverage report
        coverage_data = self.generate_coverage_report()
        
        # Generate and save report
        report = self.generate_test_report()
        self.save_report(report)
        
        # Print summary
        overall_success = self.print_summary(report)
        
        return overall_success


def main():
    """Main test runner"""
    runner = ComprehensiveTestRunner()
    
    try:
        success = runner.run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ Test execution interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during test execution: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
