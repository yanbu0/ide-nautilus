# Implementation Plan

- [x] 1. Enhance existing Nautilus extension to support both VSCode and Kiro
  - Add kiro command support alongside existing VSCode functionality
  - Create additional menu items for "Open in Kiro" while preserving "Open in Code"
  - Implement new launch_kiro method alongside existing launch_vscode method
  - Update class name to reflect dual functionality
  - _Requirements: 1.1, 1.2, 1.3, 2.1, 2.2, 2.3_

- [x] 2. Implement proper error handling and command validation
  - Add error handling for missing kiro command
  - Implement graceful failure when subprocess execution fails
  - Ensure proper path quoting for files with spaces and special characters
  - _Requirements: 2.4, 1.4_

- [x] 3. Update installation script for dual VSCode+Kiro integration
  - Modify install.sh to install enhanced extension with both VSCode and Kiro support
  - Add validation to check if both code and kiro commands are available in PATH
  - Update script to replace existing extension with enhanced version
  - Add proper feedback messages for installation success/failure and command availability
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [x] 4. Update project documentation
  - Modify README.md to reflect dual VSCode and Kiro integration
  - Update installation instructions to mention both editors
  - Add troubleshooting section for both VSCode and Kiro command issues
  - _Requirements: 3.5_