# code-nautilus

This repo provides Nautilus extensions for both Visual Studio Code and Kiro IDE integration. Right-click on any file or directory in Nautilus to open it directly in your preferred editor.

## Features

- **Open in Code**: Launch Visual Studio Code with selected files/directories
- **Open in Kiro**: Launch Kiro IDE with selected files/directories
- **Multiple Selection Support**: Open multiple files or directories at once
- **Background Context Menu**: Right-click in empty space to open current directory

## Prerequisites

Before installation, ensure you have the editors you want to use installed and available in your PATH:

- For VSCode integration: `code` command must be available
- For Kiro integration: `kiro` command must be available

## Features

```bash
wget -qO- https://raw.githubusercontent.com/harry-cpp/code-nautilus/master/install.sh | bash
```

The installation script will:
- Install required dependencies (`python-nautilus`)
- Copy the extension to the correct Nautilus directory
- Restart Nautilus to load the extension
- Verify that editor commands are available in PATH

## Uninstall Extension

```bash
rm -f ~/.local/share/nautilus-python/extensions/code-nautilus.py
```

After uninstalling, restart Nautilus:
```bash
nautilus -q && nautilus &
```

## Usage

1. Open Nautilus file manager
2. Navigate to any file or directory
3. Right-click to open the context menu
4. Select either:
   - **"Open in Code"** to launch Visual Studio Code
   - **"Open in Kiro"** to launch Kiro IDE

## Troubleshooting

### Extension not appearing in context menu

1. **Check if python-nautilus is installed:**
   ```bash
   # On Ubuntu/Debian
   sudo apt list --installed | grep python-nautilus
   
   # On Arch Linux
   pacman -Q python-nautilus
   
   # On Fedora
   rpm -qa | grep nautilus-python
   ```

2. **Verify extension file exists:**
   ```bash
   ls -la ~/.local/share/nautilus-python/extensions/code-nautilus.py
   ```

3. **Restart Nautilus:**
   ```bash
   nautilus -q && nautilus &
   ```

### "Open in Code" or "Open in Kiro" not working

1. **Check if the editor command is in PATH:**
   ```bash
   # For VSCode
   which code
   
   # For Kiro
   which kiro
   ```

2. **Test the command manually:**
   ```bash
   # For VSCode
   code /path/to/your/file
   
   # For Kiro
   kiro /path/to/your/file
   ```

3. **Install missing editors:**
   - **VSCode**: Follow instructions at https://code.visualstudio.com/docs/setup/linux
   - **Kiro**: Follow Kiro installation instructions for your system

### Permission issues

If you encounter permission errors during installation:

1. **Ensure extensions directory exists:**
   ```bash
   mkdir -p ~/.local/share/nautilus-python/extensions/
   ```

2. **Check directory permissions:**
   ```bash
   ls -la ~/.local/share/nautilus-python/
   ```

### Extension installed but menu items missing

1. **Check Python dependencies:**
   ```bash
   python3 -c "import gi; gi.require_version('Nautilus', '3.0'); from gi.repository import Nautilus"
   ```

2. **Verify extension syntax:**
   ```bash
   python3 -m py_compile ~/.local/share/nautilus-python/extensions/code-nautilus.py
   ```

3. **Check Nautilus logs:**
   ```bash
   journalctl --user -u nautilus --since "1 hour ago"
   ```

## Contributing

Feel free to submit issues and pull requests to improve the extension.
