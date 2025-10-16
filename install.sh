#!/bin/bash

# Function to check if a command is available in PATH
check_command() {
    if command -v "$1" >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Install python-nautilus
echo "Installing python-nautilus..."
if type "pacman" > /dev/null 2>&1
then
    # check if already install, else install
    pacman -Qi python-nautilus &> /dev/null
    if [ `echo $?` -eq 1 ]
    then
        sudo pacman -S --noconfirm python-nautilus
        if [ $? -eq 0 ]; then
            echo "✓ python-nautilus installed successfully"
        else
            echo "✗ Failed to install python-nautilus"
            exit 1
        fi
    else
        echo "✓ python-nautilus is already installed"
    fi
elif type "apt-get" > /dev/null 2>&1
then
    # Find Ubuntu python-nautilus package
    package_name="python-nautilus"
    found_package=$(apt-cache search --names-only $package_name)
    if [ -z "$found_package" ]
    then
        package_name="python3-nautilus"
    fi

    # Check if the package needs to be installed and install it
    installed=$(apt list --installed $package_name -qq 2> /dev/null)
    if [ -z "$installed" ]
    then
        sudo apt-get install -y $package_name
        if [ $? -eq 0 ]; then
            echo "✓ $package_name installed successfully"
        else
            echo "✗ Failed to install $package_name"
            exit 1
        fi
    else
        echo "✓ $package_name is already installed"
    fi
elif type "dnf" > /dev/null 2>&1
then
    installed=`dnf list --installed nautilus-python 2> /dev/null`
    if [ -z "$installed" ]
    then
        sudo dnf install -y nautilus-python
        if [ $? -eq 0 ]; then
            echo "✓ nautilus-python installed successfully"
        else
            echo "✗ Failed to install nautilus-python"
            exit 1
        fi
    else
        echo "✓ nautilus-python is already installed"
    fi
else
    echo "✗ Failed to find python-nautilus, please install it manually."
    exit 1
fi

# Check for VSCode and Kiro commands
echo ""
echo "Checking for editor commands..."
vscode_available=false
kiro_available=false

if check_command "code"; then
    echo "✓ VSCode command 'code' found in PATH"
    vscode_available=true
else
    echo "⚠ VSCode command 'code' not found in PATH"
fi

if check_command "kiro"; then
    echo "✓ Kiro command 'kiro' found in PATH"
    kiro_available=true
else
    echo "⚠ Kiro command 'kiro' not found in PATH"
fi

if [ "$vscode_available" = false ] && [ "$kiro_available" = false ]; then
    echo "✗ Neither VSCode nor Kiro commands are available. Please install at least one editor."
    exit 1
fi

# Remove previous versions and setup folder
echo ""
echo "Removing previous extensions (if found)..."
mkdir -p ~/.local/share/nautilus-python/extensions
rm -f ~/.local/share/nautilus-python/extensions/VSCodeExtension.py
rm -f ~/.local/share/nautilus-python/extensions/code-nautilus.py
rm -f ~/.local/share/nautilus-python/extensions/kiro-nautilus.py
echo "✓ Previous extensions removed"

echo ""
# Download and install the extension
echo "Downloading newest version..."
wget -q -O code-nautilus.py https://raw.githubusercontent.com/yanbu0/ide-nautilus/master/code-nautilus.py

# Install the enhanced extension
echo ""
echo "Installing enhanced VSCode+Kiro extension..."
if [ -f "code-nautilus.py" ]; then
    echo "Copying file..."
    cp code-nautilus.py ~/.local/share/nautilus-python/extensions/kiro-nautilus.py
    if [ $? -eq 0 ]; then
        echo "✓ Enhanced extension installed successfully"
    else
        echo "✗ Failed to install enhanced extension"
        exit 1
    fi
else
    echo "✗ Enhanced extension file 'code-nautilus.py' not found in current directory"
    exit 1
fi

# Restart nautilus
echo ""
echo "Restarting Nautilus..."
nautilus -q
if [ $? -eq 0 ]; then
    echo "✓ Nautilus restarted successfully"
else
    echo "⚠ Failed to restart Nautilus - you may need to restart it manually"
fi

echo ""
echo "=== Installation Complete ==="
echo ""
echo "Available features:"
if [ "$vscode_available" = true ]; then
    echo "  ✓ Open in VSCode (right-click context menu)"
fi
if [ "$kiro_available" = true ]; then
    echo "  ✓ Open in Kiro (right-click context menu)"
fi
echo ""
echo "The extension will automatically detect which editors are available"
echo "and show the appropriate menu items in Nautilus."
