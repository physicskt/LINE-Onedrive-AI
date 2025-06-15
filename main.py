"""
LINE BOT × OneDrive AI Business Support System
Main application entry point
"""
import logging
import logging.config
import traceback
import sys
from pathlib import Path

# Import configuration
from config import config

# Import modules
from modules.utils.logger import setup_logging, log_error_with_traceback
from modules.line_bot.bot_handler import LineBotHandler
from modules.onedrive.client import OneDriveClient
from modules.ai.assistant import AIAssistant


class LineOneDriveAIApp:
    """Main application class"""
    
    def __init__(self):
        """Initialize the application"""
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        
        # Validate configuration
        if not config.validate_config():
            self.logger.error("Configuration validation failed. Exiting.")
            sys.exit(1)
        
        self.logger.info("LINE BOT × OneDrive AI System starting...")
        
        # Initialize components
        self.line_bot_handler = None
        self.onedrive_client = None
        self.ai_assistant = None
        
        self.initialize_components()
    
    def setup_logging(self):
        """Setup logging configuration"""
        try:
            setup_logging()
            self.logger = logging.getLogger(__name__)
            self.logger.info("Logging system initialized")
        except Exception as e:
            print(f"Failed to setup logging: {e}")
            sys.exit(1)
    
    def initialize_components(self):
        """Initialize all system components"""
        try:
            # Initialize LINE Bot Handler
            self.logger.info("Initializing LINE Bot Handler...")
            self.line_bot_handler = LineBotHandler()
            
            # Initialize OneDrive Client
            self.logger.info("Initializing OneDrive Client...")
            self.onedrive_client = OneDriveClient()
            
            # Initialize AI Assistant
            self.logger.info("Initializing AI Assistant...")
            self.ai_assistant = AIAssistant()
            
            self.logger.info("All components initialized successfully")
            
        except Exception as e:
            log_error_with_traceback(self.logger, "Failed to initialize components", e)
            sys.exit(1)
    
    def run(self):
        """Run the main application"""
        try:
            self.logger.info(f"Starting application on port {config.PORT}")
            
            # Start the web server for LINE webhook
            self.line_bot_handler.start_server(port=config.PORT)
            
        except KeyboardInterrupt:
            self.logger.info("Application stopped by user")
        except Exception as e:
            log_error_with_traceback(self.logger, "Application error", e)
        finally:
            self.shutdown()
    
    def shutdown(self):
        """Cleanup and shutdown"""
        try:
            self.logger.info("Shutting down application...")
            
            # Cleanup components
            if self.onedrive_client:
                self.onedrive_client.cleanup()
            
            if self.ai_assistant:
                self.ai_assistant.cleanup()
            
            self.logger.info("Application shutdown complete")
            
        except Exception as e:
            log_error_with_traceback(self.logger, "Error during shutdown", e)


def main():
    """Main entry point"""
    try:
        app = LineOneDriveAIApp()
        app.run()
    except Exception as e:
        # Emergency logging if main setup fails
        print(f"Critical error: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)


if __name__ == "__main__":
    main()