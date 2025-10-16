# Test Suite for Code-Nautilus Installation Script

This directory contains comprehensive tests for the `install.sh` script, covering flag parsing, validation, installation scenarios, and backward compatibility.

## Test Structure

### Unit Tests
- **Flag Parsing and Validation**: Tests the `validate_wget_flags` function with various valid and invalid flag combinations
- **Security Validation**: Ensures unsafe wget flags are properly rejected
- **Input Validation**: Tests malformed flag handling and edge cases

### Integration Tests
- **Installation Scenarios**: Tests end-to-end installation with different flag combinations
- **Help System**: Validates help flag functionality
- **Error Handling**: Tests invalid flag rejection and error messages

### Compatibility Tests
- **Backward Compatibility**: Ensures existing installations continue to work
- **Default Behavior**: Verifies that no-argument execution maintains original behavior
- **Flag Override**: Tests that custom flags properly override defaults

### Error Scenario Tests
- **Unsafe Flag Rejection**: Tests security measures for dangerous wget flags
- **Malformed Input**: Tests handling of invalid flag formats
- **Edge Cases**: Tests empty values and boundary conditions

## Running Tests

### Run All Tests
```bash
cd tests/
chmod +x run_tests.sh test_install.sh
./run_tests.sh
```

### Run Individual Test Suite
```bash
cd tests/
chmod +x test_install.sh
./test_install.sh
```

## Test Requirements

The tests validate the following requirements from the specification:

- **Requirement 1.1**: Installation script accepts and processes wget flags
- **Requirement 1.2**: Default behavior is maintained when no flags are provided
- **Requirement 1.3**: Flag validation prevents unsafe wget options
- **Requirement 3.1**: Backward compatibility is preserved for existing users

## Test Coverage

### Flag Validation Tests
- Valid flags: `-q`, `-v --timeout=30`, `--progress=bar`
- Invalid security risks: `--output-document=/etc/passwd`, `--directory-prefix=/tmp`, `--execute`, `--load-cookies`
- Malformed flags: flags without dash prefix

### Installation Scenario Tests
- Help flag functionality (`--help`)
- Invalid flag rejection
- Wget flags without values
- Custom flag integration with mock wget

### Compatibility Tests
- Default behavior preservation (no arguments)
- Flag override functionality
- Existing installation compatibility

### Error Handling Tests
- Unsafe flag rejection with appropriate error messages
- Malformed flag handling
- Empty flag value processing

## Test Output

The test suite provides colored output with:
- ✓ Green checkmarks for passing tests
- ✗ Red X marks for failing tests
- Yellow headers for test sections
- Detailed failure messages for debugging

## Mock Testing

The integration tests use mock commands to avoid:
- Actual network downloads during testing
- System modifications during test runs
- Dependency on external services

This ensures tests are:
- Fast and reliable
- Safe to run in any environment
- Independent of network conditions