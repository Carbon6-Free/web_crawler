from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
import json

chromedriver_path = './chromedriver'

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-web-security')  # CORS 정책 우회 설정
options.add_argument('--headless')

# CORS 정책 우회 설정
capabilities = DesiredCapabilities.CHROME.copy()
capabilities['goog:loggingPrefs'] = {'browser': 'ALL'}

driver = webdriver.Chrome(service= Service(chromedriver_path), options=options)
url = 'https://naver.com'

driver.get(url)
wait = WebDriverWait(driver, 20)


network_requests = driver.execute_script("return window.performance.getEntriesByType('resource');")

# try:
#     for request in network_requests:
#         print(request)
# except:
#     print(network_requests)

jsonData = []
for entry in network_requests:
    jsonData.append({
        "Name": entry["name"],
        "Status": entry["responseStatus"],
        "Type": entry["initiatorType"],
        "Size": entry["transferSize"],
        "Time": entry["duration"]
    })

# print(json.dumps(jsonData))

# with open('network2.json', 'w') as json_file:
#     json.dump(network_requests, json_file)

with open('network_requests.json', 'w') as json_file2:
    json.dump(jsonData, json_file2, indent=4)


driver.quit()
