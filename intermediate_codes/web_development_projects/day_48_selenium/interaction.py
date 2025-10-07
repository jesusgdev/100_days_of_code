from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time

# Keep Chrome browser open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option(name="detach", value=True)

# Create a driver
driver = webdriver.Chrome(options=chrome_options)

# Navigate to the Wikipedia webpage
URL = "https://en.wikipedia.org/wiki/Main_Page"
driver.get(url=URL)

# Find anchor tag using a CSS selector
number_articles = driver.find_elements(by=By.CSS_SELECTOR, value="#articlecount a")[1]
# print(number_articles.text)

# Click the search icon to activate the search field
search_symbol = driver.find_element(By.XPATH, value='//*[@id="p-search"]/a/span[1]')
search_symbol.click()

# Locate the search input field
search = driver.find_element(By.NAME, value="search")

# Enter search query
search.send_keys("Python")

# Wait for search suggestions to load
time.sleep(2)

# Click the search button to submit
search_button = driver.find_element(By.CSS_SELECTOR, "button.cdx-search-input__end-button")
search_button.click()

time.sleep(2)
driver.quit()

