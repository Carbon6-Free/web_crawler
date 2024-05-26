from firebase import firebase
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from crawler_module import *
from network_carborn import *
import random
import re

file = open("URL.txt", "r")
urls = file.readlines()

urls = [line[:-2] for line in urls]
print(urls)

firebase=firebase.FirebaseApplication("https://(your url).firebaseio.com/",None)
    
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
cando = ["fetch", "css", "img", "script","link","video"]

def getjsonData(url):
    jsonData = []
    totSize = 0
    datasizeoftype = {"fetch":0, "css":0, "img":0, "script":0, "link":0, "video":0}
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        network_requests = driver.execute_script("return window.performance.getEntriesByType('resource');")

        for entry in network_requests:
            size = get_data_size(entry["name"])
            if (entry["initiatorType"] in cando):
                print(entry["name"], entry["responseStatus"], entry["initiatorType"], size, entry["duration"], sep="\n")
                totSize += size
                datasizeoftype[entry["initiatorType"]] += size
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

        return content, datasizeoftype
    except:
        pass

for url in urls:
    log, datasize = getjsonData(url)
    datasize["g of CO2"] = annual_carborn(log[-1]["Size"])
    # Storing and retrieving data in Firebase
    match = re.search(r'(?<=://)(.*?)(?=/|$)', url)  # 도메인 이름 추출을 위한 정규표현식
    if match:
        domain = match.group(1)  # 도메인 이름 추출
        modified_domain = domain.replace(".", "-")  # '.'을 '-'로 변경
        print(modified_domain)

    firebase.post(f'{modified_domain}/', datasize)
    # result = firebase.get(f'/{modified_domain}', '')
