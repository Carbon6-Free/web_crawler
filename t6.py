from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()))

url = 'https://www.google.com'

driver.get(url)

wait = WebDriverWait(driver, 20)

try:
    wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Network')]"))).click()
except:
    print("Network tab not found.")

network_requests = driver.find_elements(By.XPATH, "//div[contains(@class, 'network-item-row')]")

data = []

for request in network_requests:
    name = request.find_element(By.XPATH, ".//div[contains(@class, 'name-column')]").text
    type_ = request.find_element(By.XPATH, ".//div[contains(@class, 'type-column')]").text
    size = request.find_element(By.XPATH, ".//div[contains(@class, 'size-column')]").text
    data.append({'Name': name, 'Type': type_, 'Size': size})

driver.quit()

df = pd.DataFrame(data)

print(df)