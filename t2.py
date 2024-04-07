import requests

def crawl_network_data(url):
    try:
        response = requests.get(url)
        network_data = response.text
        
        print(network_data)
        
    except Exception as e:
        print("네트워크 데이터를 크롤링하는 동안 오류가 발생했습니다:", e)

url = 'https://google.com'

crawl_network_data(url)
