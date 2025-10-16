# Python Extension Test Suite

This directory contains comprehensive tests for the code-nautilus Python extension.

## Test Coverage

The test suite covers all requirements from the specification:

### Unit Tests for IDE Provider Classes
- **VSCodeProvider Tests**: Interface compliance, command/display name validation, argument generation, availability checking
- **KiroProvider Tests**: Interface compliance, command/display name validation, argument generation, availability checking with fallback behavior
- **Availability Checking**: Mocked subprocess calls to test IDE detection logic

### Functional Tests for Menu Generation
- **Menu Item Creation**: Tests for both file and background context menus
- **IDE Availability Handling**: Menu generation when IDEs are available vs unavailable
- **Extension Initialization**: Proper provider setup and configuration

### Error Scenario Tests
- **Invalid File Paths**: Handling of non-existent or inaccessible files
- **Unavailable IDEs**: Graceful handling when IDEs are not installed
- **Mixed Valid/Invalid Paths**: Processing files where some paths are valid and others are not
- **Exception Handling**: Graceful degradation when menu creation fails

## Running Tests

### Run All Extension Tests
```bash
python3 tests/run_extension_tests.py
```

### Run Individual Test Classes
```bash
python3 -m unittest tests.test_extension.TestIDEProviders -v
python3 -m unittest tests.test_extension.TestVSCodeExtension -v
python3 -m unittest tests.test_extension.TestIDELaunching -v
python3 -m unittest tests.test_extension.TestErrorScenarios -v
```

## Test Requirements Covered

- **Requirement 2.1**: IDE provider interface compliance and functionality
- **Requirement 2.2**: Menu generation for file and directory contexts
- **Requirement 2.3**: Error handling for missing IDEs
- **Requirement 2.4**: Path validation and error scenarios
- **Requirement 2.5**: Graceful degradation and exception handling

## Test Results

All 16 tests pass successfully, providing comprehensive coverage of:
- IDE provider class functionality
- Menu generation logic
- Error handling scenarios
- Edge cases and invalid inputs

The test suite uses mocking to avoid dependencies on actual IDE installations and system calls, ensuring tests are fast, reliable, and can run in any environment.