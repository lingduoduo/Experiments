from pandas_s3 import s3read

# read-in csv data using pandas
# df_view = pd.read_csv('s3://amp-lhuang-test/elme-sampled-data2.csv')
# print(df_view.info())


# read-in parquet data
# path = 'amp-elme-sandbox/elme-sampled-data1/*.parquet'
# df_parquet = s3read(path, 'parquet')
# print(df_parquet.info())

# read-in csv data
path = 'amp-lhuang-test/elme-sampled-data2.csv'
df_csv = s3read(path, 'csv')
print(df_csv.info())

