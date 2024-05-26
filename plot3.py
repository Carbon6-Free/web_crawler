import json
import pandas as pd

# JSON 파일 로드
with open('carbonfree-export.json') as f:
    data = json.load(f)

# 중복 제거를 위한 세트와 데이터 저장용 리스트 초기화
seen_links = set()
filtered_records = []

# 데이터 변환 및 중복 제거
for site, details in data.items():
    # 각 사이트의 최소 CO2 배출량을 저장하기 위한 딕셔너리 초기화
    min_co2_by_site = {}

    # 각 사이트의 하위 데이터를 순회하면서 최소 CO2 배출량을 찾음
    for key, metrics in details.items():
        if site not in min_co2_by_site:
            min_co2_by_site[site] = metrics["g of CO2"]
        else:
            min_co2_by_site[site] = min(min_co2_by_site[site], metrics["g of CO2"])

    # 최소 CO2 배출량을 갖는 하위 데이터를 선택하여 저장
    for key, metrics in details.items():
        if metrics["g of CO2"] == min_co2_by_site[site]:
            record = {
                "site": site,
                "css": metrics["css"],
                "fetch": metrics["fetch"],
                "g_of_CO2": metrics["g of CO2"],
                "img": metrics["img"],
                "link": metrics["link"],
                "script": metrics["script"],
                "video": metrics["video"]
            }
            filtered_records.append(record)
            seen_links.add(site)

# 데이터프레임 생성
df = pd.DataFrame(filtered_records)

# g_of_CO2 값이 0이 아닌 데이터만 필터링
df = df[df['g_of_CO2'] > 0]
df = df[df['g_of_CO2'] < 100]

# 각 사이트별 CO2 배출량 요약
site_co2_summary = df.groupby('site')['g_of_CO2'].sum().sort_values(ascending=False)

# 각 자원별 CO2 배출량 기여도 계산
resource_columns = ['css', 'fetch', 'img', 'link', 'script', 'video']
resource_contribution = df[resource_columns].sum() / df[resource_columns].sum().sum()

import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정 (옵션)
plt.rcParams['font.family'] = 'AppleGothic'  # macOS
# plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows
plt.rcParams['axes.unicode_minus'] = False


import plotly.express as px
# 상위 10개 사이트만 선택
top_n = 10
top_sites = site_co2_summary.head(top_n).reset_index()

# 상위 10개 사이트의 총 CO2 배출량 막대 그래프
fig = px.bar(top_sites, x='g_of_CO2', y='site', orientation='h',
             title=f'상위 {top_n} 사이트별 총 CO2 배출량',
             labels={'g_of_CO2': '총 CO2 배출량 (g)', 'site': '사이트'})
fig.show()

# 각 자원의 CO2 배출 기여도 파이 차트
fig = px.pie(values=resource_contribution, names=resource_contribution.index,
             title='자원별 CO2 배출 기여도',
             labels={'value': 'CO2 배출량 비율', 'index': '자원'})
fig.show()

# 사이트별 자원 사용량의 산점도
fig = px.scatter(df, x='site', y='g_of_CO2', size='img', color='script',
                 hover_name='site', log_y=True, size_max=100,
                 title='사이트별 자원 사용량 및 CO2 배출량',
                 labels={'g_of_CO2': '총 CO2 배출량 (g)', 'img': '이미지 사용량', 'script': '스크립트 사용량'})
fig.show()

# 사이트별 자원 사용량 히트맵 데이터 준비
heatmap_data = df.melt(id_vars=['site'], value_vars=resource_columns, var_name='resource', value_name='usage')

# 사이트별 자원 사용량의 히트맵
fig = px.density_heatmap(heatmap_data, x='site', y='resource', z='usage', histfunc='avg',
                         title='사이트별 자원 사용량 히트맵',
                         labels={'usage': '사용량', 'site': '사이트', 'resource': '자원'})
fig.show()




# 사이트별 총 CO2 배출량 다시 계산
site_total_co2 = df.groupby('site')['g_of_CO2'].sum()

# CO2가 적게 발생하는 상위 10개 사이트 선택
top_10_lowest_co2_sites = site_total_co2.nsmallest(30)

# 선택된 사이트들에 해당하는 데이터 필터링
filtered_df = df[df['site'].isin(top_10_lowest_co2_sites.index)]

# 사이트별 자원 사용량의 히트맵
fig = px.density_heatmap(filtered_df.melt(id_vars=['site'], value_vars=resource_columns, var_name='resource', value_name='usage'), 
                         x='site', y='resource', z='usage', histfunc='avg',
                         title='탄소가 적게 발생하는 상위 10개 링크의 자원 사용량 히트맵',
                         labels={'usage': '사용량', 'site': '사이트', 'resource': '자원'})
fig.show()

# import numpy as np
# import plotly.graph_objects as go

# # CO2 배출량의 하위 구간 계산 (전체 데이터셋의 하위 5%, 10%, 20%, 30%, 50%)
# percentiles = [5, 10, 20, 30, 50]
# co2_percentile_values = np.percentile(filtered_df['g_of_CO2'], percentiles)

# # 각 CO2 배출량 구간에 속하는 사이트들 필터링
# co2_groups = []
# for i in range(len(co2_percentile_values) - 1):
#     lower_bound = co2_percentile_values[i]
#     upper_bound = co2_percentile_values[i + 1]
#     sites_in_range = filtered_df[(filtered_df['g_of_CO2'] >= lower_bound) & (filtered_df['g_of_CO2'] < upper_bound)]
#     co2_groups.append(sites_in_range)

# # 각 구간별 자원 사용량 계산
# resource_usage_in_groups = [group[resource_columns].sum() for group in co2_groups]

# # 그래프 생성
# fig = go.Figure()

# for i, resource in enumerate(resource_columns):
#     # 각 구간별 자원 사용량 막대 그래프 추가
#     resource_values = [usage[resource] for usage in resource_usage_in_groups]
#     fig.add_trace(go.Bar(x=percentiles, y=resource_values, name=resource))

# fig.update_layout(barmode='group', 
#                   title='CO2 배출량 하위 구간에 따른 자원 사용량',
#                   xaxis_title='CO2 배출량 하위 구간 (%)',
#                   yaxis_title='사용량',
#                   legend_title='자원')

# fig.show()


# import plotly.graph_objects as go
# import numpy as np

# # 탄소 발생량이 작은 순으로 데이터 정렬
# sorted_df = filtered_df.sort_values(by='g_of_CO2')

# # CO2 배출량의 하위 구간 계산 (전체 데이터셋의 하위 5%, 10%, 20%, 30%, 50%)
# percentiles = [5, 10, 20, 30, 50, 100, 101]
# co2_percentile_values = np.percentile(sorted_df['g_of_CO2'], percentiles)

# # 각 CO2 배출량 구간에 속하는 사이트들 필터링
# co2_groups = []
# for i in range(len(co2_percentile_values) - 1):
#     lower_bound = co2_percentile_values[i]
#     upper_bound = co2_percentile_values[i + 1]
#     sites_in_range = sorted_df[(sorted_df['g_of_CO2'] >= lower_bound) & (sorted_df['g_of_CO2'] < upper_bound)]
#     co2_groups.append(sites_in_range)

# # 각 구간별 자원 사용량 계산
# resource_usage_in_groups = [group[resource_columns].sum() for group in co2_groups]

# # 그래프 생성
# fig = go.Figure()

# for i, resource in enumerate(resource_columns):
#     # 각 구간별 자원 사용량 막대 그래프 추가
#     resource_values = [usage[resource] for usage in resource_usage_in_groups]
#     fig.add_trace(go.Bar(x=percentiles, y=resource_values, name=resource))

# fig.update_layout(barmode='group', 
#                   title='탄소 발생량이 작은 순서대로 자원 사용량',
#                   xaxis_title='CO2 배출량 하위 구간 (%)',
#                   yaxis_title='사용량',
#                   legend_title='자원')

# fig.show()
