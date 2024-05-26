import json
import matplotlib.pyplot as plt
import numpy as np

# JSON 파일 읽기
with open('carbonfree-export.json', 'r') as f:
    data = json.load(f)

# 데이터 정리
categories = ['css', 'fetch', 'g of CO2', 'img', 'link', 'script', 'video']
site_data = {}

for site, site_values in data.items():
    for _, metrics in site_values.items():
        if site not in site_data:
            site_data[site] = {category: [] for category in categories}
        for category in categories:
            site_data[site][category].append(metrics.get(category, 0))

# 각 사이트별로 평균 값을 계산
average_site_data = {}
for site, metrics in site_data.items():
    average_site_data[site] = {category: np.mean(values) for category, values in metrics.items()}

# 시각화
fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(len(categories))
width = 0.2

for i, (site, metrics) in enumerate(average_site_data.items()):
    values = [metrics[category] for category in categories]
    ax.bar(x + width * i, values, width=width, label=site)

ax.set_xlabel('Metrics')
ax.set_ylabel('Average Values')
ax.set_title('Average Metrics Across Different Sites')
ax.set_xticks(x + width * (len(average_site_data) - 1) / 2)
ax.set_xticklabels(categories)
plt.xticks(rotation=45)
plt.legend(loc='best')
plt.show()
