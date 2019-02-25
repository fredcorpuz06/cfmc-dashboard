import pandas as pd
import numpy as np
impact_money = pd.read_csv("./data/impact_total_money.csv")
fund_yearly_money = pd.read_csv("./data/fund_yearly_money.csv")

my_years =fund_yearly_money['year'].unique().astype(int).min()
fund_types = fund_yearly_money['Fdescript'].unique()
money_metrics = ['total_DAmt', 'count', 'avg_DAmt']
