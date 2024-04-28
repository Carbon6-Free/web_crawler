import json
import matplotlib.pyplot as plt

def bytes_to_kb(bytes):
    return bytes / 1024

with open("request.json", "r") as file:
    data = json.load(file)

all_sizes_kb = {}
all_statuses = {}
for entry in data[0]:
    url = entry['URL']
    contents = entry['Contents']
    
    # 각 타입(type)별로 사이즈(size)와 상태(status) 저장
    sizes = {}
    statuses = {}
    for content in contents:
        content_type = content['Type']
        size = content['Size']
        status = content['Status']
        
        # Byte에서 KB로 변환하여 저장
        size_kb = bytes_to_kb(size)
        
        if content_type not in sizes:
            sizes[content_type] = []
        sizes[content_type].append(size_kb)
        
        if content_type not in statuses:
            statuses[content_type] = []
        statuses[content_type].append(status)
    
    # 전체 데이터에 추가
    for key, value in sizes.items():
        if key not in all_sizes_kb:
            all_sizes_kb[key] = []
        all_sizes_kb[key].extend(value)
    
    for key, value in statuses.items():
        if key not in all_statuses:
            all_statuses[key] = []
        all_statuses[key].extend(value)

# 시각화
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.bar(all_sizes_kb.keys(), [sum(values) for values in all_sizes_kb.values()], color='skyblue')
plt.title('Total Sizes of Contents')
plt.xlabel('Content Type')
plt.ylabel('Total Size (KB)')

plt.xticks(rotation=90)

plt.subplot(1, 2, 2)
plt.bar(all_statuses.keys(), [len(values) for values in all_statuses.values()], color='salmon')
plt.title('Total Statuses of Contents')
plt.xlabel('Content Type')
plt.ylabel('Count')

plt.xticks(rotation=90)

plt.tight_layout()
plt.show()