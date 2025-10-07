from selenium.webdriver.common.by import By
from selenium import webdriver
import json


# Keep Chrome browser open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option(name="detach", value=True)

driver = webdriver.Chrome(options=chrome_options)

URL = "https://www.python.org/"

driver.get(url=URL)

# event_name_tags = driver.find_element(
#     by=By.XPATH,
#     value='//*[@id="content"]/div/section/div[2]/div[2]/div/ul').text.split("\n")

# event_names = [event_name_tags[idx] for idx in range(len(event_name_tags)) if idx % 2 != 0]

event_name_tags = driver.find_elements(by=By.CSS_SELECTOR, value=".event-widget li a")
event_date_tags = driver.find_elements(by=By.CSS_SELECTOR, value=".event-widget li time")

event_dates = [event_date_tags[idx].get_attribute("datetime").split("T")[0] for idx in range(len(event_date_tags))]
event_names = [event_name_tags[idx].text for idx in range(len(event_name_tags))]

events = {idx: {'time': event_dates[idx], 'name': event_names[idx]} for idx in range(len(event_names))}

print(json.dumps(events, indent=4))


driver.quit()