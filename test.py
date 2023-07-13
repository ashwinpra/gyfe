from tabulate import tabulate
import pandas as pd

df = pd.read_csv('available_electives.csv')

print(tabulate(df, headers='keys', tablefmt='psql'))
print(tabulate(df, headers='keys', tablefmt='fancy_grid'))
