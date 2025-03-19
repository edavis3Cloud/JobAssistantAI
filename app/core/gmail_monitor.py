import os
import time
import base64
import email
import re
import threading
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
        self.gmail_config = config.get('gmail')
        
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
            # For the test application, return success without actual authentication
            self.logger.info("Mock Gmail authentication successful")
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
        
        # Log that we're starting
        self.logger.info("Starting Gmail monitoring...")
        
        # For demo purposes, we'll just log that we started rather than actually monitoring
        # In a real implementation, this would start a thread to monitor emails
        return True
    
    def stop_monitoring(self):
        """Stop monitoring emails."""
        # Just log that we're stopping for demo purposes
        self.logger.info("Gmail monitoring stopped")
        self.stop_event.set()
        return True
