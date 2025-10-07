# Amazon Price Tracker

A Python application that monitors Amazon product prices and sends email alerts when the price drops below your target threshold.

---

## Project Overview

This tool automates price tracking for Amazon products. It:
1. Scrapes the product page to get current price
2. Compares it with your target price
3. Sends an email alert if the price drops below your threshold

**Use Case:** Track products you want to buy and get notified when they go on sale.

---

## Requirements

### Prerequisites

- Python 3.7 or higher
- Gmail account (for sending alerts)
- Basic understanding of Python

### Required Libraries

```bash
pip install requests beautifulsoup4 python-dotenv
```

**What each library does:**
- `requests`: Fetches web pages
- `beautifulsoup4`: Extracts data from HTML
- `python-dotenv`: Manages environment variables
- `smtplib`: Sends emails (built-in with Python)

---

## Setup Guide

### Step 1: Gmail App Password

Gmail requires an "App Password" for third-party apps. Regular passwords won't work.

1. Go to your [Google Account](https://myaccount.google.com/)
2. Navigate to **Security** → **2-Step Verification** (enable if not already)
3. Scroll down to **App passwords**
4. Click **Select app** → Choose "Mail"
5. Click **Select device** → Choose "Other" → Type "Python Script"
6. Click **Generate**
7. Copy the 16-character password (save it, you won't see it again)

### Step 2: Create .env File

Create a file named `.env` in your project folder:

```
MY_EMAIL=your.email@gmail.com
MY_PASSWORD=your_16_char_app_password
```

**Important:** Never share or commit this file to GitHub!

### Step 3: Create .gitignore

Create a `.gitignore` file to protect your credentials:

```
.env
__pycache__/
*.pyc
*.pyo
```

### Step 4: Find Your Amazon Product URL

1. Go to Amazon and find the product you want to track
2. Copy the full URL from the address bar
3. Paste it in the code where `PRODUCT_URL` is defined

---

## Complete Code Walkthrough

### Part 1: Imports

```python
import os
import time
import smtplib
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
```

**What we're importing:**
- `os`: Access environment variables
- `time`: Add delays between requests
- `smtplib`: Send emails
- `requests`: Make HTTP requests
- `BeautifulSoup`: Parse HTML
- `load_dotenv`: Load .env file
- `MIMEText`/`MIMEMultipart`: Create properly formatted emails

---

### Part 2: Configuration

```python
PRODUCT_URL = "https://www.amazon.com/..."
TARGET_PRICE = 500.00
```

**Variables you should customize:**
- `PRODUCT_URL`: The Amazon product you want to track
- `TARGET_PRICE`: Send alert if price drops below this amount

---

### Part 3: HTTP Headers

```python
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...",
    "Accept": "text/html,application/xhtml+xml...",
    # ... more headers
}
```

**Why headers are important:**
- Amazon blocks requests without proper headers
- User-Agent makes your script look like a real browser
- Without these, you'll get blocked or receive different HTML

**Pro tip:** These headers work for most cases. If Amazon blocks you, try updating the User-Agent to match your actual browser.

---

### Part 4: Fetch the Amazon Page

```python
try:
    response = requests.get(url=PRODUCT_URL, headers=HEADERS)
    time.sleep(2)  # Wait 2 seconds
    response.encoding = "utf-8"
    response.raise_for_status()
    amazon_html = response.text
    
except requests.exceptions.RequestException as e:
    print(f"Error fetching Amazon data: {e}")
    exit(1)
```

**Step by step:**
1. `requests.get()`: Sends HTTP GET request to Amazon
2. `headers=HEADERS`: Includes our browser-like headers
3. `time.sleep(2)`: Waits 2 seconds (avoids rate limiting)
4. `response.encoding = "utf-8"`: Handles special characters
5. `raise_for_status()`: Raises error if HTTP status is 4xx or 5xx
6. `response.text`: Gets the HTML as text
7. `except`: Catches any network errors and exits gracefully

**Common errors:**
- `ConnectionError`: No internet connection
- `Timeout`: Amazon took too long to respond
- `HTTPError`: Amazon blocked the request (403, 404, etc.)

---

### Part 5: Parse HTML with BeautifulSoup

```python
soup = BeautifulSoup(amazon_html, "html.parser")
```

**What this does:**
- Takes raw HTML text
- Converts it into a structured object you can search
- Now you can use methods like `.find()` to extract data

---

### Part 6: Extract Product Price

```python
price_tag = soup.find("span", class_="a-price-whole")
if not price_tag:
    print("Error: Price not found on page")
    exit(1)

price_text = price_tag.get_text().strip().replace(",", "")
price = float(price_text)
```

**Step by step:**
1. Find the `<span>` with class `a-price-whole`
2. Check if it exists (Amazon might change their HTML)
3. Extract text: `"599.99"` or `"1,299.99"`
4. `.strip()`: Remove whitespace
5. `.replace(",", "")`: Remove commas from numbers like `1,299.99`
6. `float()`: Convert string to number

**How to find the class name:**
1. Go to the Amazon product page
2. Right-click the price → "Inspect"
3. Find the `<span>` element containing the price
4. Copy the class name (e.g., `a-price-whole`)

**Note:** Amazon changes their HTML occasionally. If the script breaks, re-inspect and update the class name.

---

### Part 7: Extract Product Title

```python
title_tag = soup.find("span", class_="a-size-large product-title-word-break")
if not title_tag:
    print("Error: Product title not found on page")
    exit(1)

title = title_tag.get_text().strip()
```

**What this does:**
- Finds the product title
- Extracts the text
- Removes extra whitespace

**Example output:** `"Apple Mac Mini Desktop Computer M4"`

---

### Part 8: Compare Price with Target

```python
print(f"Product: {title}")
print(f"Current price: ${price:.2f}")
print(f"Target price: ${TARGET_PRICE:.2f}")

if price >= TARGET_PRICE:
    print(f"Price is above target. No alert sent.")
    exit(0)

print(f"Price alert! Product is below ${TARGET_PRICE:.2f}")
```

**Logic:**
1. Display current price and target price
2. If price is higher than target → no alert, exit program
3. If price is lower → continue to send email

**Note:** `.2f` formats the number to 2 decimal places (e.g., `499.00`)

---

### Part 9: Load Email Credentials

```python
load_dotenv()

MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")

if not MY_EMAIL or not MY_PASSWORD:
    print("Error: Email credentials not found in .env file")
    exit(1)
```

**What happens:**
1. `load_dotenv()`: Reads the `.env` file
2. `os.getenv()`: Gets the values of environment variables
3. Validates that both credentials exist
4. Exits if credentials are missing

**Security best practice:** Never hardcode passwords in your code!

---

### Part 10: Create Email Message

```python
msg = MIMEMultipart()
msg['From'] = MY_EMAIL
msg['To'] = MY_EMAIL
msg['Subject'] = f"Amazon Price Alert: {title[:50]}..."

body = f"""
Amazon Price Alert!

The product you're tracking has dropped below ${TARGET_PRICE:.2f}

Product: {title}
Current Price: ${price:.2f}
Savings: ${TARGET_PRICE - price:.2f}

View product:
{PRODUCT_URL}

---
This is an automated alert from your Amazon Price Tracker.
"""

msg.attach(MIMEText(body, 'plain', 'utf-8'))
```

**Step by step:**
1. `MIMEMultipart()`: Creates an email message object
2. `msg['From']`: Sender email (your email)
3. `msg['To']`: Recipient email (also your email)
4. `msg['Subject']`: Email subject line
5. `title[:50]`: Truncates title to 50 characters for subject
6. `body`: The email content with f-string formatting
7. `MIMEText(..., 'utf-8')`: Attaches body with UTF-8 encoding (handles special characters)

**Why UTF-8?**
- Allows Spanish characters: ñ, á, é, í, ó, ú
- Without it, you get encoding errors

---

### Part 11: Send Email via Gmail

```python
try:
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=msg.as_string()
        )
    print("Email alert sent successfully!")
    
except smtplib.SMTPException as e:
    print(f"Error sending email: {e}")
    exit(1)
```

**Step by step:**
1. `smtplib.SMTP("smtp.gmail.com", 587)`: Connect to Gmail's SMTP server
   - `smtp.gmail.com`: Gmail's server address
   - `587`: TLS port
2. `starttls()`: Encrypts the connection (security)
3. `login()`: Authenticates with your email and app password
4. `sendmail()`: Sends the email
   - `from_addr`: Your email
   - `to_addrs`: Recipient (can be different)
   - `msg.as_string()`: Converts MIME object to string
5. `with`: Automatically closes connection when done
6. Error handling catches SMTP errors (wrong password, network issues, etc.)

---

## How to Run

### One-Time Setup
```bash
# Install dependencies
pip install requests beautifulsoup4 python-dotenv

# Create .env file with your credentials
# Add your product URL to the code
```

### Every Time You Want to Check
```bash
python main.py
```

**Expected output:**
```
Fetching Amazon product page...
Page fetched successfully
Extracting product information...
Product: Apple Mac Mini Desktop Computer M4
Current price: $479.00
Target price: $500.00
Price alert! Product is below $500.00
Sending email alert...
Email alert sent successfully!

======================================================================
PRICE TRACKING COMPLETED
======================================================================
```

---

## Automating Price Checks

### Option 1: Cron Job (Linux/Mac)

Run the script automatically every day:

```bash
# Open crontab editor
crontab -e

# Add this line (runs daily at 9 AM)
0 9 * * * /usr/bin/python3 /path/to/your/main.py
```

### Option 2: Task Scheduler (Windows)

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., daily at 9 AM)
4. Action: Start a program
5. Program: `python.exe`
6. Arguments: `C:\path\to\your\main.py`

### Option 3: While Loop in Python

Add this at the end of your script:

```python
import schedule

def check_price():
    # Your entire script logic here
    pass

# Run every day at 9 AM
schedule.every().day.at("09:00").do(check_price)

while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
```

---

## Improvements Made to Original Code

### 1. Better Error Handling
**Before:**
```python
price_tag = soup.find("span", class_="a-price-whole")
price = float(price_tag.get_text().strip())
```

**After:**
```python
price_tag = soup.find("span", class_="a-price-whole")
if not price_tag:
    print("Error: Price not found")
    exit(1)
price = float(price_tag.get_text().strip())
```

**Why:** Prevents crashes if Amazon changes their HTML.

### 2. Target Price Constant
**Before:** Hardcoded `if float(price) < 500:`

**After:** `TARGET_PRICE = 500.00` at the top

**Why:** Easier to change, more professional.

### 3. Better Variable Names
**Before:** `msg` for both message object and string

**After:** Clear separation with proper MIME objects

### 4. SMTP Port Specified
**Before:** `smtplib.SMTP("smtp.gmail.com")`

**After:** `smtplib.SMTP("smtp.gmail.com", 587)`

**Why:** Explicit is better than implicit. Port 587 is required for TLS.

### 5. Console Feedback
Added progress messages so you know what's happening at each step.

### 6. Exit Codes
**Before:** `exit()`

**After:** `exit(1)` for errors, `exit(0)` for success

**Why:** Standard practice for programs (0 = success, 1 = error).

### 7. Price Formatting
Consistent use of `.2f` for dollar amounts throughout.

### 8. Better Email Subject
**Before:** Generic "Amazon Price Alert!"

**After:** Includes truncated product name for context

---

## Troubleshooting

### Problem 1: "Error fetching Amazon data"

**Possible causes:**
- No internet connection
- Amazon blocked your IP (too many requests)
- URL is invalid or product no longer available

**Solutions:**
1. Check your internet connection
2. Wait a few hours and try again
3. Update the User-Agent header
4. Verify the product URL is still valid

---

### Problem 2: "Price not found on page"

**Cause:** Amazon changed their HTML structure

**Solution:**
1. Go to the Amazon product page
2. Right-click the price → Inspect
3. Find the `<span>` containing the price
4. Update the class name in your code:
   ```python
   price_tag = soup.find("span", class_="NEW_CLASS_NAME_HERE")
   ```

---

### Problem 3: "Email credentials not found"

**Causes:**
- `.env` file doesn't exist
- Typo in variable names
- `.env` file in wrong location

**Solutions:**
1. Verify `.env` is in the same folder as your script
2. Check for typos: `MY_EMAIL` not `my_email`
3. Ensure no spaces around `=` in .env file

---

### Problem 4: "SMTP Authentication Error"

**Causes:**
- Wrong email or password
- Using regular password instead of App Password
- 2-Step Verification not enabled

**Solutions:**
1. Generate a new App Password (see Setup Step 1)
2. Enable 2-Step Verification first
3. Copy the 16-character password exactly (no spaces)

---

### Problem 5: Email not received

**Check:**
1. Spam/Junk folder
2. Email address is correct in .env
3. Gmail is not blocking the email
4. Check terminal for error messages

---

## Security Best Practices

### ✅ Do:
- Use App Passwords, never your real Gmail password
- Keep credentials in `.env` file
- Add `.env` to `.gitignore`
- Use environment variables

### ❌ Don't:
- Hardcode passwords in your script
- Share your `.env` file
- Commit `.env` to GitHub
- Use your main Gmail password

---

## Limitations & Considerations

### Legal Considerations
- Amazon's Terms of Service prohibit automated scraping
- Use responsibly and infrequently
- For learning purposes, track 1-2 products max
- Don't run the script every minute

### Technical Limitations
- Amazon may block your IP if you make too many requests
- HTML structure changes frequently (script may break)
- Prices may be region-specific
- Some products have dynamic pricing

### Alternatives for Production Use
If you need reliable price tracking:
1. Use [Amazon Product Advertising API](https://webservices.amazon.com/paapi5/documentation/) (official)
2. Subscribe to services like [CamelCamelCamel](https://camelcamelcamel.com/)
3. Use browser extensions (Honey, Keepa)

---

## Next Steps & Enhancements

### Beginner Enhancements
1. Track multiple products (use a list of URLs)
2. Store price history in a text file
3. Send email to a friend
4. Add a log file to track when script runs

### Intermediate Enhancements
1. Store data in SQLite database
2. Create price graphs with matplotlib
3. Use Selenium for better scraping
4. Add Telegram bot notifications

### Advanced Enhancements
1. Deploy to cloud (AWS Lambda, Heroku)
2. Create web dashboard with Flask
3. Machine learning price prediction
4. Multi-currency support

---

## Project Structure

```
amazon-price-tracker/
│
├── main.py              # Your main script
├── .env                 # Credentials (NEVER commit)
├── .gitignore           # Files to ignore
├── README.md            # This documentation
└── requirements.txt     # Dependencies
```

### requirements.txt
```
requests==2.31.0
beautifulsoup4==4.12.2
python-dotenv==1.0.0
```

---

## Concepts You Learned

✓ Web scraping with BeautifulSoup
✓ HTTP requests with headers
✓ HTML parsing and data extraction
✓ Environment variables for security
✓ Sending emails with SMTP
✓ MIME email formatting
✓ Error handling and validation
✓ String formatting and manipulation
✓ Working with external APIs

---

## Additional Resources

- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests Library Guide](https://requests.readthedocs.io/)
- [Python SMTP Documentation](https://docs.python.org/3/library/smtplib.html)
- [Gmail SMTP Settings](https://support.google.com/mail/answer/7126229)

---

## Final Notes

This project demonstrates practical Python skills:
- **Data extraction** from real websites
- **Automation** of repetitive tasks
- **Email integration** for notifications
- **Error handling** for robust code

Use this knowledge responsibly and ethically. Web scraping should be done in moderation and within legal boundaries.

**Happy price tracking!** 🎯
