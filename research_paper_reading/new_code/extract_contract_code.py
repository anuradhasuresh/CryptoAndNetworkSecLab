import pandas as pd

df = pd.read_parquet('contracts0.parquet', engine='fastparquet')

print(df['bytecode'])
unique_contracts = df['bytecode'].unique()
i = 1
for contract in unique_contracts:
    with open(f'contracts/test{i}.contract.code', 'w') as f:
        f.write(contract[2:])
    i+=1
    if i == 1000:
        break