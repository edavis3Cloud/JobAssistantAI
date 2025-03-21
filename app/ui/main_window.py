import os
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QPushButton, QLabel, QTextEdit, QTabWidget, 
    QGridLayout, QGroupBox, QCheckBox, QLineEdit, 
    QFileDialog, QMessageBox, QSystemTrayIcon, QMenu
)
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt, QTimer

class MainWindow(QMainWindow):
    """Main application window for the Job Assistant AI."""
    
    def __init__(self, config, logger, gmail_monitor, ziprecruiter_client):
        """Initialize the main window."""
        super().__init__()
        
        self.config = config
        self.logger = logger
        self.gmail_monitor = gmail_monitor
        self.ziprecruiter_client = ziprecruiter_client
        
        # Set up the UI
        self._setup_ui()
        
        # Set up system tray
        self._setup_tray()
        
        # Connect signals
        self._connect_signals()
    
    def _setup_ui(self):
        """Set up the user interface."""
        self.setWindowTitle("Job Assistant AI")
        self.setGeometry(100, 100, 800, 600)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Add tabs
        tabs = QTabWidget()
        main_layout.addWidget(tabs)
        
        # Email tab
        email_tab = QWidget()
        tabs.addTab(email_tab, "Email Monitor")
        
        email_layout = QVBoxLayout(email_tab)
        email_status = QLabel("Email monitoring status: Not running")
        self.email_status_label = email_status
        email_layout.addWidget(email_status)
        
        email_buttons = QWidget()
        email_buttons_layout = QGridLayout(email_buttons)
        
        start_email_btn = QPushButton("Start Monitoring")
        stop_email_btn = QPushButton("Stop Monitoring")
        
        self.start_email_btn = start_email_btn
        self.stop_email_btn = stop_email_btn
        
        email_buttons_layout.addWidget(start_email_btn, 0, 0)
        email_buttons_layout.addWidget(stop_email_btn, 0, 1)
        
        email_layout.addWidget(email_buttons)
        
        # Job search tab
        job_tab = QWidget()
        tabs.addTab(job_tab, "Job Search")
        
        job_layout = QVBoxLayout(job_tab)
        job_status = QLabel("Job search status: Not running")
        self.job_status_label = job_status
        job_layout.addWidget(job_status)
        
        # Bottom buttons
        bottom_buttons = QWidget()
        bottom_layout = QGridLayout(bottom_buttons)
        
        settings_btn = QPushButton("Settings")
        exit_btn = QPushButton("Exit")
        
        self.settings_btn = settings_btn
        self.exit_btn = exit_btn
        
        bottom_layout.addWidget(settings_btn, 0, 0)
        bottom_layout.addWidget(exit_btn, 0, 1)
        
        main_layout.addWidget(bottom_buttons)
    
    def _setup_tray(self):
        """Set up system tray icon and menu."""
        self.tray_icon = QSystemTrayIcon(self)
        
        # Try to load an icon if available, otherwise use a default system icon
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                'resources', 'icon.png')
        
        if os.path.exists(icon_path):
            self.tray_icon.setIcon(QIcon(icon_path))
        else:
            self.tray_icon.setIcon(QIcon.fromTheme("application-x-executable"))
        
        # Create tray menu
        tray_menu = QMenu()
        
        show_action = QAction("Show", self)
        quit_action = QAction("Quit", self)
        
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
        # Connect actions
        show_action.triggered.connect(self.show)
        quit_action.triggered.connect(self.close_application)
    
    def _connect_signals(self):
        """Connect UI signals to their handlers."""
        self.start_email_btn.clicked.connect(self.start_email_monitoring)
        self.stop_email_btn.clicked.connect(self.stop_email_monitoring)
        self.exit_btn.clicked.connect(self.close_application)
        self.settings_btn.clicked.connect(self.open_settings)
    
    def start_email_monitoring(self):
        """Start email monitoring service."""
        self.gmail_monitor.start_monitoring()
        self.email_status_label.setText("Email monitoring status: Running")
        self.logger.info("Email monitoring started from UI")
    
    def stop_email_monitoring(self):
        """Stop email monitoring service."""
        self.gmail_monitor.stop_monitoring()
        self.email_status_label.setText("Email monitoring status: Stopped")
        self.logger.info("Email monitoring stopped from UI")
    
    def closeEvent(self, event):
        """Handle window close event."""
        # Minimize to tray instead of closing
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "Job Assistant AI",
            "Application is still running in the system tray.",
            QSystemTrayIcon.Information,
            2000
        )
    
    def close_application(self):
        """Properly close the application."""
        # Stop services
        self.gmail_monitor.stop_monitoring()
        
        # Really quit the application
        self.tray_icon.hide()
        QApplication.instance().quit()
    
    def show(self):
        """Show the main window."""
        self.showNormal()
        self.activateWindow()
        print("Window shown and activated!")

    def open_settings(self):
        """Open the settings dialog."""
        try:
            from app.ui.settings_dialog import SettingsDialog
            dialog = SettingsDialog(self.config, self)
            if dialog.exec_():
                # If settings were accepted, update components with new config
                self.logger.info("Settings updated")
                
                # Update Gmail monitor with new settings
                self.gmail_monitor.email = self.config['gmail'].get('email')
                self.gmail_monitor.password = self.config['gmail'].get('password')
                
                # Update ZipRecruiter client with new settings
                self.ziprecruiter_client.email = self.config['ziprecruiter'].get('email')
                self.ziprecruiter_client.password = self.config['ziprecruiter'].get('password')
                
        except Exception as e:
            self.logger.error(f"Error opening settings: {e}")
            print(f"Error opening settings: {e}")

# This is only for testing the UI independently
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    
    # Mock objects
    class MockLogger:
        def info(self, msg): print(f"INFO: {msg}")
        def error(self, msg): print(f"ERROR: {msg}")
        def debug(self, msg): print(f"DEBUG: {msg}")
    
    class MockMonitor:
        def start_monitoring(self): print("Started monitoring")
        def stop_monitoring(self): print("Stopped monitoring")
    
    # Create and show window
    window = MainWindow({}, MockLogger(), MockMonitor(), MockMonitor())
    window.show()
    
    sys.exit(app.exec_())
