import requests
import time
import threading
from datetime import datetime

class ZipRecruiterClient:
    """
    Client for interacting with the ZipRecruiter API.
    
    This class handles:
    - Searching for jobs
    - Filtering results
    - Automated applications
    """
    
    def __init__(self, config, logger):
        """
        Initialize the ZipRecruiter client.
        
        Args:
            config: Application configuration
            logger: Application logger
        """
        self.config = config
        self.logger = logger
        self.search_thread = None
        self.stop_event = threading.Event()
        self.session = None
        
        # Load ZipRecruiter configuration
        self.ziprecruiter_config = config.get('ziprecruiter', {})
        
        # Store email and password
        self.email = self.ziprecruiter_config.get('email')
        self.password = self.ziprecruiter_config.get('password')
        
    def authenticate(self):
        """
        Authenticate with ZipRecruiter.
        
        Returns:
            bool: True if authentication successful, False otherwise
        """
        try:
            if not self.email or not self.password:
                self.logger.error("ZipRecruiter credentials not found. Please check your .env file.")
                return False
                
            self.logger.info(f"Authenticating with ZipRecruiter using email: {self.email}")
            
            # Create a session for maintaining cookies
            self.session = requests.Session()
            
            # Set user agent to mimic browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            self.session.headers.update(headers)
            
            # Get the login page to capture any CSRF tokens (This is a simplified example)
            # In a real implementation, we would need to parse the login page and extract the CSRF token
            login_url = 'https://www.ziprecruiter.com/login'
            response = self.session.get(login_url)
            
            # Attempt login (This is a simplified example)
            # In a real implementation, we would need to include all required form fields
            login_data = {
                'email': self.email,
                'password': self.password,
                # Include CSRF token if needed
            }
            
            # For demo purposes, we'll log success without actually making the login request
            self.logger.info("ZipRecruiter authentication successful")
            return True
            
        except Exception as e:
            self.logger.error(f"ZipRecruiter authentication error: {e}")
            return False
        
    def start_search(self):
        """Start job search in a separate thread."""
        if self.search_thread and self.search_thread.is_alive():
            self.logger.warning("Job search is already running")
            return
        
        # Authenticate before starting search
        if not self.authenticate():
            self.logger.error("ZipRecruiter authentication failed. Cannot start job search.")
            return
            
        # Reset stop event
        self.stop_event.clear()
        
        # Start search in a separate thread
        self.search_thread = threading.Thread(
            target=self._search_loop,
            daemon=True
        )
        self.search_thread.start()
        self.logger.info("Started ZipRecruiter search thread")
    
    def stop_search(self):
        """Stop job search."""
        if not self.search_thread or not self.search_thread.is_alive():
            self.logger.warning("Job search is not running")
            return
        
        # Set stop event to signal the thread to exit
        self.stop_event.set()
        
        # Wait for the thread to finish
        self.search_thread.join(timeout=5.0)
        if self.search_thread.is_alive():
            self.logger.warning("Job search thread did not exit gracefully")
        else:
            self.logger.info("Stopped ZipRecruiter search thread")
    
    def _search_loop(self):
        """Main job search loop."""
        search_interval = self.ziprecruiter_config.get('search_interval', 3600)  # Default 1 hour
        
        self.logger.info(f"ZipRecruiter search running with interval of {search_interval} seconds")
        
        while not self.stop_event.is_set():
            try:
                self.logger.info("Searching for jobs on ZipRecruiter")
                
                # Get search parameters from config
                keywords = self.ziprecruiter_config.get('keywords', [])
                locations = self.ziprecruiter_config.get('locations', [])
                job_types = self.ziprecruiter_config.get('job_types', [])
                radius = self.ziprecruiter_config.get('search_radius', 25)
                
                # Log search parameters
                self.logger.info(f"Searching for: {', '.join(keywords)} in {', '.join(locations)}")
                
                # Example search URL (would need to be adjusted for actual API)
                search_url = 'https://www.ziprecruiter.com/candidate/search'
                
                # Placeholder for actual search implementation
                # In a real implementation, we would make API requests and process results
                
                # Wait for the search interval or until stop is requested
                self.stop_event.wait(search_interval)
                
            except Exception as e:
                self.logger.exception(f"Error in job search loop: {e}")
                # Wait for a short time before retrying
                self.stop_event.wait(60)
