import pandas as pd

df = pd.read_csv('valutazioni.csv')
# apply mean and std to each column
for col in df.columns:
    mean = df[col].mean()
    std = df[col].std()
    print(f"{col} mean of {mean:.2f} with std of {std:.2f}")