import pandas as pd
import pyarrow.parquet as pq

df=pd.DataFrame({
    "id":[1,2,3],
    "name":["Shijin","vijay","Nisha"],
    "Age":[22,23,24],
    "Salary":[200000, 300000, 100000]
})

df.to_parquet('data.parquet',engine='pyarrow',compression='brotli')

df2=pd.read_parquet('data.parquet',engine='pyarrow')

table=pq.read_table('data.parquet')

df_subset=pd.read_parquet('data.parquet',columns=['name','Age'])



print("dataframe schema",table.schema)
print("datafram",df2.head())
print("df_subset",df_subset.head())