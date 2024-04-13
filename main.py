from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
import requests
import json

file = open("URL.txt", "r")
urls = file.readlines()
print(urls)

# url = 'https://naver.com'

def get_data_size(url):
    try:
        response = requests.head(url)
        if 'content-length' in response.headers:
            content_length = int(response.headers['content-length'])
            return content_length
        else:
            print("Content length header not found.")
            return 0
    except Exception as e:
        print("Error:", e)
        return None

chromedriver_path = './chromedriver'

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-web-security')  # CORS 정책 우회 설정
options.add_argument('--headless')

# CORS 정책 우회 설정
capabilities = DesiredCapabilities.CHROME.copy()
capabilities['goog:loggingPrefs'] = {'browser': 'ALL'}

driver = webdriver.Chrome(service= Service(chromedriver_path), options=options)
content = []
data = []

def getjsonData(url):
    jsonData = []
    totSize = 0
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        network_requests = driver.execute_script("return window.performance.getEntriesByType('resource');")

        for entry in network_requests:
            size = get_data_size(entry["name"])
            totSize += size
            jsonData.append({
                "Name": entry["name"],
                "Status": entry["responseStatus"],
                "Type": entry["initiatorType"],
                "Size": size,
                "Time": entry["duration"]
            })
        content.append({
            "URL":url,
            "Contents":jsonData,
            "Size": totSize
        })

        return content
    except:
        pass

for url in urls:
    data.append(getjsonData(url))

with open('network_requests.json', 'w') as json_file:
    json.dump(data, json_file, indent=5)

driver.quit()
