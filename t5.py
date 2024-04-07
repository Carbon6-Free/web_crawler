import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()))\

driver.get('https://google.com')

webdriver.ActionChains(driver).send_keys(Keys.F12).perform()

driver.implicitly_wait(3)

tab_elements = driver.find_elements_by_class_name("toolbar-tab")
for tab_element in tab_elements:
    if tab_element.get_attribute("aria-label") == "Network panel":
        tab_element.click()
        break

network_elements = driver.find_elements_by_class_name("network-url")
network_data = []

for network_element in network_elements:
    name = network_element.text
    parent_element = network_element.find_element_by_xpath('..')
    type_element = parent_element.find_element_by_class_name("network-type")
    size_element = parent_element.find_element_by_class_name("network-size")
    network_data.append({
        'Name': name,
        'Type': type_element.text,
        'Size': size_element.text
    })

df = pd.DataFrame(network_data)

driver.quit()

print(df)