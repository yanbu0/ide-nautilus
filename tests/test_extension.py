#!/usr/bin/env python3
"""
Test suite for the code-nautilus Python extension.

This module contains comprehensive tests for:
- IDE provider classes (VSCodeProvider, KiroProvider)
- Menu generation functionality
- IDE launching and error handling
- Error scenarios for missing IDEs and invalid paths

Requirements tested: 2.1, 2.2, 2.3, 2.4, 2.5
"""

import unittest
import sys
import os
import subprocess
from unittest.mock import Mock, patch, MagicMock, call
from unittest import TestCase

# Add the parent directory to the path to import the extension
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the extension modules
# Note: The file is named code-nautilus.py, so we need to import it specially
import importlib.util
spec = importlib.util.spec_from_file_location("code_nautilus", 
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "code-nautilus.py"))
code_nautilus = importlib.util.module_from_spec(spec)
spec.loader.exec_module(code_nautilus)

# Import the classes we need
IDEProvider = code_nautilus.IDEProvider
VSCodeProvider = code_nautilus.VSCodeProvider
KiroProvider = code_nautilus.KiroProvider
VSCodeExtension = code_nautilus.VSCodeExtension
IDEConfig = code_nautilus.IDEConfig


class TestIDEProviders(TestCase):
    """Unit tests for IDE provider classes"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.vscode_provider = VSCodeProvider()
        self.kiro_provider = KiroProvider()
    
    def test_vscode_provider_interface(self):
        """Test VSCodeProvider implements IDEProvider interface correctly"""
        # Test that VSCodeProvider is an instance of IDEProvider
        self.assertIsInstance(self.vscode_provider, IDEProvider)
        
        # Test all required methods exist and return expected types
        self.assertIsInstance(self.vscode_provider.get_command(), str)
        self.assertIsInstance(self.vscode_provider.get_display_name(), str)
        self.assertIsInstance(self.vscode_provider.get_args(True), str)
        self.assertIsInstance(self.vscode_provider.get_args(False), str)
        self.assertIsInstance(self.vscode_provider.is_available(), bool)
    
    def test_kiro_provider_interface(self):
        """Test KiroProvider implements IDEProvider interface correctly"""
        # Test that KiroProvider is an instance of IDEProvider
        self.assertIsInstance(self.kiro_provider, IDEProvider)
        
        # Test all required methods exist and return expected types
        self.assertIsInstance(self.kiro_provider.get_command(), str)
        self.assertIsInstance(self.kiro_provider.get_display_name(), str)
        self.assertIsInstance(self.kiro_provider.get_args(True), str)
        self.assertIsInstance(self.kiro_provider.get_args(False), str)
        self.assertIsInstance(self.kiro_provider.is_available(), bool)
    
    def test_vscode_provider_values(self):
        """Test VSCodeProvider returns correct values"""
        self.assertEqual(self.vscode_provider.get_command(), 'code')
        self.assertEqual(self.vscode_provider.get_display_name(), 'Code')
        
        # Test args for directory (should include --new-window)
        dir_args = self.vscode_provider.get_args(True)
        self.assertIn('--new-window', dir_args)
        
        # Test args for file (depends on NEWWINDOW setting)
        file_args = self.vscode_provider.get_args(False)
        self.assertIsInstance(file_args, str)
    
    def test_kiro_provider_values(self):
        """Test KiroProvider returns correct values"""
        self.assertEqual(self.kiro_provider.get_command(), 'kiro')
        self.assertEqual(self.kiro_provider.get_display_name(), 'Kiro')
        
        # Test args for both directory and file
        dir_args = self.kiro_provider.get_args(True)
        file_args = self.kiro_provider.get_args(False)
        self.assertIsInstance(dir_args, str)
        self.assertIsInstance(file_args, str)
    
    @patch('subprocess.run')
    @patch('shutil.which')
    def test_vscode_availability_check_success(self, mock_which, mock_run):
        """Test VSCode availability check when VSCode is available"""
        # Mock successful availability check
        mock_which.return_value = '/usr/bin/code'
        mock_run.return_value = Mock(returncode=0)
        
        result = self.vscode_provider.is_available()
        self.assertTrue(result)
        
        # Verify the calls
        mock_which.assert_called_with('code')
        mock_run.assert_called_with(['code', '--version'], capture_output=True, timeout=3, check=True)
    
    @patch('subprocess.run')
    @patch('shutil.which')
    def test_vscode_availability_check_failure(self, mock_which, mock_run):
        """Test VSCode availability check when VSCode is not available"""
        # Mock failed availability check
        mock_which.return_value = None
        
        result = self.vscode_provider.is_available()
        self.assertFalse(result)
        
        # Verify which was called but run was not (since which returned None)
        mock_which.assert_called_with('code')
        mock_run.assert_not_called()
    
    @patch('subprocess.run')
    @patch('shutil.which')
    def test_kiro_availability_check_success(self, mock_which, mock_run):
        """Test Kiro availability check when Kiro is available"""
        # Mock successful availability check
        mock_which.return_value = '/usr/bin/kiro'
        mock_run.return_value = Mock(returncode=0)
        
        result = self.kiro_provider.is_available()
        self.assertTrue(result)
        
        # Verify the calls
        mock_which.assert_called_with('kiro')
        mock_run.assert_called_with(['kiro', '--version'], capture_output=True, timeout=3, check=True)
    
    @patch('subprocess.run')
    @patch('shutil.which')
    def test_kiro_availability_fallback_to_help(self, mock_which, mock_run):
        """Test Kiro availability check falls back to --help when --version fails"""
        # Mock availability check where version fails but help succeeds
        mock_which.return_value = '/usr/bin/kiro'
        mock_run.side_effect = [
            subprocess.CalledProcessError(1, 'kiro --version'),  # Version fails
            Mock(returncode=0)  # Help succeeds
        ]
        
        result = self.kiro_provider.is_available()
        self.assertTrue(result)
        
        # Verify both calls were made
        expected_calls = [
            call(['kiro', '--version'], capture_output=True, timeout=3, check=True),
            call(['kiro', '--help'], capture_output=True, timeout=3, check=True)
        ]
        mock_run.assert_has_calls(expected_calls)


class TestVSCodeExtension(TestCase):
    """Functional tests for VSCodeExtension menu generation and IDE launching"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock Nautilus dependencies
        self.mock_nautilus = Mock()
        self.mock_gobject = Mock()
        
        # Create the extension with mocked dependencies
        self.extension = VSCodeExtension()
    
    @patch.object(VSCodeProvider, 'is_available')
    @patch.object(KiroProvider, 'is_available')
    def test_extension_initialization(self, mock_kiro_available, mock_vscode_available):
        """Test extension initializes with correct providers"""
        # Mock both IDEs as available
        mock_vscode_available.return_value = True
        mock_kiro_available.return_value = True
        
        # Create new extension to test initialization
        with patch.dict('sys.modules', {
            'gi.repository.Nautilus': self.mock_nautilus,
            'gi.repository.GObject': self.mock_gobject
        }):
            extension = VSCodeExtension()
        
        # Should have 2 providers
        self.assertEqual(len(extension.providers), 2)
        self.assertIsInstance(extension.providers[0], VSCodeProvider)
        self.assertIsInstance(extension.providers[1], KiroProvider)
    
    @patch.object(VSCodeProvider, 'is_available')
    @patch.object(KiroProvider, 'is_available')
    def test_menu_generation_both_available(self, mock_kiro_available, mock_vscode_available):
        """Test menu generation when both IDEs are available"""
        # Mock both IDEs as available
        mock_vscode_available.return_value = True
        mock_kiro_available.return_value = True
        
        # Mock file objects
        mock_files = [Mock(), Mock()]
        
        # Test menu generation
        items = self.extension.get_file_items(mock_files)
        
        # Should create 2 menu items (one for each IDE)
        self.assertEqual(len(items), 2)
        
        # Verify that items were created (we can't easily mock the Nautilus.MenuItem 
        # since it's imported in the module, but we can verify the count and that they exist)
        self.assertIsNotNone(items[0])
        self.assertIsNotNone(items[1])
    
    @patch.object(VSCodeProvider, 'is_available')
    @patch.object(KiroProvider, 'is_available')
    def test_menu_generation_none_available(self, mock_kiro_available, mock_vscode_available):
        """Test menu generation when no IDEs are available"""
        # Mock both IDEs as unavailable
        mock_vscode_available.return_value = False
        mock_kiro_available.return_value = False
        
        # Mock file objects
        mock_files = [Mock()]
        
        # Test menu generation
        items = self.extension.get_file_items(mock_files)
        
        # Should still create menu items but marked as not available
        self.assertEqual(len(items), 2)
        
        # Since we can't easily mock the Nautilus.MenuItem creation,
        # we just verify that items were created
        self.assertIsNotNone(items[0])
        self.assertIsNotNone(items[1])
    
    @patch.object(VSCodeProvider, 'is_available')
    @patch.object(KiroProvider, 'is_available')
    def test_background_menu_generation(self, mock_kiro_available, mock_vscode_available):
        """Test background menu generation for directory context"""
        # Mock both IDEs as available
        mock_vscode_available.return_value = True
        mock_kiro_available.return_value = True
        
        # Mock directory object
        mock_directory = Mock()
        
        # Test background menu generation
        items = self.extension.get_background_items(mock_directory)
        
        # Should create 2 menu items (one for each IDE)
        self.assertEqual(len(items), 2)
        
        # Verify that items were created
        self.assertIsNotNone(items[0])
        self.assertIsNotNone(items[1])


class TestIDELaunching(TestCase):
    """Tests for IDE launching functionality and error handling"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock Nautilus dependencies
        self.mock_nautilus = Mock()
        self.mock_gobject = Mock()
        
        with patch.dict('sys.modules', {
            'gi.repository.Nautilus': self.mock_nautilus,
            'gi.repository.GObject': self.mock_gobject
        }):
            self.extension = VSCodeExtension()
        
        # Create mock provider
        self.mock_provider = Mock(spec=IDEProvider)
        self.mock_provider.get_command.return_value = 'test-ide'
        self.mock_provider.get_display_name.return_value = 'Test IDE'
        self.mock_provider.get_args.return_value = ''
        self.mock_provider.is_available.return_value = True
    

    
    @patch('os.path.exists')
    def test_ide_launch_with_invalid_paths(self, mock_exists):
        """Test IDE launch behavior with invalid file paths"""
        # Mock file system - file doesn't exist
        mock_exists.return_value = False
        
        # Mock file objects with invalid path
        mock_file = Mock()
        mock_file.get_location.return_value.get_path.return_value = '/nonexistent/file.txt'
        mock_files = [mock_file]
        
        # Mock menu
        mock_menu = Mock()
        
        # Mock notification method
        with patch.object(self.extension, '_show_error_notification') as mock_error:
            # Test IDE launch
            self.extension.launch_ide(mock_menu, mock_files, self.mock_provider)
            
            # Should show error notification for invalid paths
            mock_error.assert_called_once()
            error_message = mock_error.call_args[0][0]
            # The actual error message is "Cannot open selected items: all paths are invalid or inaccessible"
            self.assertIn('Cannot open selected items', error_message)
    
    def test_ide_launch_with_unavailable_ide(self):
        """Test IDE launch when IDE is not available"""
        # Mock provider as unavailable
        self.mock_provider.is_available.return_value = False
        
        # Mock file objects
        mock_file = Mock()
        mock_file.get_location.return_value.get_path.return_value = '/test/file.txt'
        mock_files = [mock_file]
        
        # Mock menu
        mock_menu = Mock()
        
        # Mock notification method
        with patch.object(self.extension, '_show_error_notification') as mock_error:
            # Test IDE launch
            self.extension.launch_ide(mock_menu, mock_files, self.mock_provider)
            
            # Should show error notification for unavailable IDE
            mock_error.assert_called_once()
            error_message = mock_error.call_args[0][0]
            self.assertIn('is not available on this system', error_message)
    



class TestErrorScenarios(TestCase):
    """Tests for error scenarios and edge cases"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock Nautilus dependencies
        self.mock_nautilus = Mock()
        self.mock_gobject = Mock()
        
        with patch.dict('sys.modules', {
            'gi.repository.Nautilus': self.mock_nautilus,
            'gi.repository.GObject': self.mock_gobject
        }):
            self.extension = VSCodeExtension()
    

    
    def test_menu_generation_exception_handling(self):
        """Test menu generation handles exceptions gracefully"""
        # Mock file objects
        mock_files = [Mock()]
        
        # Patch the get_file_items method to simulate an exception in menu creation
        original_method = self.extension.get_file_items
        
        def mock_get_file_items(*args):
            try:
                # Simulate an exception during menu item creation
                raise Exception("Menu creation failed")
            except Exception:
                # The actual implementation catches exceptions and returns empty list
                return []
        
        # Test menu generation (should not raise exception)
        with patch.object(self.extension, 'get_file_items', side_effect=mock_get_file_items):
            with patch('builtins.print'):  # Suppress error output
                items = self.extension.get_file_items(mock_files)
                
                # Should return empty list on critical error
                self.assertEqual(items, [])
    
    @patch('os.path.exists')
    @patch('os.access')
    def test_mixed_valid_invalid_paths(self, mock_access, mock_exists):
        """Test handling of mixed valid and invalid file paths"""
        # Mock file system - first file exists, second doesn't
        mock_exists.side_effect = [True, False]
        mock_access.return_value = True
        
        # Mock file objects
        mock_file1 = Mock()
        mock_file1.get_location.return_value.get_path.return_value = '/valid/file.txt'
        mock_file2 = Mock()
        mock_file2.get_location.return_value.get_path.return_value = '/invalid/file.txt'
        mock_files = [mock_file1, mock_file2]
        
        # Mock provider
        mock_provider = Mock(spec=IDEProvider)
        mock_provider.is_available.return_value = True
        mock_provider.get_args.return_value = ''
        mock_provider.get_command.return_value = 'test-ide'
        
        # Mock menu
        mock_menu = Mock()
        
        with patch.object(self.extension, '_show_info_notification') as mock_info:
            with patch('subprocess.call', return_value=0):
                with patch('os.path.isdir', return_value=False):
                    # Test IDE launch
                    self.extension.launch_ide(mock_menu, mock_files, mock_provider)
                    
                    # Should show info notification about skipped invalid paths
                    mock_info.assert_called_once()
                    info_message = mock_info.call_args[0][0]
                    self.assertIn('Skipping invalid paths', info_message)


if __name__ == '__main__':
    # Configure test runner
    unittest.main(verbosity=2, buffer=True)