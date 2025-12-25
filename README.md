# FIFA World Cup 26 Perks Sweepstakes Automation

Automates daily entry into the FIFA World Cup 26 Perks sweepstakes on [fwc26perks.com](https://www.fwc26perks.com/).

## Features

- Automatically selects all available sweepstakes
- Fills in your personal information
- Checks all required checkboxes
- Submits the form
- Can be run daily to maximize your chances

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install ChromeDriver (required for Selenium):
   - **macOS**: `brew install chromedriver`
   - **Linux**: Download from [ChromeDriver Downloads](https://chromedriver.chromium.org/)
   - **Windows**: Download and add to PATH

## Configuration

Edit `config.py` to update your personal information:

```python
FORM_DATA = {
    'first': 'Your First Name',
    'last': 'Your Last Name',
    'email': 'your.email@example.com',
    'confirmEmail': 'your.email@example.com',
    'zip': '12345',
    'aaNumber': 'YOUR_AADVANTAGE_NUMBER'
}
```

## Usage

### Basic Usage

Run the script:
```bash
python fifa_sweepstakes.py
```

The script will:
1. Open Chrome browser (you can watch the process)
2. Navigate to fwc26perks.com
3. Select all available sweepstakes
4. Fill in your information
5. Check all checkboxes
6. Submit the form

### Headless Mode

To run without showing the browser window, edit `config.py`:
```python
HEADLESS = True
```

Or modify `fifa_sweepstakes.py`:
```python
with FIFASweepstakesBot(headless=True) as bot:
```

## Daily Automation

You can set this up to run daily using cron (macOS/Linux) or Task Scheduler (Windows).

### macOS/Linux (cron)

1. Open crontab:
```bash
crontab -e
```

2. Add a line to run daily at a specific time (e.g., 10:00 AM):
```
0 10 * * * cd /Users/qrui/Projects/fifa && /usr/bin/python3 fifa_sweepstakes.py
```

Make sure to adjust the path to your Python executable and project directory.

### Windows (Task Scheduler)

1. Open Task Scheduler
2. Create a new task
3. Set trigger to "Daily" at your preferred time
4. Set action to run: `python` with arguments: `fifa_sweepstakes.py`
5. Set working directory to your project folder

## How It Works

The bot uses Selenium WebDriver to:
- Find and click all "Select" buttons for sweepstakes
- Locate form fields by their IDs and fill them
- Find and check all checkboxes
- Locate and click the submit button

## Troubleshooting

### ChromeDriver Issues
- Make sure ChromeDriver version matches your Chrome browser version
- Check that ChromeDriver is in your PATH
- Try updating ChromeDriver: `brew upgrade chromedriver` (macOS)

### Element Not Found
- The website structure may have changed
- Run with `HEADLESS = False` to see what's happening
- Check the console output for specific errors

### Submission Issues
- Some forms may have validation that requires waiting
- Try increasing `WAIT_TIMEOUT` in `config.py`
- The script includes delays to handle dynamic page loading

## Legal & Ethical Considerations

- This tool automates the entry process but still follows the website's form submission rules
- Make sure you meet all eligibility requirements for the sweepstakes
- Use responsibly and in accordance with the website's Terms of Service
- **Enter every day** as allowed by the sweepstakes rules

## Notes

- The website allows daily entries, so you can run this script once per day
- The script includes delays to ensure proper page loading
- Keep your browser and ChromeDriver updated for best results

## License

This project is provided as-is for personal use.

# fifa
