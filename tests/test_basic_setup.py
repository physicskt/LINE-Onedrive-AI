"""
Basic test for LINE OneDrive AI system
"""
import unittest
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import config


class TestBasicSetup(unittest.TestCase):
    """Test basic setup and configuration"""
    
    def test_config_exists(self):
        """Test that config module loads properly"""
        self.assertIsNotNone(config)
        self.assertTrue(hasattr(config, 'BASE_DIR'))
        self.assertTrue(hasattr(config, 'LOGS_DIR'))
    
    def test_logs_directory_exists(self):
        """Test that logs directory is created"""
        self.assertTrue(config.LOGS_DIR.exists())
        self.assertTrue(config.LOGS_DIR.is_dir())
    
    def test_modules_can_import(self):
        """Test that core modules can be imported"""
        try:
            from modules.utils.logger import setup_logging, StructuredLogger
            from modules.line_bot.bot_handler import LineBotHandler
            from modules.onedrive.client import OneDriveClient
            from modules.ai.assistant import AIAssistant
        except ImportError as e:
            self.fail(f"Failed to import modules: {e}")
    
    def test_log_config_generation(self):
        """Test that log configuration can be generated"""
        log_config = config.get_log_config()
        self.assertIsInstance(log_config, dict)
        self.assertIn('handlers', log_config)
        self.assertIn('loggers', log_config)


if __name__ == '__main__':
    unittest.main()