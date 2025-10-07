import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ==============================================================================
# CONFIGURATION
# ==============================================================================

# Game URL
GAME_URL = "https://ozh.github.io/cookieclicker/"

# Game settings
TOTAL_CLICKS = 5000  # Total clicks before stopping
UPGRADE_CHECK_INTERVAL = 100  # Check for upgrades every N clicks
LANGUAGE = "EN"  # Game language

# ==============================================================================
# SETUP CHROME DRIVER
# ==============================================================================

# Configure Chrome to stay open after script finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option(name="detach", value=True)

# Create Chrome driver instance
driver = webdriver.Chrome(options=chrome_options)

print("Starting Cookie Clicker Bot...")

# ==============================================================================
# STEP 1: Load game and select language
# ==============================================================================

driver.get(GAME_URL)
print(f"Loaded game: {GAME_URL}")

# Wait for page to load
time.sleep(5)

# Select language
try:
    wait = WebDriverWait(driver, 10)
    language_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, f'//*[@id="langSelect-{LANGUAGE}"]'))
    )
    language_button.click()
    print(f"Language set to: {LANGUAGE}")
    time.sleep(2)
except Exception as e:
    print(f"Warning: Could not select language - {e}")

# ==============================================================================
# STEP 2: Locate the big cookie
# ==============================================================================

big_cookie = driver.find_element(By.CSS_SELECTOR, "button#bigCookie")
print("Big cookie located. Starting automated clicking...")

# ==============================================================================
# STEP 3: Main game loop - Click and buy upgrades
# ==============================================================================

click_count = 0
total_upgrades_bought = 0

while click_count < TOTAL_CLICKS:
    # Click the big cookie
    big_cookie.click()
    click_count += 1

    # Periodically check for upgrades
    if click_count % UPGRADE_CHECK_INTERVAL == 0:
        try:
            # Get current cookie count
            cookies_text = driver.find_element(By.ID, "cookies").text.split()[0]
            cookies = int(cookies_text.replace(",", ""))

            # Find all available (unlocked and enabled) upgrades
            upgrades = driver.find_elements(
                By.CSS_SELECTOR,
                "div.product.unlocked.enabled"
            )

            # Only proceed if there are at least 2 upgrades available
            if len(upgrades) >= 2:
                # Collect upgrade information (name, price, element)
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
                        continue  # Skip if price is invalid

                    upgrade_data.append({
                        'element': upgrade,
                        'name': name,
                        'price': price
                    })

                # Find the most expensive upgrade we can afford
                best_upgrade = None
                max_affordable_price = 0

                for data in upgrade_data:
                    if cookies >= data['price'] > max_affordable_price:
                        max_affordable_price = data['price']
                        best_upgrade = data

                # Purchase the best upgrade if found
                if best_upgrade:
                    best_upgrade['element'].click()
                    total_upgrades_bought += 1
                    print(f"[Click {click_count}] Bought: {best_upgrade['name']} "
                          f"for {best_upgrade['price']:,} cookies "
                          f"(Total upgrades: {total_upgrades_bought})")
                    time.sleep(0.5)  # Brief pause after purchase

        except Exception as e:
            print(f"Error during upgrade check: {e}")
            continue

# ==============================================================================
# STEP 4: Display final statistics and cleanup
# ==============================================================================

print("\n" + "=" * 70)
print("GAME COMPLETED")
print("=" * 70)

try:
    # Get final cookie count
    cookies_text = driver.find_element(By.ID, "cookies").text.split()[0]
    final_cookies = int(cookies_text.replace(",", ""))

    # Get cookies per second
    cps_text = driver.find_element(By.ID, "cookies").text.split()[4]
    cookies_per_second = float(cps_text.replace(".", "").replace(",", "."))

    print(f"Total clicks: {click_count:,}")
    print(f"Total upgrades purchased: {total_upgrades_bought}")
    print(f"Final cookies: {final_cookies:,}")
    print(f"Cookies per second: {cookies_per_second:,.1f}")

except Exception as e:
    print(f"Could not retrieve final statistics: {e}")

print("=" * 70)

# Keep browser open for inspection
input("\nPress Enter to close the browser...")
driver.quit()