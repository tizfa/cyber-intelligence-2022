import pandas as pd
import sys
import json

df = pd.read_csv(sys.argv[1])
df["Location"] = df.apply(lambda r: str(r["Latitude"])+","+str(r["Longitude"]), axis=1)
df["Timestamp"] = df['Date'] + ' ' + df['Time']
df = df.fillna(value=df.mean())
jsonRowList = df.to_dict(orient='records')
for r in jsonRowList:
    jsonRow = json.dumps(r)
    print(jsonRow)







