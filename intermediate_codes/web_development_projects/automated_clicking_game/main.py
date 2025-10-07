from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time

# Keep Chrome browser open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option(name="detach", value=True)

# Create a driver
driver = webdriver.Chrome(options=chrome_options)

# Navigate to the webpage
URL = "https://ozh.github.io/cookieclicker/"
driver.get(url=URL)
time.sleep(5)

language = driver.find_element(by=By.XPATH, value='//*[@id="langSelect-EN"]')
language.click()
time.sleep(2)

playing = True
big_cookie = driver.find_element(by=By.CSS_SELECTOR, value="button#bigCookie")

t = 0
upgrades = []
while playing:
    big_cookie.click()

    t += 1
    upgrades = []
    cookies = int(driver.find_element(by=By.ID, value="cookies").text.split()[0].replace(",", ""))
    cookies_second = float(driver.find_element(
            by=By.ID,
            value="cookies").text.split()[4].replace(".", "")
    )

    upgrade_cursor = driver.find_element(by=By.ID, value="product0")
    upgrade_grandma = driver.find_element(by=By.ID, value="product1")
    upgrade_farm = driver.find_element(by=By.ID, value="product2")

    upgrade_button = [upgrade_cursor, upgrade_grandma, upgrade_farm]



    if t >= 15:
        price_upgrade_cursor = driver.find_element(by=By.ID, value="productPrice0").text
        upgrades.append(int(price_upgrade_cursor.replace(",", "")))

    if t >= 100:
        price_upgrade_grandma = driver.find_element(by=By.ID, value="productPrice1").text
        upgrades.append(int(price_upgrade_grandma.replace(",", "")))


    if cookies >= 1100:
        price_upgrade_farm = driver.find_element(by=By.ID, value="productPrice2").text
        upgrades.append(int(price_upgrade_farm.replace(",", "")))
        print(price_upgrade_farm)

    if len(upgrades) > 1 and cookies > max(upgrades):
        upgrade_button[upgrades.index(max(upgrades))].click()

    if t == 360:
        print(f"cookies/second: {cookies_second}")
        exit()
        driver.quit()

