from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()))

driver.get('https://google.com')

driver.execute_script("window.open('about:blank', '_blank');")
driver.switch_to.window(driver.window_handles[1])
driver.get('chrome://devtools/content/performance.html')
time.sleep(2)

tab_elements = driver.find_elements_by_class_name("toolbar-tab")
for tab_element in tab_elements:
    if tab_element.get_attribute("aria-label") == "Network panel":
        tab_element.click()
        break

network_elements = driver.find_elements_by_class_name("network-url")
for network_element in network_elements:
    print(network_element.text)

driver.quit()
