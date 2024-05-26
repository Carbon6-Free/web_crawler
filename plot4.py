import pandas as pd
import numpy as np
import plotly.express as px
import json

with open('carbonfree-export.json') as f:
    data = json.load(f)

def preprocess_data(data):
    preprocessed_data = {}
    for website, details in data.items():
        min_co2 = float('inf')
        min_co2_details = None
        for detail_id, detail_data in details.items():
            if detail_data.get('g of CO2', float('inf')) < min_co2:
                min_co2 = detail_data['g of CO2']
                min_co2_details = detail_data
        if min_co2_details:
            preprocessed_data[website] = {min_co2_details['link']: min_co2_details}
    return preprocessed_data

data = preprocess_data(data)

df = pd.DataFrame([(website, detail_id, detail_data['css'], detail_data['fetch'], detail_data['g of CO2'], detail_data['img'], detail_data['link'], detail_data['script'], detail_data['video']) 
                   for website, details in data.items() 
                   for detail_id, detail_data in details.items()], 
                  columns=['Website', 'Detail ID', 'CSS', 'Fetch', 'CO2', 'Img', 'Link', 'Script', 'Video'])


filtered_df = df[df['CO2'] != 0]


# 백분율 값을 0에서 100 사이의 값으로 변환
percentiles = [0, 5, 10, 20, 30, 50, 100]
percentile_values = [p / 100 for p in percentiles]

# CO2를 기준으로 데이터프레임 정렬
sorted_df = filtered_df.sort_values(by='CO2')

# 데이터셋을 나눌 백분위수 계산
percentile_values = sorted_df['CO2'].quantile(percentile_values).tolist()

# 각 구간에 속하는 데이터를 분할
datasets = []
for i in range(len(percentile_values) - 1):
    lower_bound = percentile_values[i]
    upper_bound = percentile_values[i + 1]
    subset = sorted_df[(sorted_df['CO2'] >= lower_bound) & (sorted_df['CO2'] < upper_bound)]
    datasets.append((f"하위 {percentiles[i]}~{percentiles[i+1]}% 구간의 데이터 (CO2: {lower_bound} ~ {upper_bound}):", subset))

# 결과 출력
for label, dataset in datasets:
    # print(label)
    # print(dataset)
    resource_contribution = dataset[['CSS', 'Fetch', 'Img', 'Link', 'Script', 'Video']].apply(lambda x: x * filtered_df['CO2'])
    resource_contribution.columns = ['CSS', 'Fetch', 'Img', 'Link', 'Script', 'Video']
    resource_contribution['Website'] = dataset['Website']
    color_map = {'CSS': 'blue', 'Fetch': 'orange', 'Img': 'green', 'Link': 'red', 'Script': 'purple', 'Video': 'yellow'}

    resource_contribution_sum = resource_contribution.drop('Website', axis=1).sum()
    fig = px.pie(names=resource_contribution_sum.index, values=resource_contribution_sum.values, title=label, color_discrete_map=color_map)
    fig.show()