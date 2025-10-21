import time

from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import os

load_dotenv()
GOOGLE_FORM = os.environ["GOOGLE_FORM"]


# User-Agent Header to identify the browser making the request
HEADER = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/140.0.0.0 Safari/537.36"
}

# Billboard Hot 100 chart URL with the specified date
URL = "https://appbrewery.github.io/Zillow-Clone/"

# Fetch and parse Billboard webpage
try:
    response = requests.get(url=URL, headers=HEADER)
    response.encoding = "utf-8"
    response.raise_for_status()  # Raise error for bad status codes
    billboard_html = response.text
except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")
    exit()

# Parse HTML content with BeautifulSoup
soup = BeautifulSoup(billboard_html, features="html.parser")

with open(file="zillow_data.html", mode="w", encoding="utf-8") as file:
    file.write(soup.prettify())

# property_links_raw = soup.find_all()
property_tags = soup.find_all(name="a", attrs={'data-test':'property-card-link'})
property_tag_prices = soup.find_all(name="span", attrs={'data-test':'property-card-price'})

property_prices = []
property_links = []
property_addresses = []
for n in range(len(property_tags)):
    if n % 2 == 0:
        property_links.append(property_tags[n].get('href'))
        property_addresses.append(property_tags[n].text.strip())

for n in range(len(property_tag_prices)):
    property_prices.append(
        property_tag_prices[n].text[:6].replace("+", "")
    )

# Configure Webdriver

# Configure Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option(name="detach", value=True)

# Initialize Chrome driver
driver = webdriver.Chrome(options=chrome_options)

# Navigate to the webpage
driver.get(url=GOOGLE_FORM)

# Function to wait until a element be available
def until_be_clickeable(web_driver, by):
    return WebDriverWait(web_driver, timeout=10).until(
        ec.element_to_be_clickable(by)
    )

answer_inputs = driver.find_elements(by=By.CSS_SELECTOR, value='input[type="text"]')

for n in range(len(property_addresses)):
    time.sleep(0.5)
    answer_inputs = driver.find_elements(by=By.CSS_SELECTOR, value='input[type="text"]')
    time.sleep(0.5)
    answer_inputs[0].send_keys(property_addresses[n])
    time.sleep(0.5)
    answer_inputs[1].send_keys(property_prices[n])
    time.sleep(0.5)
    answer_inputs[2].send_keys(property_links[n])
    time.sleep(0.5)

    wait_until_be_clickeable_submit_button = until_be_clickeable(web_driver=driver, by=(By.CSS_SELECTOR, "div[jsname='M2UYVd']"))
    wait_until_be_clickeable_submit_button.click()

    time.sleep(2)

    wait_until_be_clickeable_submit_another_response = until_be_clickeable(web_driver=driver, by=(By.CSS_SELECTOR, "div.c2gzEf a"))
    wait_until_be_clickeable_submit_another_response.click()