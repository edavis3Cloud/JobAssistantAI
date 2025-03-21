import os
import time
import base64
import email
import re
import threading
import smtplib
from datetime import datetime, timedelta
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

import google.auth.exceptions
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GmailMonitor:
    """
    Gmail monitoring and automated response class.
    
    This class handles:
    - Authentication with Gmail API
    - Scanning incoming emails
    - Analyzing email content
    - Automated responses with resume attachment
    """
    
    # Gmail API scopes needed for this application
    SCOPES = [
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/gmail.send',
        'https://www.googleapis.com/auth/gmail.modify'
    ]
    
    def __init__(self, config, logger):
        """
        Initialize the Gmail monitor.
        
        Args:
            config: Application configuration
            logger: Application logger
        """
        self.config = config
        self.logger = logger
        self.service = None
        self.monitor_thread = None
        self.stop_event = threading.Event()
        
        # Load Gmail configuration
        self.gmail_config = config.get('gmail', {})
        
        # Store email and password
        self.email = self.gmail_config.get('email')
        self.password = self.gmail_config.get('password')
        
        # Employment-related keywords for identifying job emails
        self.job_keywords = [
            # Job titles and positions
            'job', 'position', 'role', 'career', 'opportunity', 'vacancy', 'opening',
            
            # Application process
            'application', 'interview', 'recruiter', 'hiring', 'apply',
            'resume', 'cv', 'cover letter',
            
            # Job details
            'compensation', 'salary', 'pay rate', 'benefits', 'bonus',
            'full-time', 'part-time', 'contract', 'permanent', 'temporary',
            'remote', 'hybrid', 'on-site', 'on site', 'location',
            
            # Requirements
            'qualifications', 'requirements', 'responsibilities', 'duties',
            'skills', 'experience', 'education', 'degree', 'certification',
            
            # Company info
            'company', 'employer', 'team', 'department', 'division'
        ]
        
        # Regular expressions for extracting information
        self.pay_regex = r'(?:salary|compensation|pay)(?:\s+is|\s+range)?(?:\s*:)?\s*(?:\$|USD)?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)\s*(?:\/|\s*(?:per|an?)\s*)?(?:hour|hr|yr|year|annum|month|mo|week|wk)?(?:\s*(?:-|to)\s*(?:\$|USD)?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?))?\s*(?:\/|\s*(?:per|an?)\s*)?(?:hour|hr|yr|year|annum|month|mo|week|wk)?'
        self.employment_type_regex = r'(?:position|job|employment|work)\s+(?:type|status)(?:\s+is)?(?:\s*:)?\s*(full[ -]time|part[ -]time|contract|permanent|temporary|temp|freelance|intern|internship)'
        self.benefits_regex = r'benefits(?:\s+include|\s+offered)?(?:\s*:)?\s*([^.]*)'
        
    def authenticate(self):
        """
        Authenticate with Gmail API.
        
        Returns:
            bool: True if authentication successful, False otherwise
        """
        try:
            if not self.email or not self.password:
                self.logger.error("Gmail credentials not found. Please check your .env file.")
                return False
                
            self.logger.info(f"Authenticating with Gmail using email: {self.email}")
            
            # For SMTP-based email interactions
            try:
                smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
                smtp_server.starttls()
                smtp_server.login(self.email, self.password)
                smtp_server.quit()
                self.logger.info("SMTP Authentication successful")
            except Exception as e:
                self.logger.error(f"SMTP Authentication failed: {e}")
                return False
                
            # For API-based operations, continue with the Google API flow
            # This would use the provided OAuth credentials file too
            credentials_file = self.gmail_config.get('credentials_file')
            token_file = self.gmail_config.get('token_file')
            
            # Initialize for API access as well if credentials file is available
            if os.path.exists(credentials_file):
                self.logger.info("Setting up Gmail API access")
                # This would be expanded in a production environment
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error during authentication: {e}")
            return False
    
    def start_monitoring(self):
        """Start monitoring emails in a separate thread."""
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.logger.warning("Email monitoring is already running")
            return
        
        # Authentication is required before monitoring
        if not self.authenticate():
            self.logger.error("Gmail authentication failed. Cannot start monitoring.")
            return
        
        # Reset stop event
        self.stop_event.clear()
        
        # Start monitoring in a separate thread
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop,
            daemon=True
        )
        self.monitor_thread.start()
        self.logger.info("Started Gmail monitoring thread")
        return True
    
    def _monitor_loop(self):
        """Main email monitoring loop."""
        scan_interval = self.gmail_config.get('scan_interval', 300)  # Default 5 minutes
        
        self.logger.info(f"Gmail monitor running with scan interval of {scan_interval} seconds")
        
        while not self.stop_event.is_set():
            try:
                self.logger.info("Scanning emails for job opportunities...")
                
                # Actual email scanning code would go here
                # This is where we would use the Gmail API or IMAP to check emails
                
                # Wait for the next scan interval or until stop is requested
                self.stop_event.wait(scan_interval)
                
            except Exception as e:
                self.logger.exception(f"Error in email monitoring loop: {e}")
                # Wait for a short time before retrying
                self.stop_event.wait(60)
    
    def stop_monitoring(self):
        """Stop monitoring emails."""
        if not self.monitor_thread or not self.monitor_thread.is_alive():
            self.logger.warning("Email monitoring is not running")
            return
        
        # Set stop event to signal the thread to exit
        self.stop_event.set()
        
        # Wait for the thread to finish
        self.monitor_thread.join(timeout=5.0)
        if self.monitor_thread.is_alive():
            self.logger.warning("Email monitoring thread did not exit gracefully")
        else:
            self.logger.info("Stopped Gmail monitoring thread")
        return True
