import os
import sys
import logging
import json
import traceback
from datetime import datetime
import time
from PyQt5.QtWidgets import QApplication

# Import app components
from app.core.gmail_monitor import GmailMonitor
from app.core.ziprecruiter_client import ZipRecruiterClient
from app.ui.main_window import MainWindow
from app.utils.logger import setup_logger

def main():
    try:
        # Initialize QApplication first
        app = QApplication(sys.argv)
        
        # Load configuration
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', 'config.json')
        
        if not os.path.exists(config_path):
            print(f"Configuration file not found: {config_path}")
            return 1
        
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Set up logging
        log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
        logger = setup_logger('job_assistant', log_dir, logging.DEBUG)
        
        # Initialize core components
        gmail_monitor = GmailMonitor(config, logger)
        ziprecruiter_client = ZipRecruiterClient(config, logger)
        
        # Initialize main window
        main_window = MainWindow(config, logger, gmail_monitor, ziprecruiter_client)
        
        # Start services
        # gmail_monitor.start_monitoring()  # Commented out until credentials are setup
        
        # Always show the window
        print("Showing main application window...")
        main_window.show()
        
        # Start the event loop to keep the application running
        return app.exec_()
        
    except Exception as e:
        print(f"Error in main: {str(e)}")
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
