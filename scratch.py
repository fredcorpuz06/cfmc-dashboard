import pandas as pd
import numpy as np
import sqlite3
from sqlalchemy import create_engine
import os 
import psycopg2


from app_utils import graphers

# print(dir(graphers))
x = graphers.PlotlyGrapher()
# x.hi()
print(x.pie_chart())


# DATABASE_URL = os.environ['DATABASE_URL']
# DATABASE_URL = "postgresql-dimensional-36261"


# cmd = "heroku config:get DATABASE_URL"
# DATABASE_URL = os.popen(cmd).read()
# print(DATABASE_URL)
# DATABASE_URL = "host=ec2-50-17-231-192.compute-1.amazonaws.com dbname=dbpcnq9cirtphf user=rnkbpafrerjisd  password=57c384efff4206b3556c7b33fd99a3e936a856658b3ebc5870a204e2a8dea9a9 sslmode=require"
# conn = psycopg2.connect(
#     host="ec2-50-17-231-192.compute-1.amazonaws.com",
#     dbname="dbpcnq9cirtphf",
#     user="rnkbpafrerjisd",
#     password="57c384efff4206b3556c7b33fd99a3e936a856658b3ebc5870a204e2a8dea9a9",
#     port=5432,
#     # sslmode="require"
# )
# conn = psycopg2.connect(DATABASE_URL)
# cur = conn.cursor()
# cur.execute('CREATE TABLE test (id PRIMARY KEY, num INTEGER, data VARCHAR);')
# cur.execute('INSERT INTO test (num, data) VALUES (100, "abc");')
# cur.execute('SELECT * FROM test;')
# rez = cur.fetchall()
# print(rez)

# conn.commit()
# conn.close()



# conn = sqlite3.connect("./fred.db")
# conn = sqlite3.connect(":memory:")
# engine = create_engine('sqlite:///fred.db', echo=False)
# c = conn.cursor()
# c.execute("SELECT * FROM funds")
# funds1 = c.fetchall()
# print(funds1[:5])
# funds1 = pd.read_sql_query("SELECT * FROM funds", conn)
# print(funds1.head())

# funds = pd.read_csv("./data/funds_clean.csv")
# funds.to_sql('funds', con=engine)



# c.execute("""CREATE TABLE employees (
#             first TEXT,
#             last TEXT,
#             pay INTEGER
#             )""")

# def insert_emp(emp):
#     with conn:
#         c.execute(
#             "INSERT INTO employees VALUES (:first, :last, :pay)",
#             {'first': emp.first, 'last': emp.last, 'pay': emp.pay}
#         )

# def get_emps_by_name(lastname):
#     c.execute(
#         "SELECT * FROM employees WHERE last=:last",
#         {'last': lastname}
#     )
#     return c.fetchall()

# def update_pay(emp, pay):
#     with conn:
#         c.execute(
#             """UPDATE employees SET pay=:pay
#               WHERE first = :first AND last = :last""",
#             {'first': emp.first, 'last': emp.last, 'pay': emp.pay}
#         )

# def remove_emp(emp):
#     with conn:
#         c.execute(
#             "DELETE FROM employees WHERE first = :first AND last = :last",
#             {'first': emp.first, 'last': emp.last}
#         )


# class Employee:
#     def __init__(self, first, last, pay):
#         self.first = first
#         self.last = last
#         self.pay = pay
    
#     @property
#     def email(self):
#         return '{}.{}@email.com'.format(self.first, self.last)

#     @property
#     def fullname(self):
#         return '{} {}'.format(self.first, self.last)

#     def __repr__(self):
#         return "Employee('{}', '{}', {})".format(self.first, self.last, self.pay)

# emp_1 = Employee('John', 'Doe', 80000)
# emp_2 = Employee('Jane', 'Doe', 90000)

# c.execute("SELECT * FROM fredsTable")
# print(c.fetchall())

# insert_emp(emp_1)
# insert_emp(emp_2)

# emps = get_emps_by_name('Doe')
# print(emps)

# update_pay(emp_2, 95000)
# remove_emp(emp_1)

# emps = get_emps_by_name('Doe')
# print(emps)


# conn.close()
 


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

"""