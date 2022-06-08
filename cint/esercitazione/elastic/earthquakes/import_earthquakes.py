import pandas as pd
import sys 

df = pd.read_csv(sys.argv[1])
df["Location"] = df.apply(lambda r: str(r["Latitude"])+","+str(r["Longitude"]), axis=1)
for index, r in df.iterrows():
    jsonRow = r.to_json()
    print(jsonRow)






