# Design Document

## Overview

This design extends the code-nautilus project to support dual IDE functionality (VSCode and Kiro) while adding configurable wget flags to the installation process. The solution maintains backward compatibility and follows the existing architecture patterns.

## Architecture

The enhancement follows a dual-provider pattern where both IDEs are supported through a unified extension interface:

```
Nautilus File Manager
    ↓
Enhanced Python Extension
    ├── VSCode Provider (existing)
    └── Kiro Provider (new)
```

### Installation Architecture

```
install.sh
    ├── Flag Parser (new)
    ├── Dependency Installation (existing)
    └── Extension Download (enhanced)
```

## Components and Interfaces

### 1. Enhanced Installation Script

**Purpose**: Handle wget flag configuration and maintain backward compatibility

**Key Changes**:
- Add command-line argument parsing for wget flags
- Implement flag validation to prevent unsafe options
- Maintain default behavior when no flags are provided
- Add help documentation for new options

**Interface**:
```bash
./install.sh [--wget-flags "flag1 flag2"] [--help]
```

### 2. Dual IDE Extension

**Purpose**: Provide context menu options for both VSCode and Kiro

**Architecture Decision**: Extend the existing `VSCodeExtension` class to become a more generic `IDEExtension` class that supports multiple IDEs through a provider pattern.

**Key Components**:

#### IDE Provider Interface
```python
class IDEProvider:
    def get_command(self) -> str
    def get_display_name(self) -> str
    def get_args(self, is_directory: bool) -> str
    def is_available(self) -> bool
```

#### Concrete Providers
- `VSCodeProvider`: Existing VSCode functionality
- `KiroProvider`: New Kiro functionality with similar behavior patterns

#### Enhanced Menu Provider
- Generate menu items dynamically based on available IDE providers
- Handle IDE availability checking
- Provide error handling for missing IDEs

## Data Models

### Configuration Model
```python
@dataclass
class IDEConfig:
    command: str
    display_name: str
    new_window_flag: str
    availability_check: callable
```

### Installation Configuration
```bash
# Environment variables for installation customization
WGET_FLAGS: Optional wget flags for download
DEFAULT_WGET_FLAGS: "-q" (quiet mode)
```

## Error Handling

### Installation Script Error Handling
1. **Invalid wget flags**: Display help message and exit with error code
2. **Network failures**: Retry with exponential backoff
3. **Permission errors**: Provide clear instructions for resolution
4. **Missing dependencies**: Attempt automatic installation where possible

### Extension Error Handling
1. **Missing IDE**: Display user-friendly notification via Nautilus
2. **File access errors**: Log errors and continue with available options
3. **Command execution failures**: Provide fallback behavior and error logging

### Error Recovery Strategies
- Graceful degradation when one IDE is unavailable
- Fallback to default wget behavior if custom flags fail
- Maintain existing functionality if new features encounter issues

## Testing Strategy

### Installation Script Testing
1. **Unit Tests**: Flag parsing and validation logic
2. **Integration Tests**: End-to-end installation with various flag combinations
3. **Compatibility Tests**: Verify backward compatibility with existing installations
4. **Error Scenario Tests**: Invalid flags, network failures, permission issues

### Extension Testing
1. **Functional Tests**: Menu item generation and IDE launching
2. **Availability Tests**: Behavior when IDEs are missing or unavailable
3. **File Selection Tests**: Various file and folder selection scenarios
4. **Error Handling Tests**: Invalid paths, permission issues, command failures

### Test Environment Setup
- Docker containers with different Linux distributions
- Mock IDE installations for testing availability detection
- Network simulation for testing installation scenarios
- File system permission testing scenarios

## Implementation Considerations

### Backward Compatibility
- Existing installations continue to work without modification
- Default behavior remains unchanged
- New features are additive, not replacing existing functionality

### Performance
- IDE availability checking should be cached to avoid repeated system calls
- Menu generation should be efficient for large file selections
- Installation script should minimize network requests

### Security
- Wget flag validation prevents injection attacks
- IDE command execution uses safe subprocess practices
- File path handling prevents directory traversal issues

### Maintainability
- Provider pattern allows easy addition of new IDEs in the future
- Configuration-driven approach reduces hardcoded values
- Clear separation of concerns between installation and runtime functionality