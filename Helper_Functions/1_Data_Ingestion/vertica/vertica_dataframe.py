# vertica-db-client needs to use python3.8

import pandas as pd
import vertica_python

# [TLSMode: require]
conn_info = {'host': '***',
             'port': 5433,
             'user': '***',
             'password': '***',
             'database': 'amp'}
connection = vertica_python.connect(**conn_info)

with vertica_python.connect(**conn_info) as conn:
    # Open a cursor to perform database operations
    # vertica-python only support one cursor per connection
    cur = conn.cursor()

    query = "select cc.* from amp_reporting.CLICK_CONVERSION_FACT_BY_DAY cc where cc.PUBLISHER_ID in (select distinct PUBLISHER_ID from publisher_taxonomy.PUBLISHER_MEDIA_TAXONOMY where MEDIA_PRODUCT_ID = 10) and cc.COUNTRY_ID = 2 and cc.ACCOUNT_ID = 74521 and RPT_DATE between current_date - 180 and current_date - 1"

    # Execute a command: create a table
    cur.execute(query)
    result = cur.fetchall()
    df = pd.DataFrame(result)
    df.to_csv("vertica_data.csv", index=False)
    print(df)
