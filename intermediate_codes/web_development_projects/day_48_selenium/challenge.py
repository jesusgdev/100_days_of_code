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
URL = "https://secure-retreat-92358.herokuapp.com/"
driver.get(url=URL)

first_name_field = driver.find_element(by=By.NAME, value="fName")

first_name_field.send_keys("Jesus")

last_name_field = driver.find_element(by=By.NAME, value="lName")

last_name_field.send_keys("Garcia")

email_field = driver.find_element(by=By.NAME, value="email")

email_field.send_keys("jesusgpythondev@gmail.com")

sign_up_button = driver.find_element(by=By.CSS_SELECTOR, value="form button")

sign_up_button.click()

# Tab Method

# first_name_field = driver.find_element(by=By.NAME, value="fName")
# last_name_field = driver.find_element(by=By.NAME, value="lName")
# email_field = driver.find_element(by=By.NAME, value="email")
# sign_up_button = driver.find_element(by=By.CSS_SELECTOR, value="form button")
# time.sleep(2)
# first_name_field.send_keys("Jesus")
# time.sleep(2)
# first_name_field.send_keys(Keys.TAB)
# time.sleep(2)
# last_name_field.send_keys("Garcia")
# time.sleep(2)
# last_name_field.send_keys(Keys.TAB)
# time.sleep(2)
# email_field.send_keys("jesusgpythondev@gmail.com")
# time.sleep(2)
# email_field.send_keys(Keys.TAB)
# time.sleep(2)
# sign_up_button.click()