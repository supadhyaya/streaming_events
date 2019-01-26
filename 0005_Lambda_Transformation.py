
''' 
Following snippet shows how events can be stored into persistance layer and how formats of data can be changed.
'''

import boto3
import urllib
import json
import pyarrow as pa
import pandas as pd
import numpy as np
import pyarrow.parquet  as pq
import urllib



s3 = boto3.client('s3')

def lambda_handler(event, context):

    x = json.dumps(event)

    y = json.loads(x)

    key = event['Records'][0]['s3']['object']['key']

    bucket = 'sensor_data'

    data = s3.get_object(Bucket=bucket, Key=key)
    
    content = data['Body'].read().rstrip().decode("utf-8", "ignore")
    
    df = pd.DataFrame()
    
    lines = [line for line in content.split('\n')]
    
    # below for loop is changed as per business transformation needs.
    for line in lines:
        df1 = pd.DataFrame({'sensor_data' : 123TEST})
        df = df.append(df1)

    client = boto3.resource('s3')

    df.to_csv('/tmp/tmp.csv',index=False, sep=';')

    client.Object('sensor_data',+key+'.csv').put(Body=open('/tmp/tmp.csv', 'rb'))

    # process to create simplistic parquet using pyarrow package of python.
    table = pa.Table.from_pandas(df)

    pq.write_table(table,'/tmp/tmp.parquet')

    client.Object('sensor_data',+key+'.parquet').put(Body=open('/tmp/tmp.parquet', 'rb'))


