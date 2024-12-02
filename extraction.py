import pandas as pd
import numpy as np

df = pd.read_csv(r'/Users/gustavomeira/Downloads/ibirapuera,-são paulo, brazil-air-quality.csv',
                 delimiter=', ')

df['date'] = pd.to_datetime(df['date'], format="%Y/%m/%d")
df = df.fillna(np.nan)
del df['so2']
del df['pm10']

df.to_pickle(r'/Users/gustavomeira/Documents/Python/TCC/Data_SP.pkl')