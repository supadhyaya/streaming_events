''' 
Once the payload is pushed into the kinesis stream via lambda, the data will persist in stream for serveral hours/days/months.
For further transforming the data which arrives at the kinesis stream, another lambda can be attached into the kinesis stream.
To do this, simple open the dashboard for the stream and add a lambda as a trigger. Following is the lambda which gets called
by the kinesis stream on insertion of new payload. The lambda below does simple transformation and calls another lambda which
then puts the data either into s3 or in any data persistance layer.
'''

import boto3
import json

s3 = boto3.client('s3')
iam = boto3.client('lambda', region_name='eu-west-1')

def lambda_handler(event, context):
    print('new file is added: '+ event['Records'][0]['s3']['object']['key'])
    
    # lambda calling another lambda. This is just for showing the functionality
    iam.invoke(FunctionName='0005_Lambda_Transformation',
                                 InvocationType='Event',
                                  Payload=json.dumps(event))
