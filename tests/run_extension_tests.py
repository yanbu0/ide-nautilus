#!/usr/bin/env python3
"""
Test runner for code-nautilus Python extension tests.

This script runs all Python extension tests and provides detailed output
with proper error handling and test discovery.
"""

import sys
import os
import unittest
import subprocess
from io import StringIO

# Colors for output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    BOLD = '\033[1m'
    NC = '\033[0m'  # No Color


def print_header(text):
    """Print a colored header"""
    print(f"{Colors.BLUE}{Colors.BOLD}{text}{Colors.NC}")
    print("=" * len(text))
    print()


def print_success(text):
    """Print success message in green"""
    print(f"{Colors.GREEN}✓ {text}{Colors.NC}")


def print_error(text):
    """Print error message in red"""
    print(f"{Colors.RED}✗ {text}{Colors.NC}")


def print_warning(text):
    """Print warning message in yellow"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.NC}")


def check_dependencies():
    """Check if required dependencies are available"""
    print_header("Checking Dependencies")
    
    dependencies_ok = True
    
    # Check Python version
    if sys.version_info < (3, 6):
        print_error(f"Python 3.6+ required, found {sys.version}")
        dependencies_ok = False
    else:
        print_success(f"Python version: {sys.version.split()[0]}")
    
    # Check if main extension file exists
    extension_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "code-nautilus.py")
    if not os.path.exists(extension_file):
        print_error("code-nautilus.py not found in project root")
        dependencies_ok = False
    else:
        print_success("Extension file found")
    
    # Check for unittest module
    try:
        import unittest
        print_success("unittest module available")
    except ImportError:
        print_error("unittest module not available")
        dependencies_ok = False
    
    # Check for mock module (should be available in Python 3.3+)
    try:
        from unittest.mock import Mock
        print_success("unittest.mock module available")
    except ImportError:
        print_error("unittest.mock module not available")
        dependencies_ok = False
    
    print()
    return dependencies_ok


def discover_and_run_tests():
    """Discover and run all extension tests"""
    print_header("Running Python Extension Tests")
    
    # Change to tests directory
    test_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(test_dir)
    
    # Discover tests
    loader = unittest.TestLoader()
    start_dir = test_dir
    suite = loader.discover(start_dir, pattern='test_extension.py')
    
    # Count tests
    test_count = suite.countTestCases()
    print(f"Discovered {test_count} tests")
    print()
    
    # Run tests with detailed output
    stream = StringIO()
    runner = unittest.TextTestRunner(
        stream=stream,
        verbosity=2,
        buffer=True,
        failfast=False
    )
    
    result = runner.run(suite)
    
    # Print results
    output = stream.getvalue()
    print(output)
    
    # Print summary
    print_header("Test Summary")
    
    if result.wasSuccessful():
        print_success(f"All {result.testsRun} tests passed!")
        return True
    else:
        print_error(f"{len(result.failures)} test(s) failed")
        print_error(f"{len(result.errors)} test(s) had errors")
        
        # Print failure details
        if result.failures:
            print()
            print_header("Test Failures")
            for test, traceback in result.failures:
                print(f"{Colors.RED}FAIL: {test}{Colors.NC}")
                print(traceback)
                print()
        
        # Print error details
        if result.errors:
            print()
            print_header("Test Errors")
            for test, traceback in result.errors:
                print(f"{Colors.RED}ERROR: {test}{Colors.NC}")
                print(traceback)
                print()
        
        return False


def main():
    """Main test runner function"""
    print_header("Code-Nautilus Python Extension Test Runner")
    
    # Check dependencies first
    if not check_dependencies():
        print_error("Dependency check failed. Please resolve issues before running tests.")
        return 1
    
    # Run tests
    success = discover_and_run_tests()
    
    if success:
        print_success("All tests completed successfully!")
        return 0
    else:
        print_error("Some tests failed. Please review the output above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())