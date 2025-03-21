import os
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QGroupBox, QCheckBox, QTabWidget, QSpinBox,
    QFormLayout, QFileDialog
)
from PySide6.QtCore import Qt

class SettingsDialog(QDialog):
    """Dialog for configuring application settings."""
    
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.setup_ui()
        self.load_settings()
        
    def setup_ui(self):
        """Set up the user interface."""
        self.setWindowTitle("Settings")
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Create tabs
        tabs = QTabWidget()
        main_layout.addWidget(tabs)
        
        # Gmail tab
        gmail_tab = QGroupBox("Gmail Settings")
        gmail_layout = QFormLayout(gmail_tab)
        
        self.gmail_email = QLineEdit()
        self.gmail_password = QLineEdit()
        self.gmail_password.setEchoMode(QLineEdit.Password)
        self.gmail_scan_interval = QSpinBox()
        self.gmail_scan_interval.setRange(60, 3600)
        self.gmail_scan_interval.setSuffix(" seconds")
        self.gmail_resume_path = QLineEdit()
        
        browse_resume_btn = QPushButton("Browse...")
        browse_resume_btn.clicked.connect(self.browse_resume)
        
        resume_layout = QHBoxLayout()
        resume_layout.addWidget(self.gmail_resume_path)
        resume_layout.addWidget(browse_resume_btn)
        
        gmail_layout.addRow("Email:", self.gmail_email)
        gmail_layout.addRow("Password:", self.gmail_password)
        gmail_layout.addRow("Scan Interval:", self.gmail_scan_interval)
        gmail_layout.addRow("Resume File:", resume_layout)
        
        # ZipRecruiter tab
        zip_tab = QGroupBox("ZipRecruiter Settings")
        zip_layout = QFormLayout(zip_tab)
        
        self.zip_email = QLineEdit()
        self.zip_password = QLineEdit()
        self.zip_password.setEchoMode(QLineEdit.Password)
        self.zip_search_interval = QSpinBox()
        self.zip_search_interval.setRange(600, 86400)
        self.zip_search_interval.setSuffix(" seconds")
        self.zip_keywords = QLineEdit()
        
        zip_layout.addRow("Email:", self.zip_email)
        zip_layout.addRow("Password:", self.zip_password)
        zip_layout.addRow("Search Interval:", self.zip_search_interval)
        zip_layout.addRow("Keywords (comma separated):", self.zip_keywords)
        
        # UI tab
        ui_tab = QGroupBox("UI Settings")
        ui_layout = QFormLayout(ui_tab)
        
        self.start_minimized = QCheckBox("Start minimized")
        self.show_notifications = QCheckBox("Show notifications")
        
        ui_layout.addRow(self.start_minimized)
        ui_layout.addRow(self.show_notifications)
        
        # Add tabs to tab widget
        tabs.addTab(gmail_tab, "Gmail")
        tabs.addTab(zip_tab, "ZipRecruiter")
        tabs.addTab(ui_tab, "UI")
        
        # Button layout
        button_layout = QHBoxLayout()
        
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        
        self.save_button.clicked.connect(self.save_settings)
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        
        main_layout.addLayout(button_layout)
    
    def load_settings(self):
        """Load settings from config into UI elements."""
        # Gmail settings
        gmail_config = self.config.get('gmail', {})
        self.gmail_email.setText(gmail_config.get('email', ''))
        self.gmail_password.setText(gmail_config.get('password', ''))
        self.gmail_scan_interval.setValue(gmail_config.get('scan_interval', 300))
        self.gmail_resume_path.setText(gmail_config.get('resume_path', ''))
        
        # ZipRecruiter settings
        zip_config = self.config.get('ziprecruiter', {})
        self.zip_email.setText(zip_config.get('email', ''))
        self.zip_password.setText(zip_config.get('password', ''))
        self.zip_search_interval.setValue(zip_config.get('search_interval', 3600))
        
        # Join keywords list to string
        keywords = zip_config.get('keywords', [])
        self.zip_keywords.setText(", ".join(keywords))
        
        # UI settings
        ui_config = self.config.get('ui', {})
        self.start_minimized.setChecked(ui_config.get('start_minimized', False))
        self.show_notifications.setChecked(ui_config.get('show_notifications', True))
    
    def save_settings(self):
        """Save settings from UI elements to config."""
        # Gmail settings
        self.config['gmail']['email'] = self.gmail_email.text()
        self.config['gmail']['password'] = self.gmail_password.text()
        self.config['gmail']['scan_interval'] = self.gmail_scan_interval.value()
        self.config['gmail']['resume_path'] = self.gmail_resume_path.text()
        
        # ZipRecruiter settings
        self.config['ziprecruiter']['email'] = self.zip_email.text()
        self.config['ziprecruiter']['password'] = self.zip_password.text()
        self.config['ziprecruiter']['search_interval'] = self.zip_search_interval.value()
        
        # Split keywords string to list
        keywords_text = self.zip_keywords.text()
        if keywords_text:
            keywords = [k.strip() for k in keywords_text.split(',')]
            self.config['ziprecruiter']['keywords'] = keywords
        
        # UI settings
        self.config['ui']['start_minimized'] = self.start_minimized.isChecked()
        self.config['ui']['show_notifications'] = self.show_notifications.isChecked()
        
        # Save to environment variables
        os.environ['GMAIL_EMAIL'] = self.gmail_email.text()
        os.environ['GMAIL_PASSWORD'] = self.gmail_password.text()
        os.environ['SCAN_INTERVAL'] = str(self.gmail_scan_interval.value())
        
        os.environ['ZIPRECRUITER_EMAIL'] = self.zip_email.text()
        os.environ['ZIPRECRUITER_PASSWORD'] = self.zip_password.text()
        os.environ['SEARCH_INTERVAL'] = str(self.zip_search_interval.value())
        
        # Close dialog with accept result
        self.accept()
    
    def browse_resume(self):
        """Open file dialog to select resume file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Resume File", 
            "", "Text Files (*.txt);;PDF Files (*.pdf);;Word Documents (*.doc *.docx);;All Files (*.*)"
        )
        
        if file_path:
            self.gmail_resume_path.setText(file_path) 