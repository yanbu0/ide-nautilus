# VSCode and Kiro Nautilus Extension
#
# Place me in ~/.local/share/nautilus-python/extensions/,
# ensure you have python-nautilus package, restart Nautilus, and enjoy :)
#
# This script is released to the public domain.

from gi.repository import Nautilus, GObject
from subprocess import call, CalledProcessError, DEVNULL
import os
import shutil
import shlex

# path to vscode
VSCODE = 'code'

# path to kiro
KIRO = 'kiro'

# what name do you want to see in the context menu?
VSCODENAME = 'Code'
KIRONAME = 'Kiro'

# always create new window?
NEWWINDOW = False


class VSCodeKiroExtension(GObject.GObject, Nautilus.MenuProvider):

    def _is_command_available(self, command):
        """Check if a command is available in the system PATH"""
        return shutil.which(command) is not None

    def _quote_path(self, path):
        """Properly quote a file path to handle spaces and special characters"""
        return shlex.quote(path)

    def launch_vscode(self, menu, files):
        # Check if VSCode command is available
        if not self._is_command_available(VSCODE):
            return

        safepaths = ''
        args = ''

        for file in files:
            filepath = file.get_location().get_path()
            if filepath and os.path.exists(filepath):
                try:
                safepaths += self._quote_path(filepath) + ' '

                # If one of the files we are trying to open is a folder
                # create a new instance of vscode
                if os.path.isdir(filepath):
                    args = '--new-window '

                    # Check if any of the files is a directory
                    if os.path.isdir(filepath):
                        has_directory = True
                        
                except Exception as e:
                    invalid_paths.append(f"{filepath} (error: {str(e)})")
                    continue

        if safepaths.strip():  # Only execute if we have valid paths
            try:
                call(VSCODE + ' ' + args + safepaths + '&', shell=True)
            except (CalledProcessError, OSError):
                # Gracefully handle subprocess execution failures
                pass

    def launch_kiro(self, menu, files):
        # Check if Kiro command is available
        if not self._is_command_available(KIRO):
            return

        safepaths = ''

        for file in files:
            filepath = file.get_location().get_path()
            if filepath and os.path.exists(filepath):
                safepaths += self._quote_path(filepath) + ' '

        if safepaths.strip():  # Only execute if we have valid paths
            try:
                call(KIRO + ' ' + safepaths + '&', shell=True)
            except (CalledProcessError, OSError):
                # Gracefully handle subprocess execution failures
                pass

    def get_file_items(self, *args):
        """Generate menu items for file selection"""
        files = args[-1]
        items = []
        
        # VSCode menu item (only if command is available)
        if self._is_command_available(VSCODE):
            vscode_item = Nautilus.MenuItem(
                name='VSCodeOpen',
                label='Open in ' + VSCODENAME,
                tip='Opens the selected files with VSCode'
            )
            vscode_item.connect('activate', self.launch_vscode, files)
            items.append(vscode_item)
        
        # Kiro menu item (only if command is available)
        if self._is_command_available(KIRO):
            kiro_item = Nautilus.MenuItem(
                name='KiroOpen',
                label='Open in ' + KIRONAME,
                tip='Opens the selected files with Kiro'
            )
            kiro_item.connect('activate', self.launch_kiro, files)
            items.append(kiro_item)

        return items

    def get_background_items(self, *args):
        """Generate menu items for background (directory) context"""
        file_ = args[-1]
        items = []
        
        # VSCode menu item (only if command is available)
        if self._is_command_available(VSCODE):
            vscode_item = Nautilus.MenuItem(
                name='VSCodeOpenBackground',
                label='Open in ' + VSCODENAME,
                tip='Opens the current directory in VSCode'
            )
            vscode_item.connect('activate', self.launch_vscode, [file_])
            items.append(vscode_item)
        
        # Kiro menu item (only if command is available)
        if self._is_command_available(KIRO):
            kiro_item = Nautilus.MenuItem(
                name='KiroOpenBackground',
                label='Open in ' + KIRONAME,
                tip='Opens the current directory in Kiro'
            )
            kiro_item.connect('activate', self.launch_kiro, [file_])
            items.append(kiro_item)

        return items
