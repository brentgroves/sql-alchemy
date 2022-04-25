# https://towardsdatascience.com/heres-how-to-run-sql-in-jupyter-notebooks-f26eb90f3259
# https://www.sqlshack.com/learn-jupyter-notebooks-for-sql-server/
import sqlalchemy

# mssql+pyodbc://<username>:<password>@<dsnname>
username = 'mgadmin' 
password = 'WeDontSharePasswords1!' 

engine = sqlalchemy.create_engine("mssql+pyodbc://"+username+":"+password+"@dw")

%load_ext sql 
%sql mssql+pyodbc://mgadmin:WeDontSharePasswords1!@dw

%%sql
select *
from Plex.accounting_period ap 
where period_key = 45758

pd = %sql select period_display from Plex.accounting_period ap where period_key = 45758 
print(pd)

pd = %sql select period_display from Plex.accounting_period ap  
print(pd[0][0])

%%sql
with cte as 
(
select *, row_number() over(order by period_key) as rownum 
from Plex.accounting_period
)
result = select * from cte
where rownum < 5

%%sql
insert into Scratch.accounting_period
exec Report.accounting_period 202201,202203

result = %sql select * from Scratch.accounting_period

import pandas as pd
df = result.DataFrame()


%%sql 
insert into Scratch.trial_balance
exec Report.trial_balance 202203,202203

import matplotlib.pyplot as plt 

plt.figure(figsize=(4,5)) 
chart = %sql select category_type, sum(balance) balance, sum(ytd_balance) from Scratch.trial_balance group by category_type 

chart.bar()