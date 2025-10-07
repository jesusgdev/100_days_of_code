from selenium.webdriver.common.by import By
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
upgrade_product_buttons = []
title_product_buttons = []
price_upgrades = []
while playing:
    big_cookie.click()
    t += 1

    cookies = int(driver.find_element(by=By.ID, value="cookies").text.split()[0].replace(",", ""))
    cookies_per_second = float(driver.find_element(
            by=By.ID,
            value="cookies").text.split()[4].replace(".", "")
                               )

    upgrades = driver.find_elements(by=By.CSS_SELECTOR, value="div.product.unlocked.enabled")
    if len(upgrades) > 1:
        title_product_buttons = []
        title_products = driver.find_elements(by=By.CSS_SELECTOR,
                                              value="div.product.unlocked.enabled div.title.productName")
        for idx in range(0, len(upgrades)):
            upgrade_product_buttons.append(upgrades[idx])
            title_product_buttons.append(title_products[idx].text)

    if t >= 100:
        price_upgrades = []
        price_u = driver.find_elements(by=By.CLASS_NAME, value="price")
        for idx in range(0, len(upgrades)):
            price_upgrades.append(int(price_u[idx].text.replace(",", "")))


    if len(price_upgrades) > 1 and cookies > max(price_upgrades) and cookies % 100 == 0:
        upgrade_product_buttons[price_upgrades.index(max(price_upgrades))].click()


    if t == 5000:
        print(f"cookies/second: {cookies_per_second}")
        driver.quit()
        exit()

