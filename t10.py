from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def crawl_network_info(url):
    driver = webdriver.Safari()

    driver.get(url)
    time.sleep(5)
    driver.get("about:blank")
    driver.get("about:preferences#advanced")
    driver.find_element(By.XPATH, "//button[@id='advanced-tab']").click()
    driver.find_element(By.XPATH, "//input[@id='advanced-toggle-dev-tools']").click()

    driver.get("about:blank")
    driver.get("about:devtools")
    devtools = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "devtools-app")))
    devtools.send_keys(Keys.TAB)
    devtools.send_keys(Keys.TAB)
    devtools.send_keys(Keys.TAB)
    devtools.send_keys(Keys.TAB)
    devtools.send_keys(Keys.ENTER)

    network_requests = driver.execute_script("return NetworkLogView.networkLogView._dataGrid._rootNode._children.map(node => node._record)")

    for request in network_requests:
        request_url = request['url']
        request_type = request['resourceType']
        request_status = request['statusCode']
        request_size = request['transferSize']
        print("URL:", request_url)
        print("Type:", request_type)
        print("Status:", request_status)
        print("Size:", request_size)

    driver.quit()

if __name__ == "__main__":
    url = 'https://example.com'
    crawl_network_info(url)
