# code-nautilus

This repo provides IDE extensions for Nautilus file manager, supporting both Visual Studio Code and Kiro IDE. Right-click on files or folders in Nautilus to open them directly in your preferred IDE.

## Features

- **Dual IDE Support**: Open files and folders in both Visual Studio Code and Kiro IDE
- **Context Menu Integration**: Right-click context menu options for quick IDE access
- **Configurable Installation**: Customize wget behavior during installation
- **Backward Compatibility**: Existing installations continue to work without modification

## Requirements

### System Requirements
- Linux system with Nautilus file manager
- Python 3.x with nautilus-python extension support

### IDE Requirements
- **Visual Studio Code**: Install from [official website](https://code.visualstudio.com/) or package manager
- **Kiro IDE**: Install Kiro IDE for AI-powered development features (optional)

Both IDEs are detected automatically. If an IDE is not installed, its menu option will handle the error gracefully.

## Installation

### Quick Install (Default)
```bash
wget -qO- https://raw.githubusercontent.com/harry-cpp/code-nautilus/master/install.sh | bash
```

### Custom Installation with Wget Flags
You can customize the download behavior by specifying wget flags:

```bash
# Download and run with custom wget flags
wget -qO- https://raw.githubusercontent.com/harry-cpp/code-nautilus/master/install.sh | bash -s -- --wget-flags "-v --timeout=30"

# Or download the script first and run with flags
wget https://raw.githubusercontent.com/harry-cpp/code-nautilus/master/install.sh
chmod +x install.sh
./install.sh --wget-flags "-v --progress=bar"
```

### Installation Examples

**Verbose output with progress bar:**
```bash
./install.sh --wget-flags "-v --progress=bar"
```

**Custom timeout and retry settings:**
```bash
./install.sh --wget-flags "--timeout=60 --tries=3"
```

**Quiet installation (default behavior):**
```bash
./install.sh
# Equivalent to: ./install.sh --wget-flags "-q"
```

### Installation Help
```bash
./install.sh --help
```

## Usage

After installation, restart Nautilus or log out and back in. Then:

1. **Right-click** on any file or folder in Nautilus
2. Select **"Open in Code"** to open in Visual Studio Code
3. Select **"Open in Kiro"** to open in Kiro IDE (if installed)

### Supported Actions
- Open individual files in either IDE
- Open entire folders/directories as IDE workspaces
- Multiple file selection support
- Graceful error handling for missing IDEs

## Uninstall Extension

```bash
rm -f ~/.local/share/nautilus-python/extensions/code-nautilus.py
```

## Troubleshooting

### IDE Not Opening
- Ensure the IDE is properly installed and available in your system PATH
- Check that the IDE command (`code` for VSCode, `kiro` for Kiro) works in terminal
- Restart Nautilus after installation: `nautilus -q && nautilus &`

### Menu Items Not Appearing
- Verify nautilus-python is installed: `python3 -c "import gi; gi.require_version('Nautilus', '3.0')"`
- Check extension file exists: `ls ~/.local/share/nautilus-python/extensions/code-nautilus.py`
- Restart Nautilus or log out/in

### Installation Issues
- Ensure you have write permissions to `~/.local/share/nautilus-python/extensions/`
- Check network connectivity if wget fails
- Try installation with verbose flags: `./install.sh --wget-flags "-v"`
