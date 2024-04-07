import requests
from bs4 import BeautifulSoup

def get_network_data(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        network_data = soup.find('div', class_='network-data')
        
        if network_data:
            print(network_data.text)
        
        else:
            print("네트워크 데이터를 찾을 수 없습니다.")
    else:
        print("요청이 실패했습니다. 상태 코드:", response.status_code)

url = 'https://naver.com'

get_network_data(url)
