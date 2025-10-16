# VSCode Nautilus Extension
#
# Place me in ~/.local/share/nautilus-python/extensions/,
# ensure you have python-nautilus package, restart Nautilus, and enjoy :)
#
# This script is released to the public domain.

from gi.repository import Nautilus, GObject
from subprocess import call
import os
import subprocess
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

# path to vscode
VSCODE = 'code'

# what name do you want to see in the context menu?
VSCODENAME = 'Code'

# always create new window?
NEWWINDOW = False


@dataclass
class IDEConfig:
    """Configuration data class for IDE settings"""
    command: str
    display_name: str
    new_window_flag: str
    availability_check: callable


class IDEProvider(ABC):
    """Abstract base class for IDE providers"""
    
    @abstractmethod
    def get_command(self) -> str:
        """Return the command to launch the IDE"""
        pass
    
    @abstractmethod
    def get_display_name(self) -> str:
        """Return the display name for menu items"""
        pass
    
    @abstractmethod
    def get_args(self, is_directory: bool) -> str:
        """Return command arguments based on whether target is a directory"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the IDE is available on the system"""
        pass


class VSCodeProvider(IDEProvider):
    """Provider for Visual Studio Code IDE"""
    
    def get_command(self) -> str:
        return VSCODE
    
    def get_display_name(self) -> str:
        return VSCODENAME
    
    def get_args(self, is_directory: bool) -> str:
        if NEWWINDOW or is_directory:
            return '--new-window '
        return ''
    
    def is_available(self) -> bool:
        """Check if VSCode is available by trying to find it in PATH"""
        try:
            from shutil import which
            result = which(VSCODE) is not None
            if result:
                # Double-check by trying to get version info
                try:
                    subprocess.run([VSCODE, '--version'], capture_output=True, timeout=3, check=True)
                    return True
                except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
                    return False
            return result
        except ImportError:
            # Fallback for older Python versions
            try:
                subprocess.check_output(['which', VSCODE], stderr=subprocess.DEVNULL)
                # Try to run the command to verify it's actually executable
                subprocess.run([VSCODE, '--version'], capture_output=True, timeout=3, check=True)
                return True
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
                return False


class KiroProvider(IDEProvider):
    """Provider for Kiro IDE"""
    
    def get_command(self) -> str:
        return 'kiro'
    
    def get_display_name(self) -> str:
        return 'Kiro'
    
    def get_args(self, is_directory: bool) -> str:
        # Kiro creates new windows for directories by default
        if is_directory:
            return ''
        return ''
    
    def is_available(self) -> bool:
        """Check if Kiro is available by trying to find it in PATH"""
        try:
            from shutil import which
            result = which('kiro') is not None
            if result:
                # Double-check by trying to get version info or help
                try:
                    # Try version first, then help if version fails
                    try:
                        subprocess.run(['kiro', '--version'], capture_output=True, timeout=3, check=True)
                        return True
                    except subprocess.CalledProcessError:
                        # Some programs don't support --version, try --help
                        subprocess.run(['kiro', '--help'], capture_output=True, timeout=3, check=True)
                        return True
                except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
                    return False
            return result
        except ImportError:
            # Fallback for older Python versions
            try:
                subprocess.check_output(['which', 'kiro'], stderr=subprocess.DEVNULL)
                # Try to run the command to verify it's actually executable
                try:
                    subprocess.run(['kiro', '--version'], capture_output=True, timeout=3, check=True)
                    return True
                except subprocess.CalledProcessError:
                    # Try help if version fails
                    subprocess.run(['kiro', '--help'], capture_output=True, timeout=3, check=True)
                    return True
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
                return False


class VSCodeExtension(GObject.GObject, Nautilus.MenuProvider):
    """Enhanced Nautilus extension supporting multiple IDEs"""
    
    def __init__(self):
        super().__init__()
        # Initialize available IDE providers
        self.providers = [
            VSCodeProvider(),
            KiroProvider()
        ]
        # Filter to only available providers
        self.available_providers = [p for p in self.providers if p.is_available()]

    def launch_ide(self, menu, files, provider):
        """Launch the specified IDE with the given files"""
        try:
            # Double-check availability before launching
            if not provider.is_available():
                error_msg = f"{provider.get_display_name()} is not available on this system. Please install {provider.get_display_name()} to use this feature."
                self._show_error_notification(error_msg)
                return

            safepaths = ''
            has_directory = False
            invalid_paths = []

            # Validate file paths and build command
            for file in files:
                try:
                    filepath = file.get_location().get_path()
                    
                    # Check if path exists and is accessible
                    if not os.path.exists(filepath):
                        invalid_paths.append(filepath)
                        continue
                    
                    # Check if we have read permissions
                    if not os.access(filepath, os.R_OK):
                        invalid_paths.append(f"{filepath} (no read permission)")
                        continue
                    
                    safepaths += '"' + filepath + '" '

                    # Check if any of the files is a directory
                    if os.path.isdir(filepath):
                        has_directory = True
                        
                except Exception as e:
                    invalid_paths.append(f"{filepath} (error: {str(e)})")
                    continue

            # Handle invalid paths
            if invalid_paths:
                if len(invalid_paths) == len(files):
                    # All paths are invalid
                    self._show_error_notification("Cannot open selected items: all paths are invalid or inaccessible")
                    return
                else:
                    # Some paths are invalid, warn user but continue with valid ones
                    invalid_list = ", ".join(invalid_paths[:3])  # Show first 3 invalid paths
                    if len(invalid_paths) > 3:
                        invalid_list += f" and {len(invalid_paths) - 3} more"
                    self._show_info_notification(f"Skipping invalid paths: {invalid_list}")

            # If no valid paths remain, don't launch
            if not safepaths.strip():
                self._show_error_notification("No valid files or folders to open")
                return

            # Get appropriate arguments from provider
            args = provider.get_args(has_directory)
            command = provider.get_command() + ' ' + args + safepaths + '&'
            
            # Execute command with better error handling
            result = call(command, shell=True)
            
            # Check if command execution failed
            if result != 0:
                fallback_msg = self._attempt_fallback_launch(provider, safepaths, has_directory)
                if not fallback_msg:
                    self._show_error_notification(f"Failed to launch {provider.get_display_name()}. Please check if it's properly installed and accessible.")
            
        except Exception as e:
            # Handle unexpected errors gracefully with detailed user notification
            error_msg = f"Unexpected error launching {provider.get_display_name()}: {str(e)}"
            self._show_error_notification(error_msg)
            print(f"DEBUG: {error_msg}")  # For debugging purposes

    def _show_error_notification(self, message):
        """Show error notification to user via system notification"""
        try:
            # Try to use notify-send for user notification
            call(['notify-send', 'Nautilus Extension Error', message])
        except Exception as e:
            # Fallback to console output if notify-send is not available
            print(f"Nautilus Extension Error: {message}")
            print(f"Notification system error: {e}")
    
    def _show_info_notification(self, message):
        """Show informational notification to user"""
        try:
            call(['notify-send', 'Nautilus Extension', message])
        except Exception as e:
            print(f"Nautilus Extension Info: {message}")
            print(f"Notification system error: {e}")
    
    def _attempt_fallback_launch(self, provider, safepaths, has_directory):
        """Attempt fallback launch strategies when primary launch fails"""
        try:
            # Try launching without the background flag (&)
            args = provider.get_args(has_directory)
            command = provider.get_command() + ' ' + args + safepaths
            
            import subprocess
            result = subprocess.run(command, shell=True, capture_output=True, timeout=5)
            
            if result.returncode == 0:
                self._show_info_notification(f"Successfully launched {provider.get_display_name()} using fallback method")
                return True
            else:
                # Log the error for debugging
                error_output = result.stderr.decode() if result.stderr else "No error output"
                print(f"DEBUG: Fallback launch failed for {provider.get_display_name()}: {error_output}")
                return False
                
        except subprocess.TimeoutExpired:
            # Command took too long, but might have succeeded
            self._show_info_notification(f"Launched {provider.get_display_name()} (startup took longer than expected)")
            return True
        except Exception as e:
            print(f"DEBUG: Fallback launch exception for {provider.get_display_name()}: {e}")
            return False
    
    def _show_no_ides_message(self, menu):
        """Show message when no IDEs are available"""
        self._show_info_notification("No supported IDEs (VSCode or Kiro) found on this system. Please install at least one IDE to use this feature.")

    def get_file_items(self, *args):
        """Generate menu items for file selection"""
        files = args[-1]
        items = []
        
        try:
            # Refresh available providers in case IDE availability changed
            self.available_providers = [p for p in self.providers if p.is_available()]
            
            # Always show menu items for all providers, but handle unavailable ones gracefully
            for provider in self.providers:
                try:
                    is_available = provider.is_available()
                    label = f'Open in {provider.get_display_name()}'
                    tip = f'Opens the selected files with {provider.get_display_name()}'
                    
                    if not is_available:
                        label += ' (Not Available)'
                        tip += ' - IDE not found on system'
                    
                    item = Nautilus.MenuItem(
                        name=f'{provider.get_display_name()}Open',
                        label=label,
                        tip=tip
                    )
                    item.connect('activate', self.launch_ide, files, provider)
                    items.append(item)
                    
                except Exception as e:
                    # Handle menu item creation errors gracefully
                    print(f"Error creating menu item for {provider.get_display_name()}: {e}")
                    # Continue with other providers
                    continue
            
            # If no items were created successfully, create a fallback info item
            if not items:
                try:
                    item = Nautilus.MenuItem(
                        name='NoIDEsAvailable',
                        label='No IDEs Available',
                        tip='No supported IDEs found on this system'
                    )
                    # Connect to a no-op function that shows an info message
                    item.connect('activate', self._show_no_ides_message)
                    items.append(item)
                except Exception as e:
                    print(f"Error creating fallback menu item: {e}")
                    
        except Exception as e:
            print(f"Error in get_file_items: {e}")
            # Return empty list on critical error
            return []

        return items

    def get_background_items(self, *args):
        """Generate menu items for background (directory) context"""
        file_ = args[-1]
        items = []
        
        try:
            # Refresh available providers in case IDE availability changed
            self.available_providers = [p for p in self.providers if p.is_available()]
            
            # Always show menu items for all providers, but handle unavailable ones gracefully
            for provider in self.providers:
                try:
                    is_available = provider.is_available()
                    label = f'Open in {provider.get_display_name()}'
                    tip = f'Opens the current directory in {provider.get_display_name()}'
                    
                    if not is_available:
                        label += ' (Not Available)'
                        tip += ' - IDE not found on system'
                    
                    item = Nautilus.MenuItem(
                        name=f'{provider.get_display_name()}OpenBackground',
                        label=label,
                        tip=tip
                    )
                    item.connect('activate', self.launch_ide, [file_], provider)
                    items.append(item)
                    
                except Exception as e:
                    # Handle menu item creation errors gracefully
                    print(f"Error creating background menu item for {provider.get_display_name()}: {e}")
                    # Continue with other providers
                    continue
            
            # If no items were created successfully, create a fallback info item
            if not items:
                try:
                    item = Nautilus.MenuItem(
                        name='NoIDEsAvailableBackground',
                        label='No IDEs Available',
                        tip='No supported IDEs found on this system'
                    )
                    # Connect to a no-op function that shows an info message
                    item.connect('activate', self._show_no_ides_message)
                    items.append(item)
                except Exception as e:
                    print(f"Error creating fallback background menu item: {e}")
                    
        except Exception as e:
            print(f"Error in get_background_items: {e}")
            # Return empty list on critical error
            return []

        return items
