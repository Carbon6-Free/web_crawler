import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
import requests
from network_carborn import *
import json

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
cando = ["fetch", "css", "img", "script","link","video"]

def getjsonData(url):
    jsonData = []
    totSize = 0
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        network_requests = driver.execute_script("return window.performance.getEntriesByType('resource');")

        for entry in network_requests:
            size = get_data_size(entry["name"])
            if (entry["initiatorType"] in cando):
                # print(entry["name"], entry["responseStatus"], entry["initiatorType"], size, entry["duration"], sep="\n")
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


st.title("CarbonFree")

# 검색어 입력을 받는 텍스트 상자
search_query = st.text_input(label="url", value='url을 입력하세요')

# 엔터(입력 버튼)를 누르면 결과 표시
if st.button("결과보기"):
    log = getjsonData(search_query)
    st.write(annual_carborn(log[-1]["Size"]), "g of CO2")
    st.write(log)