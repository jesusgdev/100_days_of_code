import os
import time
import smtplib
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ==============================================================================
# CONFIGURATION
# ==============================================================================

# Amazon product URL to track
PRODUCT_URL = ("https://www.amazon.com/-/es/Apple-Computadora-escritorio-"
               "mini-n%C3%BAcleos/dp/B0DLBTPDCS/ref=pd_ci_mcx_mh_mcx_"
               "views_0_title?pd_rd_w=n9pih&content-id=amzn1.sym.679481c3-"
               "2bf4-4843-80c0-ffb319282e84%3Aamzn1.symc.c3d5766d-b606-"
               "46b8-ab07-1d9d1da0638a&pf_rd_p=679481c3-2bf4-4843-80c0-"
               "ffb319282e84&pf_rd_r=SA3G88A923WSV95C0HR8&pd_rd_wg=HBML4&pd_"
               "rd_r=78d56093-a70d-48d3-93bf-34fc314bd942&pd_rd_"
               "i=B0DLBTPDCS&th=1")

# Target price threshold (send alert if product price falls below this)
TARGET_PRICE = 500.00

# HTTP headers to mimic a real browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/131.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

# ==============================================================================
# STEP 1: Fetch Amazon product page
# ==============================================================================

print("Fetching Amazon product page...")

try:
    response = requests.get(url=PRODUCT_URL, headers=HEADERS)
    time.sleep(2)  # Delay to avoid rate limiting
    response.encoding = "utf-8"
    response.raise_for_status()  # Raise exception for HTTP errors
    amazon_html = response.text
    print("Page fetched successfully")

except requests.exceptions.RequestException as e:
    print(f"Error fetching Amazon data: {e}")
    exit(1)

# ==============================================================================
# STEP 2: Parse HTML and extract product information
# ==============================================================================

print("Extracting product information...")

soup = BeautifulSoup(amazon_html, "html.parser")

# Extract product price
price_tag = soup.find("span", class_="a-price-whole")
if not price_tag:
    print("Error: Price not found on page")
    exit(1)

# Clean price text and convert to float
price_text = price_tag.get_text().strip().replace(",", "")
try:
    price = float(price_text)
except ValueError:
    print(f"Error: Could not convert price '{price_text}' to number")
    exit(1)

# Extract product title
title_tag = soup.find("span", class_="a-size-large product-title-word-break")
if not title_tag:
    print("Error: Product title not found on page")
    exit(1)

title = title_tag.get_text().strip()

print(f"Product: {title}")
print(f"Current price: ${price:.2f}")
print(f"Target price: ${TARGET_PRICE:.2f}")

# ==============================================================================
# STEP 3: Check if price meets threshold
# ==============================================================================

if price >= TARGET_PRICE:
    print(f"Price is above target. No alert sent.")
    exit(0)

print(f"Price alert! Product is below ${TARGET_PRICE:.2f}")

# ==============================================================================
# STEP 4: Load email credentials
# ==============================================================================

load_dotenv()

MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")

# Verify credentials are loaded
if not MY_EMAIL or not MY_PASSWORD:
    print("Error: Email credentials not found in .env file")
    exit(1)

# ==============================================================================
# STEP 5: Compose and send email alert
# ==============================================================================

print("Sending email alert...")

# Create email message
msg = MIMEMultipart()
msg['From'] = MY_EMAIL
msg['To'] = MY_EMAIL
msg['Subject'] = f"Amazon Price Alert: {title[:50]}..."

# Email body with product details
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

# Send email via Gmail SMTP
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

print("\n" + "=" * 70)
print("PRICE TRACKING COMPLETED")
print("=" * 70)