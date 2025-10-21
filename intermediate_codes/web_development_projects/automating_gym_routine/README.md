# Gym Class Booking Bot

An automated Selenium bot that books gym classes on specific days and times, handling unreliable network connections with automatic retry mechanisms.

---

## Project Overview

This bot automates the tedious process of booking gym classes by:
1. Logging into your gym account automatically
2. Scanning the schedule for specific days (Tuesday/Thursday) and times (6:00 PM)
3. Booking available classes or joining waitlists
4. Handling 50% network failure rate with smart retry logic
5. Verifying all bookings were successful

**Use Case:** Never miss your favorite gym classes again, especially when they fill up quickly!

---

## Table of Contents

- [Requirements](#requirements)
- [Installation Guide](#installation-guide)
- [Configuration](#configuration)
- [How to Run](#how-to-run)
- [Complete Code Walkthrough](#complete-code-walkthrough)
- [How It Works](#how-it-works)
- [Troubleshooting](#troubleshooting)
- [Improvements & Extensions](#improvements--extensions)
- [Concepts Learned](#concepts-learned)

---

## Requirements

### Prerequisites

- **Python 3.7+**
- **Google Chrome browser** (latest version)
- **ChromeDriver** (automatically managed by Selenium 4+)
- Gym account credentials
- Basic understanding of Python

### Required Libraries

```bash
pip install selenium python-dotenv
```

**What each library does:**
- `selenium`: Browser automation for web interactions
- `python-dotenv`: Securely loads credentials from .env file

---

## Installation Guide

### Step 1: Install Python

Download from [python.org](https://www.python.org/downloads/)

Verify:
```bash
python --version
# Should show 3.7 or higher
```

### Step 2: Install Required Libraries

```bash
pip install selenium python-dotenv
```

### Step 3: Verify Chrome is Installed

Check Chrome version: `chrome://version/`

Selenium 4+ automatically downloads the correct ChromeDriver.

### Step 4: Clone or Download Project

```bash
git clone <your-repo-url>
cd gym-booking-bot
```

---

## Configuration

### Step 1: Create .env File

Create a file named `.env` in the project root:

```
ACCOUNT_EMAIL=your.email@example.com
ACCOUNT_PASSWORD=your_secure_password
```

**Security:** This file contains sensitive information. Never share or commit it!

### Step 2: Create .gitignore

Create `.gitignore` to protect credentials:

```
.env
chrome_profile/
__pycache__/
*.pyc
*.pyo
```

### Step 3: Customize Booking Preferences

Edit these constants in the code:

```python
TARGET_DAYS = ["Tue", "Thu"]    # Days to book
TARGET_TIME = "6:00 PM"         # Preferred time
MAX_CLICK_RETRIES = 5           # Button click retries
```

---

## How to Run

### Basic Execution

```bash
python main.py
```

The bot will:
1. Open Chrome browser
2. Navigate to gym website
3. Log in with your credentials
4. Scan schedule for Tuesday/Thursday 6:00 PM classes
5. Book available classes
6. Verify bookings on My Bookings page
7. Display summary report

### What to Expect

**Console Output:**
```
Navigated to: https://appbrewery.github.io/gym/

Trying Login. Attempt: 1/7
✓ Successfully logged in

======================================================================
SCANNING SCHEDULE FOR AVAILABLE CLASSES
======================================================================

📋 Attempting to book: Yoga on Tue, Jan 15
  → Attempt 1/5: Clicking 'Book Class'...
  ✓ Success! Button changed to 'Booked'
✓ Successfully booked: Yoga on Tue, Jan 15

======================================================================
BOOKING SUMMARY
======================================================================
Days processed: Tuesday/Thursday
Target time: 6:00 PM
Total classes processed: 2
New bookings: 2
Waitlisted: 0
Already booked: 0

======================================================================
VERIFYING BOOKINGS
======================================================================

✓ Verified: Yoga (Booking)
✓ Verified: Pilates (Booking)

======================================================================
VERIFICATION RESULT
======================================================================
Expected bookings: 2
Found in My Bookings: 2

✅ SUCCESS: All bookings verified!
======================================================================
```

---

## Complete Code Walkthrough

### Part 1: Imports and Setup

```python
import os
import time
import calendar
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from dotenv import load_dotenv
```

**What we're importing:**
- `os`: File and environment variable operations
- `time`: Add delays and timing
- `calendar`: Work with day names
- `selenium`: Browser automation
- `dotenv`: Load credentials securely

---

### Part 2: Configuration Constants

```python
TARGET_DAYS = ["Tue", "Thu"]
TARGET_TIME = "6:00 PM"
DAYS_OF_THE_WEEK = list(calendar.day_name)

MAX_LOGIN_RETRIES = 7
MAX_BOOKING_RETRIES = 7
MAX_CLICK_RETRIES = 5
```

**Why use constants?**
- Easy to modify without searching through code
- Self-documenting (clear what each value means)
- Prevents "magic numbers" scattered in code
- Professional coding practice

**What each constant means:**
- `TARGET_DAYS`: Which days to book classes
- `TARGET_TIME`: What time slot to book
- `DAYS_OF_THE_WEEK`: Full names like "Tuesday", "Thursday"
- `MAX_*_RETRIES`: How many times to retry on failure

---

### Part 3: Load Credentials

```python
load_dotenv()
ACCOUNT_EMAIL = os.getenv("ACCOUNT_EMAIL")
ACCOUNT_PASSWORD = os.getenv("ACCOUNT_PASSWORD")

if not ACCOUNT_EMAIL or not ACCOUNT_PASSWORD:
    raise ValueError("Missing credentials in .env file...")
```

**Step by step:**
1. `load_dotenv()`: Read `.env` file
2. `os.getenv()`: Get environment variable value
3. Validate credentials exist before continuing
4. `raise ValueError`: Stop program if credentials missing

**Why this is important:**
- Never hardcode passwords in source code
- Prevents accidentally sharing credentials
- Separates configuration from code
- Industry standard security practice

---

### Part 4: Chrome Driver Setup

```python
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option(name="detach", value=True)

user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

driver = webdriver.Chrome(options=chrome_options)
```

**Line by line:**
1. Create Chrome options object
2. `detach=True`: Keep browser open after script ends
3. `user_data_dir`: Create persistent Chrome profile
4. Launch Chrome with these settings

**What is a Chrome profile?**
- Saves cookies, login sessions, preferences
- Next time you run, may already be logged in
- Located in `chrome_profile/` folder
- Simulates using the same browser repeatedly

---

### Part 5: Retry Utility Function

```python
import sys

def retry_with_attempts(func, retries, description):
    for attempt in range(1, retries + 1):
        print(f"Trying {description}. Attempt: {attempt}/{retries}")
        try:
            return func()
        except TimeoutException as e:
            if attempt == retries:
                # Final attempt failed - display friendly error and exit
                print("\n" + "="*70)
                print(f"❌ ERROR: {description} Failed After {retries} Attempts")
                print("="*70)
                print("Reason: Network timeout - the page did not load in time")
                print("\nPossible causes:")
                print("  • Internet connection is slow or unstable")
                print("  • Gym website is down or not responding")
                print("  • Firewall or antivirus blocking connection")
                print("\nPlease check your connection and try again.")
                print("="*70 + "\n")
                driver.quit()
                sys.exit(1)  # Exit cleanly with error code
            
            print(f"✗ Attempt {attempt} failed, retrying...\n")
            time.sleep(1)
```

**How it works:**
1. Takes a function to execute
2. Tries to run it
3. If it fails with `TimeoutException`, waits 1 second and retries
4. If all retries fail, displays a **user-friendly error message** and exits
5. If succeeds, returns the function result

**Why use `sys.exit(1)` instead of raising exception?**
- **More user-friendly:** No scary stacktrace for non-technical users
- **Clean termination:** Program exits gracefully with error code 1
- **Clear messaging:** Users see exactly what went wrong and how to fix it
- **Professional:** Looks polished instead of crashed

**Error message breakdown:**
```python
sys.exit(1)  # Exit code 1 = error (0 = success)
```
- Exit codes tell the operating system if program succeeded
- Code 0 = Success
- Code 1+ = Error occurred
- Useful for automation and scripting

**Example output when all retries fail:**
```
Trying Login. Attempt: 1/7
✗ Attempt 1 failed, retrying...

Trying Login. Attempt: 2/7
✗ Attempt 2 failed, retrying...

...

Trying Login. Attempt: 7/7

======================================================================
❌ ERROR: Login Failed After 7 Attempts
======================================================================
Reason: Network timeout - the page did not load in time

Possible causes:
  • Internet connection is slow or unstable
  • Gym website is down or not responding
  • Firewall or antivirus blocking connection

Please check your connection and try again.
======================================================================
```

**Why this pattern is powerful:**
- Network issues are temporary (retry often fixes them)
- Makes any function retryable
- Centralized retry logic (don't repeat code)
- Configurable retry count
- **Graceful failure** with helpful guidance

**Example usage:**
```python
retry_with_attempts(login, retries=7, description="Login")
# Tries login() up to 7 times before exiting with friendly message
```

---

### Part 6: Click Until Success Function

```python
def click_until_text_changes(button, max_attempts=5):
    initial_text = button.text

    for attempt in range(1, max_attempts + 1):
        try:
            button.click()
            time.sleep(2)
            
            current_text = button.text
            if current_text != initial_text:
                print(f"  ✓ Success! Button changed to '{current_text}'")
                return True
            else:
                print(f"  ✗ No change detected, retrying...")
        except Exception as e:
            print(f"  ✗ Error: {e}")
            time.sleep(0.5)
    
    return False
```

**Algorithm explanation:**
1. Save button's initial text (e.g., "Book Class")
2. Click the button
3. Wait 2 seconds for server response
4. Check if button text changed (e.g., to "Booked")
5. If changed → Success! Return True
6. If not changed → Network probably failed, retry
7. After 5 attempts → Give up, return False

**Why check text change?**
- Gym site has 50% network failure rate
- Click might not register on server
- Button text change = definitive proof click worked
- More reliable than assuming click succeeded

**Real-world scenario:**
```
Attempt 1: Click → "Book Class" (no change) → retry
Attempt 2: Click → "Book Class" (no change) → retry
Attempt 3: Click → "Booked" (changed!) → success
```

---

### Part 7: Login Function

```python
def login():
    # Click login button
    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()
    
    time.sleep(0.5)

    # Enter email
    email_input = driver.find_element(By.ID, "email-input")
    email_input.clear()
    email_input.send_keys(ACCOUNT_EMAIL)

    # Enter password
    password_input = driver.find_element(By.ID, "password-input")
    password_input.clear()
    password_input.send_keys(ACCOUNT_PASSWORD)

    # Submit
    submit_button = driver.find_element(By.ID, "submit-button")
    submit_button.click()

    # Wait for schedule page (confirms login success)
    wait = WebDriverWait(driver, timeout=5)
    wait.until(EC.presence_of_element_located((By.ID, "schedule-page")))
```

**Step by step:**
1. Find and click "Login" button
2. Wait briefly for modal to appear
3. Find email input field, clear any existing text, type email
4. Find password input, clear it, type password
5. Click submit button
6. **Critical:** Wait for schedule page to load

**Why wait for schedule page?**
- Confirms login actually succeeded
- If wait times out → login failed → retry
- Prevents moving to next step before ready
- Common pattern in automation

---

### Part 8: Book Classes Function - Scanning Schedule

```python
def book_classes():
    schedule_days = driver.find_elements(By.CLASS_NAME, "Schedule_dayGroup__y79__")
    
    class_bookings = []
    new_button_status = ""
    booked_count = 0
    processed_classes = 0
    
    for day_group in schedule_days:
        date_heading = day_group.find_element(By.TAG_NAME, "h2").text
        
        # Parse dates like "Today (Tue, Jan 15)"
        if "Tomorrow" in date_heading or "Today" in date_heading:
            start_idx = date_heading.index("(") + 1
            end_idx = date_heading.index(")")
            date_heading = date_heading[start_idx:end_idx]
        
        # Check if this is Tuesday or Thursday
        if any(day in date_heading for day in TARGET_DAYS):
            # Process this day...
```

**What's happening:**
1. Find all day groups on schedule page
2. For each day, extract the date heading
3. Handle special cases like "Today" and "Tomorrow"
4. Check if it's a target day (Tue or Thu)

**Parsing example:**
```
Raw text: "Today (Tue, Jan 15)"
After extraction: "Tue, Jan 15"
```

**Why use `any()`?**
```python
any(day in date_heading for day in TARGET_DAYS)
# Returns True if EITHER "Tue" OR "Thu" is in the heading
# Cleaner than: "Tue" in date_heading or "Thu" in date_heading
```

---

### Part 9: Finding and Booking Classes

```python
class_cards = day_group.find_elements(By.CLASS_NAME, "ClassCard_card__KpCx5")

for card in class_cards:
    class_time_raw = card.find_element(By.TAG_NAME, "p").text
    class_time = class_time_raw.replace("Time: ", "")
    class_name = card.find_element(By.TAG_NAME, "h3").text
    
    if class_time == TARGET_TIME:
        booking_button = card.find_element(By.TAG_NAME, "button")
        button_status = booking_button.text
        
        if button_status not in ["Booked", "Waitlisted"]:
            print(f"📋 Attempting to book: {class_name}")
            click_until_text_changes(booking_button, max_attempts=5)
            button_status = booking_button.text
```

**Step by step:**
1. Find all class cards for this day
2. Loop through each class card
3. Extract time (remove "Time: " prefix)
4. Extract class name
5. Check if it's 6:00 PM (our target)
6. Find the booking button
7. Check button status
8. If not already booked/waitlisted, attempt booking
9. Update status after clicking

**Why check status first?**
- Don't waste clicks on already-booked classes
- Prevents unnecessary network requests
- Makes bot more efficient
- Avoids potential issues with double-booking

---

### Part 10: Tracking Booking Status

```python
if new_button_status:
    if new_button_status == "Waitlisted":
        print(f"⏳ Joined waitlist: {class_name} on {full_date}")
        waitlist_count += 1
    else:
        print(f"✓ Successfully booked: {class_name} on {full_date}")
        booked_count += 1
elif button_status == "Waitlisted":
    print(f"⏳ Already Waitlisted: {class_name} on {full_date}")
    already_booked_count += 1
else:
    print(f"✓ Already booked: {class_name} on {full_date}")
    already_booked_count += 1   

class_bookings.append({
    "class_name": class_name,
    "day": day_abbrev,
    "date": full_date,
    "status": button_status
})
```

**Button status meanings:**
- **"Book Class"** → Available, needs booking
- **"Booked"** → Already booked previously
- **"Waitlisted"** → Already on waitlist
- **"Join Waitlist"** → Class full, can join waitlist

**Data structure:**
Each booking is stored as a dictionary:
```python
{
    "class_name": "Yoga",
    "day": "Tue",
    "date": "Tue, Jan 15",
    "status": "Booked"
}
```

This allows tracking and verification later.

---

### Part 11: Day Name Conversion

```python
for day_name in DAYS_OF_THE_WEEK:
    for booking in class_bookings:
        if booking["day"] in day_name:
            booking["day"] = day_name
```

**What this does:**
- Converts "Tue" → "Tuesday"
- Converts "Thu" → "Thursday"

**How it works:**
- `DAYS_OF_THE_WEEK` = `["Monday", "Tuesday", ..., "Sunday"]`
- Checks if "Tue" is in "Tuesday" (True!)
- Replaces abbreviated name with full name

**Why do this?**
- More readable in reports
- Professional output
- Consistent formatting

---

### Part 12: Booking Summary

```python
print("\n" + "="*70)
print("BOOKING SUMMARY")
print("="*70)

if len(class_bookings) > 1:
    days_processed = f"{class_bookings[0]['day']}/{class_bookings[1]['day']}"
elif len(class_bookings) == 1:
    days_processed = class_bookings[0]['day']
else:
    days_processed = "None"

print(f"Days processed: {days_processed}")
print(f"Target time: {TARGET_TIME}")
print(f"Total classes processed: {processed_classes}")
print(f"New bookings: {booked_count}")
print(f"New Waitlists: {waitlist_count}")
print(f"Already booked: {already_booked_count}")
```

**Logic explained:**
- If 2+ bookings: Show "Tuesday/Thursday"
- If 1 booking: Show just that day
- If 0 bookings: Show "None"

**Sample output:**
```
======================================================================
BOOKING SUMMARY
======================================================================
Days processed: Tuesday/Thursday
Target time: 6:00 PM
Total classes processed: 2
New bookings: 2
Waitlisted: 0
Already booked: 0
```

---

### Part 13: Verification on My Bookings Page

```python
my_bookings_link = driver.find_element(By.ID, "my-bookings-link")
my_bookings_link.click()
time.sleep(1)

booking_cards = driver.find_elements(By.CLASS_NAME, "MyBookings_bookingCard__VRdrR")

for card in booking_cards:
    class_name = card.find_element(By.TAG_NAME, "h3").text
    reserve_button = card.find_element(By.TAG_NAME, "button")
    reserve_type = reserve_button.text.split()[1]
    
    verified_bookings.append({
        "class_name": class_name