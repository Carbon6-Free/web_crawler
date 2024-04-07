import requests
import time
import matplotlib.pyplot as plt

def send_request(url):
    start_time = time.time()
    response = requests.get(url)
    end_time = time.time()

    print(f"URL: {url}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Time: {end_time - start_time:.2f} seconds")
    print("Headers:")
    for header, value in response.headers.items():
        print(f"  {header}: {value}")

    return end_time - start_time

def plot_response_times(urls):
    response_times = []
    for url in urls:
        response_time = send_request(url)
        response_times.append(response_time)

    plt.figure(figsize=(8, 6))
    plt.bar(range(len(urls)), response_times, tick_label=urls)
    plt.xlabel("URLs")
    plt.ylabel("Response Time (seconds)")
    plt.title("Response Times for URLs")
    plt.show()

if __name__ == "__main__":
    target_urls = ["https://bing.com", "https://github.com", "https://google.com", "https://naver.com"]
    plot_response_times(target_urls)