# Design Document

## Overview

The Nautilus-Kiro integration consists of a Python-based Nautilus extension that adds context menu items for opening files and directories in Kiro. The solution modifies the existing VSCode-based extension to work with Kiro instead, ensuring proper command execution and error handling.

## Architecture

The integration follows Nautilus's extension architecture pattern:

```
User Right-Click → Nautilus → Python Extension → Kiro Command → Kiro Launch
```

### Components

1. **KiroExtension Class**: Main extension class inheriting from Nautilus.MenuProvider
2. **Installation Script**: Bash script for dependency management and extension deployment
3. **Command Execution Layer**: Subprocess handling for launching Kiro

## Components and Interfaces

### KiroExtension Class

```python
class VSCodeKiroExtension(GObject.GObject, Nautilus.MenuProvider):
    def launch_vscode(self, menu, files)  # Existing VSCode functionality
    def launch_kiro(self, menu, files)    # New Kiro functionality
    def get_file_items(self, *args)       # Returns both VSCode and Kiro menu items
    def get_background_items(self, *args) # Returns both VSCode and Kiro menu items
```

**Key Changes from VSCode Version:**
- Add `KIRO = 'kiro'` alongside existing `VSCODE = 'code'`
- Create additional menu items for "Open in Kiro" while preserving "Open in Code"
- Add new `launch_kiro` method alongside existing `launch_vscode` method
- Maintain both VSCode and Kiro functionality in the same extension

### Menu Item Creation

The extension creates four types of menu items:
1. **VSCode File/Directory Items**: Existing "Open in Code" functionality
2. **Kiro File/Directory Items**: New "Open in Kiro" functionality  
3. **VSCode Background Items**: Existing "Open in Code" for current directory
4. **Kiro Background Items**: New "Open in Kiro" for current directory

### Command Execution

The `launch_kiro` method handles:
- Path sanitization with proper quoting
- Multiple file selection support
- Error handling for missing kiro command
- Background process execution

## Data Models

### File Path Handling
- Input: Nautilus file objects with `get_location().get_path()` method
- Processing: Quote paths to handle spaces and special characters
- Output: Space-separated quoted paths for command line execution

### Menu Item Structure
```python
Nautilus.MenuItem(
    name='KiroOpen',
    label='Open in Kiro',
    tip='Opens the selected files/directories with Kiro'
)
```

## Error Handling

### Command Not Found
- Check if `kiro` command exists in PATH during installation
- Graceful degradation if command fails during execution
- User feedback through installation script

### Path Handling
- Proper quoting of file paths to handle spaces and special characters
- Validation of file/directory existence before command execution

### Extension Loading
- Proper GObject inheritance for Nautilus compatibility
- Error handling for missing python-nautilus dependency

## Testing Strategy

### Manual Testing
1. **Installation Testing**
   - Test on different Linux distributions (Arch, Ubuntu, Fedora)
   - Verify dependency installation
   - Confirm extension file placement

2. **Functionality Testing**
   - Right-click on files → verify "Open in Kiro" appears
   - Right-click on directories → verify "Open in Kiro" appears
   - Right-click in empty space → verify "Open in Kiro" appears
   - Test with files/directories containing spaces
   - Test with multiple file selection

3. **Integration Testing**
   - Verify Kiro launches with correct arguments
   - Test with different file types
   - Test with nested directory structures

### Error Scenario Testing
- Test behavior when kiro command is not installed
- Test with invalid file paths
- Test Nautilus restart after installation

## Implementation Notes

### Key Additions to VSCode Extension
1. **Dual Command Support**: Add `kiro` command alongside existing `code` command
2. **Additional Menu Items**: Create separate Kiro menu items while preserving VSCode ones
3. **Separate Launch Methods**: Implement `launch_kiro` method alongside existing `launch_vscode`
4. **Error Handling**: Add validation for kiro command availability without affecting VSCode functionality

### Installation Process
1. Detect and install python-nautilus dependency
2. Create extensions directory if it doesn't exist
3. Replace existing VSCode-only extension with combined VSCode+Kiro extension
4. Install the enhanced extension with both VSCode and Kiro support
5. Restart Nautilus to load the extension
6. Verify both code and kiro commands availability

### File Structure
```
~/.local/share/nautilus-python/extensions/
└── kiro-nautilus.py
```