import pandas as pd
import sys
import json
import numpy as np

df = pd.read_csv(sys.argv[1])
df["Location"] = df.apply(lambda r: str(r["Latitude"])+","+str(r["Longitude"]), axis=1)
df["Timestamp"] = df['Date'] + ' ' + df['Time']
print(df.columns)
c = df.select_dtypes(np.number).columns
df[c] = df[c].fillna(value=df[c].mean())
df = df.fillna("unspecified")
jsonRowList = df.to_dict(orient='records')
for r in jsonRowList:
    jsonRow = json.dumps(r)
    print(jsonRow)







