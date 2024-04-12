from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# options = webdriver.ChromeOptions()
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--incognito')
# options.add_argument('--headless')

driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()), 
                        #   options=options
)

url = 'https://google.com'


driver.get(url)
time.sleep(5)

network_requests = driver.execute_script("return window.performance.getEntries();")

for request in network_requests:
    print(request)

driver.quit()
