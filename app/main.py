import sys
import os
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from dotenv import load_dotenv

from app.utils.config import Config
from app.utils.logger import Logger
from app.core.gmail_monitor import GmailMonitor
from app.core.ziprecruiter_client import ZipRecruiterClient
from app.ui.main_window import MainWindow

def main():
    """Main application entry point."""
    # Load environment variables from .env file
    root_dir = Path(__file__).parent.parent
    dotenv_path = root_dir / '.env'
    load_dotenv(dotenv_path)
    
    # Initialize application
    app = QApplication(sys.argv)
    app.setApplicationName("Job Assistant AI")
    app.setOrganizationName("JobAssistantAI")
    
    # Set application style
    app.setStyle("Fusion")
    
    # Load configuration
    config = Config()
    
    # Initialize logger
    logger = Logger(config)
    log = logger.get_logger()
    log.info("Starting Job Assistant AI application")
    
    # Initialize core components
    gmail_monitor = GmailMonitor(config, logger)
    ziprecruiter_client = ZipRecruiterClient(config, logger)
    
    # Initialize main window
    main_window = MainWindow(config, logger, gmail_monitor, ziprecruiter_client)
    
    # When started from run_app.py, always show the main window
    # Check the name of the script that started the application
    if Path(sys.argv[0]).name == 'run_app.py':
        main_window.show()
    else:
        # Use config setting only if not started from run_app.py
        ui_config = config.get('ui', {})
        if ui_config.get('startup_minimized', False):
            main_window.hide()
        else:
            main_window.show()
    
    # Run application event loop
    exit_code = app.exec()
    
    # Cleanup before exit
    log.info("Shutting down Job Assistant AI application")
    
    return exit_code

if __name__ == "__main__":
    sys.exit(main())
