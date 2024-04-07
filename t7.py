from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()))

url = 'https://google.com'

driver.get(url)

driver.execute_script("window.open('about:blank', 'tab2');")
driver.switch_to.window("tab2")
driver.get('chrome://network')

driver.implicitly_wait(5)

network_requests = driver.find_elements(By.XPATH, "//div[contains(@class, 'request')]/div[contains(@class, 'name')]/span")

for request in network_requests:
    print(request.text)

driver.quit()
