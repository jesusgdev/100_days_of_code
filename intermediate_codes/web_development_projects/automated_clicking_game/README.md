# Cookie Clicker Bot - Automated Game Player

An automated bot that plays Cookie Clicker using Selenium WebDriver. The bot clicks the cookie, monitors available upgrades, and purchases the most expensive affordable upgrade to maximize cookie production.

---

## Project Overview

This project demonstrates web automation using Selenium to:
1. Automatically click the cookie to generate cookies
2. Monitor available upgrades in real-time
3. Intelligently purchase the most expensive affordable upgrade
4. Track game statistics (cookies per second, total upgrades)

**Use Case:** Learn web automation, Selenium basics, and game bot development.

---

## Table of Contents

- [Requirements](#requirements)
- [Installation Guide](#installation-guide)
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
- **ChromeDriver** (matching your Chrome version)
- Basic understanding of Python

### Required Libraries

```bash
pip install selenium
```

**What Selenium does:**
- Controls web browsers programmatically
- Simulates user interactions (clicks, typing, etc.)
- Extracts data from web pages

---

## Installation Guide

### Step 1: Install Python

Download and install Python from [python.org](https://www.python.org/downloads/)

Verify installation:
```bash
python --version
# Should show Python 3.7 or higher
```

### Step 2: Install Selenium

```bash
pip install selenium
```

### Step 3: Install ChromeDriver

**Option A: Automatic (Recommended)**

Selenium 4+ includes automatic driver management. No manual installation needed!

**Option B: Manual Installation**

1. Check your Chrome version: `chrome://version/` in Chrome
2. Download matching ChromeDriver from [chromedriver.chromium.org](https://chromedriver.chromium.org/downloads)
3. Add ChromeDriver to your system PATH

**Linux/Mac:**
```bash
# Move to /usr/local/bin
sudo mv chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
```

**Windows:**
- Place `chromedriver.exe` in `C:\Windows\System32\`
- Or add its folder to PATH environment variable

### Step 4: Verify Installation

```python
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.google.com")
print("Selenium working!")
driver.quit()
```

If this runs without errors, you're ready!

---

## How to Run

### Basic Execution

```bash
python main.py
```

The bot will:
1. Open Chrome browser
2. Navigate to Cookie Clicker
3. Start clicking automatically
4. Buy upgrades when possible
5. Display statistics after 5000 clicks

### Customizing Settings

Edit these constants at the top of the file:

```python
TOTAL_CLICKS = 5000              # Change to 10000 for longer gameplay
UPGRADE_CHECK_INTERVAL = 100     # Check upgrades every 100 clicks
LANGUAGE = "EN"                  # Language: EN, ES, FR, etc.
```

---

## Complete Code Walkthrough

### Part 1: Imports

```python
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
```

**What we're importing:**
- `time`: Add delays between actions
- `webdriver`: Control Chrome browser
- `By`: Specify how to find elements (ID, CSS, XPath)
- `WebDriverWait`: Wait for elements to load
- `EC`: Expected conditions for smart waiting

---

### Part 2: Configuration

```python
GAME_URL = "https://ozh.github.io/cookieclicker/"
TOTAL_CLICKS = 5000
UPGRADE_CHECK_INTERVAL = 100
LANGUAGE = "EN"
```

**Why use constants?**
- Easy to modify without digging through code
- Makes the code self-documenting
- Professional coding practice
- Values in one place at the top

---

### Part 3: Chrome Driver Setup

```python
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option(name="detach", value=True)
driver = webdriver.Chrome(options=chrome_options)
```

**Line by line:**
1. `ChromeOptions()`: Create a configuration object for Chrome
2. `add_experimental_option("detach", True)`: Keep browser open after script ends
3. `webdriver.Chrome(options=chrome_options)`: Launch Chrome with settings

**Without "detach":** Browser closes immediately when script finishes

---

### Part 4: Load Game and Select Language

```python
driver.get(GAME_URL)
time.sleep(5)

try:
    wait = WebDriverWait(driver, 10)
    language_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, f'//*[@id="langSelect-{LANGUAGE}"]'))
    )
    language_button.click()
    time.sleep(2)
except Exception as e:
    print(f"Warning: Could not select language - {e}")
```

**Step by step:**
1. `driver.get(GAME_URL)`: Navigate to the game URL
2. `time.sleep(5)`: Wait 5 seconds for page to fully load
3. `WebDriverWait(driver, 10)`: Wait up to 10 seconds for elements
4. `EC.element_to_be_clickable()`: Wait until language button is clickable
5. `By.XPATH`: Find element using XPath selector
6. `f'//*[@id="langSelect-{LANGUAGE}"]'`: Dynamic XPath using f-string
7. `.click()`: Click the language button
8. `try-except`: Handle errors gracefully (language button might not exist)

**What is XPath?**
- A query language for selecting elements in HTML/XML
- More powerful than CSS selectors
- Example: `//*[@id="langSelect-EN"]` finds element with id="langSelect-EN"

---

### Part 5: Locate the Big Cookie

```python
big_cookie = driver.find_element(By.CSS_SELECTOR, "button#bigCookie")
```

**Explanation:**
- `find_element()`: Find ONE element (returns first match)
- `By.CSS_SELECTOR`: Use CSS selector syntax
- `"button#bigCookie"`: Find `<button>` with id="bigCookie"
- Result: A WebElement object you can interact with

**CSS Selector syntax:**
- `#id` → Find by ID
- `.class` → Find by class
- `button#bigCookie` → Button element with ID "bigCookie"

---

### Part 6: Main Game Loop

```python
click_count = 0
total_upgrades_bought = 0

while click_count < TOTAL_CLICKS:
    big_cookie.click()
    click_count += 1
    
    if click_count % UPGRADE_CHECK_INTERVAL == 0:
        # Check for upgrades...
```

**Logic flow:**
1. Initialize counters to zero
2. Loop until we reach TOTAL_CLICKS (5000)
3. Click the cookie on every iteration
4. Increment click counter
5. Every 100 clicks, check for upgrades (using modulo `%`)

**What is modulo (`%`)?**
- Returns remainder of division
- `100 % 100 = 0` ✓ (check upgrades)
- `101 % 100 = 1` (skip)
- `200 % 100 = 0` ✓ (check upgrades)

---

### Part 7: Get Cookie Count

```python
cookies_text = driver.find_element(By.ID, "cookies").text.split()[0]
cookies = int(cookies_text.replace(",", ""))
```

**Step by step:**
1. `driver.find_element(By.ID, "cookies")`: Find element with id="cookies"
2. `.text`: Get the text content (e.g., "1,234 cookies per second : 56")
3. `.split()[0]`: Split by spaces, take first part ("1,234")
4. `.replace(",", "")`: Remove commas ("1234")
5. `int()`: Convert string to integer (1234)

**Example transformation:**
```
"1,234 cookies per second : 56"
↓ .split()[0]
"1,234"
↓ .replace(",", "")
"1234"
↓ int()
1234
```

---

### Part 8: Find Available Upgrades

```python
upgrades = driver.find_elements(
    By.CSS_SELECTOR, 
    "div.product.unlocked.enabled"
)
```

**Explanation:**
- `find_elements()` (plural): Find ALL matching elements
- Returns a list of WebElements
- `"div.product.unlocked.enabled"`: div with ALL three classes
  - `product`: Base class for all upgrades
  - `unlocked`: Upgrade is visible
  - `enabled`: You have enough cookies to buy it

**Why check `len(upgrades) >= 2`?**
- Early game has only 1 upgrade (Cursor)
- We want at least 2 to compare prices
- Ensures the bot makes smart decisions

---

### Part 9: Collect Upgrade Information

```python
upgrade_data = []

for upgrade in upgrades:
    # Extract upgrade name
    name_element = upgrade.find_element(By.CLASS_NAME, "productName")
    name = name_element.text
    
    # Extract upgrade price
    price_element = upgrade.find_element(By.CLASS_NAME, "price")
    price_text = price_element.text.replace(",", "")
    
    try:
        price = int(price_text)
    except ValueError:
        continue
    
    upgrade_data.append({
        'element': upgrade,
        'name': name,
        'price': price
    })
```

**Step by step:**
1. Create empty list to store upgrade data
2. Loop through each upgrade element
3. Find child element with class "productName"
4. Extract name text (e.g., "Grandma")
5. Find child element with class "price"
6. Clean price text (remove commas)
7. Try to convert to integer
8. If conversion fails (invalid price), skip this upgrade
9. Store dictionary with element reference, name, and price

**Why use `.find_element()` on upgrade?**
- Searches WITHIN that specific upgrade div
- Prevents getting wrong prices from other upgrades
- More precise than global search

**What is a dictionary?**
```python
{
    'element': <WebElement>,  # The clickable element
    'name': "Grandma",         # Human-readable name
    'price': 100               # Cost in cookies
}
```

---

### Part 10: Find Best Upgrade

```python
best_upgrade = None
max_affordable_price = 0

for data in upgrade_data:
    if data['price'] <= cookies and data['price'] > max_affordable_price:
        max_affordable_price = data['price']
        best_upgrade = data
```

**Algorithm explanation:**
1. Start with no best upgrade (`None`)
2. Start with price of 0 as the maximum
3. Loop through all collected upgrades
4. Check two conditions:
   - Can we afford it? (`data['price'] <= cookies`)
   - Is it more expensive than current best? (`data['price'] > max_affordable_price`)
5. If both true, this becomes the new best upgrade
6. Continue until all upgrades checked

**Example:**
```
Cookies available: 1000

Upgrades:
- Cursor: 15 cookies ✓ affordable, but cheap
- Grandma: 100 cookies ✓ affordable, more expensive → BEST so far
- Farm: 500 cookies ✓ affordable, more expensive → NEW BEST
- Factory: 3000 cookies ✗ too expensive

Result: Buy Farm (most expensive we can afford)
```

**Why buy the most expensive?**
- More expensive upgrades give better production rates
- Maximizes cookies per second growth
- More efficient strategy than buying cheapest first

---

### Part 11: Purchase Upgrade

```python
if best_upgrade:
    best_upgrade['element'].click()
    total_upgrades_bought += 1
    print(f"[Click {click_count}] Bought: {best_upgrade['name']} "
          f"for {best_upgrade['price']:,} cookies "
          f"(Total upgrades: {total_upgrades_bought})")
    time.sleep(0.5)
```

**Step by step:**
1. Check if we found a best upgrade (`if best_upgrade:`)
2. Click the upgrade element to purchase it
3. Increment total upgrades counter
4. Print formatted purchase information
5. Wait 0.5 seconds for purchase animation

**F-string formatting tricks:**
- `f"Bought: {best_upgrade['name']}"` → Insert variable value
- `{best_upgrade['price']:,}` → Add thousand separators (1,000)
- Multi-line f-string for readability

**Output example:**
```
[Click 200] Bought: Grandma for 100 cookies (Total upgrades: 1)
[Click 400] Bought: Farm for 500 cookies (Total upgrades: 2)
```

---

### Part 12: Error Handling

```python
except Exception as e:
    print(f"Error during upgrade check: {e}")
    continue
```

**Why error handling is important:**
- Web pages change dynamically
- Elements might disappear or move
- Network issues can occur
- Prevents entire script from crashing

**What happens:**
1. If ANY error occurs in the try block
2. Catch it as variable `e`
3. Print the error message
4. `continue`: Skip to next loop iteration
5. Bot keeps running despite errors

---

### Part 13: Final Statistics

```python
try:
    cookies_text = driver.find_element(By.ID, "cookies").text.split()[0]
    final_cookies = int(cookies_text.replace(",", ""))
    
    cps_text = driver.find_element(By.ID, "cookies").text.split()[4]
    cookies_per_second = float(cps_text.replace(".", "").replace(",", "."))
    
    print(f"Total clicks: {click_count:,}")
    print(f"Total upgrades purchased: {total_upgrades_bought}")
    print(f"Final cookies: {final_cookies:,}")
    print(f"Cookies per second: {cookies_per_second:,.1f}")
    
except Exception as e:
    print(f"Could not retrieve final statistics: {e}")
```

**Explanation:**
1. Extract final cookie count (same method as before)
2. Extract cookies per second rate
   - `.split()[4]`: Get 5th word from text
   - Handle European number format (comma as decimal separator)
3. Print formatted statistics
4. Use `:,` for thousands separator
5. Use `:.1f` for one decimal place in float

**Example output:**
```
======================================================================
GAME COMPLETED
======================================================================
Total clicks: 5,000
Total upgrades purchased: 12
Final cookies: 45,832
Cookies per second: 127.3
======================================================================
```

---

## How It Works

### Game Strategy

1. **Continuous Clicking:** Bot clicks cookie every iteration
2. **Periodic Checks:** Every 100 clicks, scan for upgrades
3. **Smart Purchasing:** Always buy most expensive affordable upgrade
4. **Efficiency:** Maximizes cookies per second growth rate

### Why This Strategy Works

Cookie Clicker uses exponential growth:
- Early game: Manual clicking dominates
- Mid game: First few upgrades make huge difference
- Late game: Upgrades compound for massive production

By prioritizing expensive upgrades, we skip inefficient small upgrades and accelerate growth.

### Algorithm Flow Chart

```
Start
  ↓
Click Cookie
  ↓
Increment Counter
  ↓
Counter % 100 == 0? → No → Back to Click Cookie
  ↓ Yes
Get Cookie Count
  ↓
Find Available Upgrades
  ↓
Collect Upgrade Data
  ↓
Find Most Expensive Affordable
  ↓
Purchase Upgrade
  ↓
Reached 5000 Clicks? → No → Back to Click Cookie
  ↓ Yes
Display Statistics
  ↓
End
```

---

## Troubleshooting

### Problem 1: "ChromeDriver not found"

**Cause:** ChromeDriver not installed or not in PATH

**Solution:**
```bash
# Option 1: Let Selenium handle it (Selenium 4+)
pip install --upgrade selenium

# Option 2: Install webdriver-manager
pip install webdriver-manager

# Then in code:
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
```

---

### Problem 2: "Element not found"

**Cause:** Page not fully loaded or element changed

**Solution:**
```python
# Add explicit wait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.ID, "cookies")))
```

---

### Problem 3: Chrome version mismatch

**Error:** "This version of ChromeDriver only supports Chrome version X"

**Solution:**
1. Update Chrome: `chrome://settings/help`
2. Update ChromeDriver to match
3. Or use webdriver-manager (auto-updates)

---

### Problem 4: Script clicks but doesn't buy upgrades

**Cause:** Game URL or HTML structure changed

**Debug steps:**
```python
# Add debug prints
print(f"Cookies available: {cookies}")
print(f"Upgrades found: {len(upgrades)}")
print(f"Upgrade data: {upgrade_data}")

# Verify selectors manually
driver.get(GAME_URL)
time.sleep(5)
upgrades = driver.find_elements(By.CSS_SELECTOR, "div.product.unlocked.enabled")
print(f"Found {len(upgrades)} upgrades")
```

---

### Problem 5: Browser closes immediately

**Cause:** `detach` option not set

**Solution:** Ensure this line is present:
```python
chrome_options.add_experimental_option(name="detach", value=True)
```

---

## Improvements & Extensions

### Beginner Extensions

1. **Adjustable speed:**
```python
CLICK_DELAY = 0.01  # Seconds between clicks
time.sleep(CLICK_DELAY)
```

2. **Save statistics to file:**
```python
with open('game_stats.txt', 'w') as f:
    f.write(f"Clicks: {click_count}\n")
    f.write(f"Upgrades: {total_upgrades_bought}\n")
```

3. **Visual progress bar:**
```python
print(f"Progress: {click_count}/{TOTAL_CLICKS} [{click_count/TOTAL_CLICKS*100:.1f}%]")
```

4. **Buy golden cookies:**
```python
golden_cookie = driver.find_element(By.ID, "goldenCookie")
if golden_cookie.is_displayed():
    golden_cookie.click()
```

### Intermediate Extensions

1. **Multiple strategies:**
```python
STRATEGY = "expensive"  # or "cheap" or "balanced"

if STRATEGY == "expensive":
    # Buy most expensive
elif STRATEGY == "cheap":
    # Buy cheapest for frequency
```

2. **Database tracking:**
```python
import sqlite3
# Track game history over multiple runs
```

3. **Adaptive timing:**
```python
# Check upgrades more frequently late game
interval = max(10, 100 - (click_count // 100))
```

4. **Machine learning:**
```python
# Predict optimal purchase timing
# Train on historical data
```

### Advanced Extensions

1. **Multi-threading:**
```python
import threading
# Separate threads for clicking and buying
```

2. **Web dashboard:**
```python
from flask import Flask
# Real-time statistics web interface
```

3. **Computer vision:**
```python
import cv2
# Detect golden cookies by image recognition
```

4. **Cloud deployment:**
- Run bot 24/7 on AWS/Heroku
- Scheduled execution with cron jobs

---

## Project Structure

```
cookie-clicker-bot/
│
├── main.py              # Main bot script
├── requirements.txt     # Dependencies
├── README.md           # This documentation
└── .gitignore          # Git ignore file
```

### requirements.txt
```
selenium==4.15.2
```

### .gitignore
```
__pycache__/
*.pyc
*.pyo
.DS_Store
```

---

## Concepts Learned

### Python Concepts

✓ **While loops** - Continuous execution until condition met
✓ **If statements** - Conditional logic and decision making
✓ **Modulo operator** - Periodic actions with `%`
✓ **Try-except blocks** - Error handling and recovery
✓ **Lists and dictionaries** - Data structure management
✓ **F-strings** - Modern string formatting
✓ **Functions and imports** - Code organization

### Selenium Concepts

✓ **WebDriver setup** - Browser automation initialization
✓ **Element location** - Finding elements by ID, class, CSS selector
✓ **Element interaction** - Clicking, reading text
✓ **Explicit waits** - Smart waiting for elements
✓ **Multiple elements** - Working with lists of elements
✓ **Child element search** - Finding elements within elements

### Web Development Concepts

✓ **DOM structure** - HTML element hierarchy
✓ **CSS selectors** - Targeting specific elements
✓ **XPath queries** - Alternative element selection
✓ **Dynamic content** - Handling changing web pages
✓ **Class attributes** - Understanding multiple classes

### Algorithmic Thinking

✓ **Greedy algorithm** - Always choosing best immediate option
✓ **Data collection** - Gathering information before decisions
✓ **Comparison logic** - Finding maximum values
✓ **Loop optimization** - Balancing speed vs. resource checking

---

## Best Practices Demonstrated

### Code Quality

- **Constants at top:** Easy configuration
- **Descriptive names:** `click_count` not `c`
- **Comments:** Explain WHY, not just WHAT
- **Error handling:** Graceful failure recovery
- **Logging:** Track bot actions with prints

### Performance

- **Periodic checking:** Don't check upgrades every click
- **Smart waiting:** Use WebDriverWait instead of sleep
- **Resource cleanup:** Properly quit driver
- **Efficient selectors:** CSS faster than XPath

### Maintainability

- **Modular logic:** Clear separation of concerns
- **Magic numbers as constants:** No hardcoded values
- **Documentation:** Comprehensive README
- **Version control ready:** .gitignore included

---

## Legal & Ethical Considerations

### Educational Purpose

This bot is designed for:
- Learning Selenium web automation
- Understanding bot development concepts
- Practicing Python programming
- Educational experimentation

### Responsible Use

- Don't use on multiplayer games (unfair advantage)
- Respect website Terms of Service
- Don't overload servers with requests
- Use only on games that allow automation
- Cookie Clicker is single-player and bot-friendly

### Rate Limiting

The bot includes delays to be respectful:
- 0.5 second pause after purchases
- Checks upgrades every 100 clicks, not every click
- Doesn't spam the server

---

## Additional Resources

### Selenium Documentation
- [Official Selenium Docs](https://www.selenium.dev/documentation/)
- [Selenium with Python](https://selenium-python.readthedocs.io/)
- [WebDriver API](https://www.selenium.dev/documentation/webdriver/)

### Cookie Clicker
- [Official Game](https://orteil.dashnet.org/cookieclicker/)
- [Cookie Clicker Wiki](https://cookieclicker.fandom.com/wiki/Cookie_Clicker_Wiki)
- [Game Mechanics](https://cookieclicker.fandom.com/wiki/Building)

### Python Resources
- [Python Official Tutorial](https://docs.python.org/3/tutorial/)
- [Real Python](https://realpython.com/)
- [Automate the Boring Stuff](https://automatetheboringstuff.com/)

---

## FAQ

**Q: Why does the bot keep browser open?**
A: The `detach=True` option is set for debugging. Remove it to auto-close.

**Q: Can I run this 24/7?**
A: Yes, but cookies are saved in browser memory. Close and reopen to reset.

**Q: How do I make it faster?**
A: Reduce `UPGRADE_CHECK_INTERVAL` or add multi-threading (advanced).

**Q: Does it work on the official Cookie Clicker?**
A: Yes! Change `GAME_URL` to `https://orteil.dashnet.org/cookieclicker/`

**Q: Can I get banned?**
A: No, Cookie Clicker is single-player and bot-friendly.

**Q: Why buy expensive upgrades first?**
A: Exponential growth means expensive upgrades have better ROI.

---

## Conclusion

Congratulations! You've learned:
- Web automation with Selenium
- DOM manipulation and element location
- Algorithm design for game optimization
- Error handling and robust code practices
- Python programming fundamentals

This project provides a foundation for:
- Web scraping projects
- Automated testing
- Browser automation tasks
- Data collection from websites
- Advanced bot development

**Keep experimenting and happy coding!** 🍪🤖