import pandas as pd
import numpy as np

grants = pd.read_csv("./data/grants_clean.csv")
funds = pd.read_csv("./data/funds_clean.csv")

summary_type = ['gross_total', 'count', 'ave_amt']
var_choices = ['fund_type', 'project_impact', 'org_impact', 'region']


yearRange=[2008, 2015]
summaryType=summary_type[0]
varChoice1=var_choices[1]
varChoice2=var_choices[2]


dff = grants[(grants.year >= yearRange[0]) & (grants.year <= yearRange[1])]
# dff = dff[[varChoice1, varChoice2, 'grant_damt']]
dff = dff[['year', varChoice1, varChoice2, 'grant_damt']]

g = dff.groupby([varChoice1, 'year'])
# g = dff.groupby([varChoice1, varChoice2])
rez = g.agg([np.sum, lambda x: np.shape(x)[0], np.mean]).rename(columns={
            'sum': summary_type[0],
            'mean': summary_type[2],
            '<lambda>': summary_type[1],
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