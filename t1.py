import requests

def crawl_network_data(url):
    try:
        response = requests.get(url)
        
        request_info = {
            'Name': response.request.url,
            'Status': response.status_code,
            'Size': len(response.content)
        }
        
        for key, value in request_info.items():
            print(f"{key}: {value}")

    except Exception as e:
        print("네트워크 데이터를 크롤링하는 동안 오류가 발생했습니다:", e)

url = 'https://naver.com'

crawl_network_data(url)
