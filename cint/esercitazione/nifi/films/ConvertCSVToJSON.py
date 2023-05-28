import sys

import pandas as pd
import json

# Read CSV input file
df = pd.read_csv(sys.argv[1])
df = df.dropna()

# Convert dataframe to a list of dict records
data = df.to_dict('records')

# Convert each record in a JSON record and write it to stdout.
for d in data:
    print(json.dumps(d))
