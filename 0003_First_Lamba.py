''' Following is a snippet of a simple lambda which will be attached to the API Gateway (in script 0001_*, it was referred as
a dummy lambda). Lambda will listen to any events posted to the endpoint and once the lambda notices payload in the endpoint, 
the payload will be parsed and pushed into the kinesis stream.'''

import json
import boto3
from time import gmtime, strftime
import time


firehose_client = boto3.client('firehose')

def lambda_handler(event, context):
    event = json.dumps(event)
    data =  json.loads(event,strict=False) 
    keys = data.keys()
    
    # iterating the keys in the json. Only print out the values of the body parameters
    for keys in data:
        if keys == 'body':
            data[keys]['data_source']='sensor_data'
            var = str(json.dumps(data[keys]))+'\n'
            print(var) # for debugging purpose
            firehose_client.put_record(DeliveryStreamName='firehose_sensor_data',
            Record={'Data':var} )
