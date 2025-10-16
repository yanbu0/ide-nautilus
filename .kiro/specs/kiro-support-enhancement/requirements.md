# Requirements Document

## Introduction

This feature enhances the code-nautilus project to support Kiro IDE alongside Visual Studio Code. The enhancement includes adding configurable wget flags for installation and providing users with an "Open in Kiro" context menu option in Nautilus file manager.

## Glossary

- **Nautilus Extension**: A Python-based plugin that extends the Nautilus file manager with custom context menu items
- **Kiro IDE**: An AI-powered integrated development environment
- **VSCode**: Visual Studio Code editor
- **Context Menu**: Right-click menu that appears when selecting files or folders in Nautilus
- **Installation Script**: The bash script that downloads and installs the Nautilus extension
- **Wget Flags**: Command-line options that modify wget behavior during file downloads

## Requirements

### Requirement 1

**User Story:** As a developer, I want to configure wget flags during installation, so that I can customize the download behavior according to my network or security requirements.

#### Acceptance Criteria

1. WHEN the installation script is executed with a flag parameter, THE Installation_Script SHALL pass the specified flags to the wget command
2. WHERE no flags are specified, THE Installation_Script SHALL use the default quiet output flag (-q)
3. THE Installation_Script SHALL validate that provided flags are safe wget options
4. THE Installation_Script SHALL display help information when invalid flags are provided

### Requirement 2

**User Story:** As a Kiro user, I want an "Open in Kiro" option in the Nautilus context menu, so that I can directly open files and folders in Kiro IDE from the file manager.

#### Acceptance Criteria

1. WHEN right-clicking on files or folders in Nautilus, THE Nautilus_Extension SHALL display both "Open in Code" and "Open in Kiro" menu options
2. WHEN the "Open in Kiro" option is selected, THE Nautilus_Extension SHALL launch Kiro IDE with the selected files or folders
3. WHERE Kiro is not installed on the system, THE Nautilus_Extension SHALL handle the error gracefully and display an appropriate message
4. THE Nautilus_Extension SHALL support the same file and folder selection behaviors for Kiro as it does for VSCode
5. WHEN opening a directory in Kiro, THE Nautilus_Extension SHALL create a new Kiro window if the directory exists

### Requirement 3

**User Story:** As a system administrator, I want the installation process to remain backward compatible, so that existing users are not affected by the new features.

#### Acceptance Criteria

1. WHERE no installation parameters are provided, THE Installation_Script SHALL maintain the current default behavior
2. THE Installation_Script SHALL continue to install the VSCode functionality as the primary option
3. THE Nautilus_Extension SHALL display both IDE options without requiring additional configuration
4. THE Installation_Script SHALL not break existing installations when updated