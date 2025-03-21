# Job Assistant AI

An automated tool for job searching and application management that monitors Gmail for job opportunities and interacts with ZipRecruiter.

## Features

- Monitors Gmail for job-related emails
- Searches for jobs on ZipRecruiter
- Analyzes job opportunities
- Sends automated responses with resume

## Setup

### Prerequisites

- Python 3.8 or higher
- Required Python packages (see requirements.txt)

### Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```
# Gmail credentials
GMAIL_EMAIL=your_email@gmail.com
GMAIL_PASSWORD=your_password

# ZipRecruiter credentials
ZIPRECRUITER_EMAIL=your_email@gmail.com
ZIPRECRUITER_PASSWORD=your_password

# Configuration settings
SCAN_INTERVAL=300
SEARCH_INTERVAL=3600
```

Replace the example values with your actual credentials.

## Usage

Run the application:

```
python run_app.py
```

## Security Notes

- Never commit your `.env` file to version control
- For Gmail, you may need to enable "Less secure app access" or use App Passwords
