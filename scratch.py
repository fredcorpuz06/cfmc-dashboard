import pandas as pd
import numpy as np

""" 
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

df[' index'] = range(1, len(df) + 1)
# print(df)

page_settings={'current_page': 0, 'page_size': 5}

startP = page_settings['current_page'] * page_settings['page_size']
endP = (page_settings['current_page'] + 1) * page_settings['page_size']

print(startP, endP)
print(df.iloc[startP:endP])
print(df.iloc[startP:endP].to_dict('rows'))

 """
grants = pd.read_csv("./data/grants_clean.csv")
funds = pd.read_csv("./data/funds_clean.csv")

summary_types = ['gross_total', 'count', 'ave_amt']
var_choices = ['fund_type', 'project_impact', 'org_impact', 'region']


yearRange=[2008, 2015]
summaryType=summary_types[0]
varChoice1=var_choices[1]
varChoice2=var_choices[3]



df = funds
dff = df[(df.year >= yearRange[0]) & (df.year <= yearRange[1])]
dff = dff[['fund_type', varChoice1, varChoice2, 'fund_damt']]

g = dff.groupby(['fund_type', varChoice1, varChoice2])
rez = g.agg([np.sum, lambda x: np.shape(x)[0], np.mean]).rename(columns={
    'sum': summary_types[0],
    '<lambda>': summary_types[1],
    'mean': summary_types[2]
})['fund_damt'].reset_index()

# print(rez)
rez01 = rez[['fund_type', varChoice1] + summary_types].rename(columns={
    'fund_type': 'source',
    varChoice1: 'target'
}
)
rez12 = rez[[varChoice1, varChoice2] + summary_types].rename(columns={
    varChoice1: 'source',
    varChoice2: 'target'
})

rez_all = rez01.append(rez12, ignore_index=True)
# rez_all = rez01

# print(rez_all)
source_nodes = rez_all.source.tolist()
target_nodes = rez_all.target.tolist()
all_nodes = set(source_nodes + target_nodes)

myMap = {}
for i, n in enumerate(sorted(all_nodes)):
    myMap[n] = i

# print(sorted(myMap.keys()))
rez_all = rez_all.replace(myMap)
# print(rez_all)
print(rez_all.source.shape[0])
print(len(myMap))

flows = {
    'source': rez_all.source.tolist(),
    'target': rez_all.target.tolist(),
    'value': rez_all[summaryType].tolist(),
    'label': list(sorted(myMap.keys())) + ['fred' for _ in range(0, rez_all.shape[0] - len(myMap))],

}
for k, f in flows.items():
    print(k, len(f))
pd.DataFrame(flows).to_csv('./data/scratch3.csv', index=False)


'''
dff = grants[(grants.year >= yearRange[0]) & (grants.year <= yearRange[1])]
# dff = dff[[varChoice1, varChoice2, 'grant_damt']]
dff = dff[['year', varChoice1, varChoice2, 'grant_damt']]

g = dff.groupby([varChoice1, 'year'])
# g = dff.groupby([varChoice1, varChoice2])
rez = g.agg([np.sum, lambda x: np.shape(x)[0], np.mean]).rename(columns={
            'sum': summary_types[0],
            'mean': summary_types[2],
            '<lambda>': summary_types[1],
        })['grant_damt']

# print(rez['grant_damt'].gross_total)

print(rez)
# bars =[{
#     'name': varChoice1,
#     'label': rez.index.tolist(),
#     'value': rez[summaryType].tolist()
# }]
# print(bars)
# .unstack(fill_na=0).stack()

bars = []
for name, group in rez.groupby(level=0):
    bar = {
        'name': name,
        'label': [i[1] for i in group.index],
        'value': group[summaryType].tolist(),
    }
    bars.append(bar)
print(bars)

# bars = [
#     {
#         'label': rez.index.tolist(),
#         'value': rez[summaryType].tolist()
#     },
#     {
#         'label': ['a','b','c'],
#         'value': [4,5,6]
#     },

# ]
# print(bars)

# dff = grants[(grants.year >= yearRange[0]) & (grants.year <= yearRange[1])]
# dff = dff[[varChoice1, varChoice2, 'grant_damt']]
'''

