import os
import json
from pathlib import Path

class Config:
    """Configuration manager for the application."""
    
    def __init__(self):
        """Initialize the configuration."""
        self.config = {}
        self.config_path = self._get_config_path()
        self.load_config()
        self.load_env_vars()
        
    def _get_config_path(self):
        """Get the path to the configuration file."""
        app_dir = Path(__file__).parent.parent
        config_path = app_dir / 'resources' / 'config.json'
        return config_path
    
    def load_config(self):
        """Load configuration from file."""
        if not self.config_path.exists():
            print(f"Configuration file not found: {self.config_path}")
            self._create_default_config()
            return
            
        try:
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
        except Exception as e:
            print(f"Error loading configuration: {e}")
            self._create_default_config()
    
    def load_env_vars(self):
        """Load configuration from environment variables."""
        # Gmail settings
        if 'GMAIL_EMAIL' in os.environ:
            self.config.setdefault('gmail', {})['email'] = os.environ['GMAIL_EMAIL']
            
        if 'GMAIL_PASSWORD' in os.environ:
            self.config.setdefault('gmail', {})['password'] = os.environ['GMAIL_PASSWORD']
            
        if 'SCAN_INTERVAL' in os.environ:
            try:
                scan_interval = int(os.environ['SCAN_INTERVAL'])
                self.config.setdefault('gmail', {})['scan_interval'] = scan_interval
            except ValueError:
                pass
                
        # ZipRecruiter settings
        if 'ZIPRECRUITER_EMAIL' in os.environ:
            self.config.setdefault('ziprecruiter', {})['email'] = os.environ['ZIPRECRUITER_EMAIL']
            
        if 'ZIPRECRUITER_PASSWORD' in os.environ:
            self.config.setdefault('ziprecruiter', {})['password'] = os.environ['ZIPRECRUITER_PASSWORD']
            
        if 'SEARCH_INTERVAL' in os.environ:
            try:
                search_interval = int(os.environ['SEARCH_INTERVAL'])
                self.config.setdefault('ziprecruiter', {})['search_interval'] = search_interval
            except ValueError:
                pass
    
    def _create_default_config(self):
        """Create default configuration."""
        self.config = {
            'gmail': {
                'credentials_file': 'app/resources/credentials.json',
                'token_file': 'app/resources/token.json',
                'scan_interval': 300,
                'resume_path': 'app/resources/dummy_resume.txt',
                'response_template': 'Thank you for considering my application.',
                'criteria': {
                    'pay_range_min': 70000,
                    'employment_types': ['full-time', 'contract'],
                    'excluded_companies': [],
                    'location_requirements': ['remote']
                }
            },
            'ziprecruiter': {
                'api_key': '',
                'search_interval': 3600,
                'search_radius': 25,
                'job_types': ['full-time'],
                'keywords': ['python', 'developer', 'software engineer'],
                'locations': ['remote']
            },
            'ui': {
                'start_minimized': False,
                'show_notifications': True
            }
        }
        
        # Save default config
        self.save_config()
    
    def save_config(self):
        """Save configuration to file."""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=4)
                
        except Exception as e:
            print(f"Error saving configuration: {e}")
    
    def get(self, section, default=None):
        """Get a configuration section."""
        return self.config.get(section, default)
    
    def set(self, section, value):
        """Set a configuration section."""
        self.config[section] = value
        self.save_config()
