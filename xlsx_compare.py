import pandas as pd
import numpy as np

df1=pd.read_excel('1.xlsx')
df2=pd.read_excel('2.xlsx')

df1.equals(df2)
comparison_values = df1.values == df2.values
rows,cols=np.where(comparison_values==False)
for item in zip(rows,cols):
    df1.iloc[item[0], item[1]] = '{} --> {}'.format(df1.iloc[item[0], item[1]],df2.iloc[item[0], item[1]])

def color_diff_red(val):
    bgcolor = 'red' if ">" in str(val) else 'none'
    return f'background-color: {bgcolor}'
final=df1.style.applymap(color_diff_red)

final.to_excel('./Excel_diff.xlsx',index=False,header=True)

