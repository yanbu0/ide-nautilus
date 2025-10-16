#!/bin/bash

# Default wget flags
DEFAULT_WGET_FLAGS="-q"
WGET_FLAGS="$DEFAULT_WGET_FLAGS"

# Function to display help
show_help() {
    cat << EOF
Usage: $0 [OPTIONS]

Install code-nautilus extension for Nautilus file manager with VSCode and Kiro support.

OPTIONS:
    --wget-flags "FLAGS"    Specify custom wget flags for downloading the extension
                           Example: --wget-flags "-v --timeout=30"
                           Default: "-q" (quiet mode)
    -h, --help             Display this help message

EXAMPLES:
    $0                                    # Install with default settings
    $0 --wget-flags "-v"                 # Install with verbose wget output
    $0 --wget-flags "--timeout=30 -q"    # Install with custom timeout and quiet mode

NOTES:
    - The script maintains backward compatibility when no flags are specified
    - Only safe wget flags are allowed for security reasons
    - Unsafe flags like --output-document with system paths are blocked

EOF
}

# Function to validate wget flags
validate_wget_flags() {
    local flags="$1"
    
    # Check for potentially unsafe flags
    if echo "$flags" | grep -qE "(--output-document=/|--output-document ~/|--output-document /tmp)"; then
        echo "Error: Unsafe wget flag detected in: $flags"
        echo "Output redirection to system directories is not allowed for security reasons."
        echo "Use --help for more information about safe wget flags."
        return 1
    fi
    
    if echo "$flags" | grep -qE "(--directory-prefix=/|--directory-prefix ~/|--directory-prefix /tmp)"; then
        echo "Error: Unsafe wget flag detected in: $flags"
        echo "Directory prefix to system directories is not allowed for security reasons."
        echo "Use --help for more information about safe wget flags."
        return 1
    fi
    
    if echo "$flags" | grep -qE "(--input-file|--force-html|--base|--config)"; then
        echo "Error: Unsafe wget flag detected in: $flags"
        echo "File input/output and configuration flags are not allowed for security reasons."
        echo "Use --help for more information about safe wget flags."
        return 1
    fi
    
    if echo "$flags" | grep -qE "(--execute|--post-data|--post-file)"; then
        echo "Error: Unsafe wget flag detected in: $flags"
        echo "Code execution and POST data flags are not allowed for security reasons."
        echo "Use --help for more information about safe wget flags."
        return 1
    fi
    
    if echo "$flags" | grep -qE "(--load-cookies|--save-cookies|--certificate|--private-key)"; then
        echo "Error: Unsafe wget flag detected in: $flags"
        echo "Cookie and certificate handling flags are not allowed for security reasons."
        echo "Use --help for more information about safe wget flags."
        return 1
    fi
    
    # Check if flags start with dash (basic validation)
    if [[ -n "$flags" && ! "$flags" =~ ^[[:space:]]*- ]]; then
        echo "Error: wget flags must start with '-' or '--'"
        echo "Example: --wget-flags \"-v --timeout=30\""
        return 1
    fi
    
    return 0
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --wget-flags)
            if [[ -n "$2" ]]; then
                if validate_wget_flags "$2"; then
                    WGET_FLAGS="$2"
                else
                    exit 1
                fi
                shift 2
            else
                echo "Error: --wget-flags requires a value"
                echo "Use --help for usage information"
                exit 1
            fi
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Error: Unknown option $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Install python-nautilus
echo "Installing python-nautilus..."
if type "pacman" > /dev/null 2>&1
then
    # check if already install, else install
    pacman -Qi python-nautilus &> /dev/null
    if [ `echo $?` -eq 1 ]
    then
        sudo pacman -S --noconfirm python-nautilus
    else
        echo "python-nautilus is already installed"
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
    else
        echo "$package_name is already installed."
    fi
elif type "dnf" > /dev/null 2>&1
then
    installed=`dnf list --installed nautilus-python 2> /dev/null`
    if [ -z "$installed" ]
    then
        sudo dnf install -y nautilus-python
    else
        echo "nautilus-python is already installed."
    fi
else
    echo "Failed to find python-nautilus, please install it manually."
fi

# Remove previous version and setup folder
echo "Removing previous version (if found)..."
mkdir -p ~/.local/share/nautilus-python/extensions
rm -f ~/.local/share/nautilus-python/extensions/VSCodeExtension.py
rm -f ~/.local/share/nautilus-python/extensions/code-nautilus.py

# Download and install the extension
echo "Downloading newest version..."
echo "Using wget flags: $WGET_FLAGS"
wget $WGET_FLAGS -O ~/.local/share/nautilus-python/extensions/code-nautilus.py https://raw.githubusercontent.com/harry-cpp/code-nautilus/master/code-nautilus.py

# Restart nautilus
echo "Restarting nautilus..."
nautilus -q

echo "Installation Complete"
