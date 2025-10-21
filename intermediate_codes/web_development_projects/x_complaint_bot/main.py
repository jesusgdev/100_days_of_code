from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium import webdriver
from dotenv import load_dotenv
import time
import  os

load_dotenv()

PROMISED_DOWN = 150
PROMISED_UP = 10
CHROME_DRIVER_PATH = ""
X_EMAIL = os.environ["X_EMAIL"]
X_PASSWORD = os.environ["X_PASSWORD"]

# ==============================================================================
# SETUP CHROME DRIVER
# ==============================================================================

# Configure Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option(name="detach", value=True)

# Use persistent Chrome profile to save login sessions
user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

# Initialize Chrome driver
driver = webdriver.Chrome(options=chrome_options)

# Navigate to the webpage
URL = "https://x.com/"
driver.get(url=URL)

login = driver.find_element(by=By.LINK_TEXT, value="Sign in")
login.click()

# time.sleep(4)
#
# # wait = WebDriverWait(login, timeout=4)
# # wait.until(ec.presence_of_element_located((By.NAME, "text")))
#
# input_login = driver.find_element(by=By.NAME, value="text")
# input_login.send_keys(X_EMAIL)
#
# next_button = driver.find_element(by=By.XPATH, value='//button[contains(., "Next")]')
# next_button.click()