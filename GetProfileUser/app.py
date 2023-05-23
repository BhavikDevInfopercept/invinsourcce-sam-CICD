import json
import boto3
import os


def lambda_handler(event, context):
      # TODO implement
    try:  
        client = boto3.client('lambda')
        
        inputParams= {
             "acc_token": event["headers"]["Authorization"]
            }
            
        inputParams["acc_token"] = inputParams["acc_token"][7:]
        
        response = client.invoke(
            FunctionName = os.environ['FUNCTION_ARN'],
            InvocationType = 'RequestResponse',
            Payload = json.dumps(inputParams)
        )
        
        response_payload = response['Payload'].read().decode('utf-8')
        
        return json.loads(response_payload)
    except Exception as e:
        return {
            'statusCode': 400,
        	'success': False,
        	'message' : str(e),
        	'data': None
        }

