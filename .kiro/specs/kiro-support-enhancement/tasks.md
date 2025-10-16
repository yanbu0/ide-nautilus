# Implementation Plan

- [x] 1. Enhance installation script with wget flag support
  - Add command-line argument parsing to install.sh for wget flags
  - Implement flag validation to prevent unsafe wget options
  - Add help documentation and usage instructions
  - Maintain backward compatibility with existing installation behavior
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 3.1_

- [x] 2. Refactor Python extension for dual IDE support
  - [x] 2.1 Create IDE provider interface and base classes
    - Define IDEProvider abstract base class with required methods
    - Create IDEConfig dataclass for IDE configuration
    - _Requirements: 2.1, 2.2_

  - [x] 2.2 Implement VSCode provider (refactor existing code)
    - Extract existing VSCode functionality into VSCodeProvider class
    - Implement IDEProvider interface methods for VSCode
    - Maintain existing VSCode behavior and configuration
    - _Requirements: 2.4, 3.2_

  - [x] 2.3 Implement Kiro provider
    - Create KiroProvider class implementing IDEProvider interface
    - Add Kiro-specific command and argument handling
    - Implement availability checking for Kiro installation
    - _Requirements: 2.2, 2.3, 2.5_

  - [x] 2.4 Update main extension class for multiple IDE support
    - Modify VSCodeExtension class to support multiple IDE providers
    - Generate menu items dynamically based on available IDEs
    - Implement error handling for missing IDEs
    - _Requirements: 2.1, 2.3, 3.3_

- [x] 3. Add error handling and user feedback
  - Implement graceful error handling for missing IDEs
  - Add user-friendly error messages through Nautilus notifications
  - Create fallback behavior when IDEs are unavailable
  - _Requirements: 2.3, 3.3_

- [x] 4. Update project documentation
  - Update README.md with new installation options and Kiro support
  - Add usage examples for wget flags
  - Document both IDE options and requirements
  - _Requirements: 1.4, 2.1_

- [x] 5. Create test suite for installation script
  - Write unit tests for flag parsing and validation
  - Create integration tests for installation scenarios
  - Add compatibility tests for backward compatibility verification
  - _Requirements: 1.1, 1.2, 1.3, 3.1_

- [x] 6. Create test suite for Python extension
  - Write unit tests for IDE provider classes
  - Create functional tests for menu generation and IDE launching
  - Add error scenario tests for missing IDEs and invalid paths
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_