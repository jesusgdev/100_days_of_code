from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from selenium import webdriver
import time
import os

load_dotenv(dotenv_path=".env")
LOGIN_USERNAME = os.environ["LOGIN_USERNAME"]
LOGIN_PASSWORD = os.environ["LOGIN_PASSWORD"]
SIMILAR_ACCOUNT = os.environ["SIMILAR_ACCOUNT"]
URL = "https://www.instagram.com/"

class InstaFollower:
    def __init__(self):

        # Configure Chrome options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option(name="detach", value=True)

        # Initialize Chrome driver
        self.driver = webdriver.Chrome(options=chrome_options)

    def until_be_clickeable(self, driver, by):

        return WebDriverWait(driver, timeout=10).until(
            ec.element_to_be_clickable(by)
        )

    def login(self):

        # Navigate to the webpage
        self.driver.get(url=URL)

        login_ui = self.until_be_clickeable(
            driver=self.driver,
            by=(By.NAME, "username")
        )
        login_ui.send_keys(LOGIN_USERNAME)

        password_input = self.driver.find_element(
            by=By.NAME,
            value="password")
        password_input.send_keys(LOGIN_PASSWORD)

        wait_login_button = self.until_be_clickeable(
            driver=self.driver,
            by=(By.CSS_SELECTOR, "button[type='submit']")
        )
        wait_login_button.click()

        wait_save_login_ui = self.until_be_clickeable(
            driver=self.driver,
        by=(By.XPATH, "//div[text()='Not now']")
        )
        wait_save_login_ui.click()

    def find_followers(self):

        wait_for_search_label = self.until_be_clickeable(
            driver=self.driver,
            by=(By.CSS_SELECTOR, "a[href='#']")
        )

        wait_for_search_label.click()

        wait_for_search_input = self.until_be_clickeable(
            driver=self.driver,
            by=(By.CSS_SELECTOR, "input[aria-label='Search input']")
        )

        wait_for_search_input.click()
        wait_for_search_input.send_keys(SIMILAR_ACCOUNT)

        wait_for_link_account = self.until_be_clickeable(
            driver=self.driver,
            by=(By.CSS_SELECTOR, "a[href='/portraitgames/']")
        )
        wait_for_link_account.click()

        wait_for_found_followers = self.until_be_clickeable(
            driver=self.driver,
            by=(By.CSS_SELECTOR, "a[href='/portraitgames/followers/']")
        )
        wait_for_found_followers.click()

    def follow(self):
        time.sleep(2)

        for n in range(11):
            follow_buttons = self.driver.find_elements(
                by=By.CSS_SELECTOR,
                value="button._aswp._aswr._aswu._asw_._asx2"
            )

            label_button = self.driver.find_elements(
                by=By.CSS_SELECTOR,
                value="div._ap3a._aaco._aacw._aad6._aade"
            )

            for i in range(len(follow_buttons)):
                if label_button[i].text != "Following":
                    follow_buttons[i].click()
                    time.sleep(0.5)

            container = self.driver.find_element(
                by=By.XPATH,
                value="/html/body/div[5]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]"
            )
            container.send_keys(Keys.END)

            time.sleep(2)


        # Other option os def follow(self):
        # import random
        # from selenium.webdriver.common.action_chains import ActionChains
        #
        # def follow(self):
        #     time.sleep(random.uniform(3, 5))  # Espera inicial aleatoria
        #
        #     followed_count = 0
        #     max_follows = random.randint(8, 12)  # Número aleatorio de follows
        #
        #     print(f"Intentando seguir hasta {max_follows} cuentas...")
        #
        #     for n in range(15):  # Más iteraciones pero con límite de follows
        #         if followed_count >= max_follows:
        #             print(f"✓ Alcanzado el límite de {followed_count} follows. Deteniendo...")
        #             break
        #
        #         try:
        #             follow_buttons = self.driver.find_elements(
        #                 by=By.CSS_SELECTOR,
        #                 value="button._aswp._aswr._aswu._asw_._asx2"
        #             )
        #
        #             label_button = self.driver.find_elements(
        #                 by=By.CSS_SELECTOR,
        #                 value="div._ap3a._aaco._aacw._aad6._aade"
        #             )
        #
        #             for i in range(len(follow_buttons)):
        #                 if followed_count >= max_follows:
        #                     break
        #
        #                 try:
        #                     if label_button[i].text != "Following":
        #                         # Scroll suave al elemento
        #                         self.driver.execute_script(
        #                             "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
        #                             follow_buttons[i]
        #                         )
        #
        #                         # Espera aleatoria antes de hover
        #                         time.sleep(random.uniform(0.5, 1.5))
        #
        #                         # Simular hover (comportamiento humano)
        #                         actions = ActionChains(self.driver)
        #                         actions.move_to_element(follow_buttons[i]).perform()
        #                         time.sleep(random.uniform(0.3, 0.8))
        #
        #                         # Click
        #                         follow_buttons[i].click()
        #                         followed_count += 1
        #                         print(f"✓ Follow #{followed_count}")
        #
        #                         # Espera ALEATORIA entre follows (CRÍTICO)
        #                         wait_time = random.uniform(3, 7)
        #                         print(f"  Esperando {wait_time:.1f}s...")
        #                         time.sleep(wait_time)
        #
        #                 except Exception as e:
        #                     print(f"✗ Error en botón {i}: {e}")
        #                     continue
        #
        #             # Scroll aleatorio (más natural)
        #             container = self.driver.find_element(
        #                 by=By.XPATH,
        #                 value="/html/body/div[5]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]"
        #             )
        #
        #             # Scroll gradual en lugar de END directo
        #             scroll_amount = random.randint(300, 600)
        #             self.driver.execute_script(f"arguments[0].scrollBy(0, {scroll_amount});", container)
        #
        #             # Espera aleatoria entre scrolls
        #             time.sleep(random.uniform(2, 4))
        #
        #         except Exception as e:
        #             print(f"Error en iteración {n}: {e}")
        #             time.sleep(random.uniform(2, 4))
        #             continue
        #
        #     print(f"\n✓ Proceso completado. Total de follows: {followed_count}")

