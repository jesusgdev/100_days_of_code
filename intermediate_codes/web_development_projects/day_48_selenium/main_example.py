from selenium.webdriver.common.by import By
from selenium import webdriver


# Keep Chrome browser open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option(name="detach", value=True)

driver = webdriver.Chrome(options=chrome_options)
# driver.get("https://www.amazon.com/Apple-2024-Desktop-Computer-"
#            "10%E2%80%91core/dp/B0DLBTPDCS/?_encoding=UTF8&pd_rd_"
#            "w=GyMUI&content-id=amzn1.sym.4efc43db-939e-4a80-abaf-"
#            "50c6a6b8c631%3Aamzn1.symc.5a16118f-86f0-44cd-8e3e-"
#            "6c5f82df43d0&pf_rd_p=4efc43db-939e-4a80-abaf-"
#            "50c6a6b8c631&pf_rd_r=K8HBMQ6GGZN81FPHN02Z&pd_"
#            "rd_wg=crKIN&pd_rd_r=bb434489-c45c-4d89-b9b9-"
#            "b0582fd5059e&ref_=pd_hp_d_atf_ci_mcx_mr_ca_"
#            "hp_atf_d&th=1")

# price_dollar = driver.find_element(by=By.CLASS_NAME, value="a-price-whole")
# price_cents = driver.find_element(by=By.CLASS_NAME, value="a-price-fraction")
#
# print(f"{price_dollar.text}.{price_cents.text}")

# URL = "https://en.wikipedia.org/wiki/Main_Page"
#
# driver.get(url=URL)
#
# number_articles = driver.find_element(by=By.XPATH, value='//*[@id="articlecount"]/ul/li[2]/a[1]')
# print(number_articles.text)

# number_articles2 = driver.find_elements(by=By.CSS_SELECTOR, value='a[href="/wiki/Special:Statistics"]')[1]
# print(number_articles2.text)
#
# number_articles3 = driver.find_elements(by=By.CSS_SELECTOR, value='a[title="Special:Statistics"]')[1]

driver.get("https://www.python.org/")

search_bar = driver.find_element(by=By.NAME, value="q")
print(search_bar.get_attribute("placeholder"))
button = driver.find_element(by=By.ID, value="submit")
print(button.size)
documentation_link = driver.find_element(
    by=By.CSS_SELECTOR,
    value=".documentation-widget a"
)
print(documentation_link.text)

bug_link  = driver.find_element(by=By.XPATH, value='//*[@id="site-map"]/div[2]/div/ul/li[3]/a')
print(bug_link.text)


driver.quit()