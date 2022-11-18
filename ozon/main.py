import pandas as pd
import os
import json

df = pd.read_csv('os.txt')
with open('result.txt', 'w') as f:
    f.write(df.value_counts().to_string())