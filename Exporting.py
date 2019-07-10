import pandas as pd
from pandas import ExcelFile, ExcelWriter

df = pd.read_excel("C:\\Users\\Josh\\Downloads\\Invoice for Brinkmans.xlsx", sheet_name='Sheet1')

print(df)
