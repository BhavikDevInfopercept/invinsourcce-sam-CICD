import json
import boto3
import random
import base64
import string
import datetime
import time





def lambda_handler(event, context):
    try:
        
        client=boto3.client('lambda')
        
        inputParams= {
            "acc_token": event["headers"]["Authorization"]
         }
        inputParams["acc_token"] = inputParams["acc_token"][7:]
        response = client.invoke(
        FunctionName = os.environ['USER_POOL_ID'],
        InvocationType = 'RequestResponse',
        Payload = json.dumps(inputParams)
        )
        response_payload = response['Payload'].read().decode('utf-8')

        data= json.loads(response_payload)
        
        
        if "admin" in data['data']['roles']:
            email=data['data']['email']
            # return event
            name=event['body']["name"]
            phone=event['body']["phone"]
            nda=event['body']['nda']
            work_experience=event['body']['work_experience']
            bg_test=event['body']['bg_test']
            apt_test=event['body']['apt_test']
            technical_experience=event['body']['technical_experience']
            meta=event['body']['meta']
            try:
                base64_image=event['body']['base64_image']
                
                inputParams={
                    "email":email,
                    "name":name,
                    "phone":phone,
                    "nda":nda,
                    "work_experience":work_experience,
                    "bg_test":bg_test,
                    "apt_test":apt_test,
                    "technical_experience":technical_experience,
                    "meta":meta,
                    "base64_image":base64_image
                    
                    
                }
                
                response = client.invoke(
                FunctionName = 'arn:aws:lambda:ap-south-1:219435080300:function:isr-common-update-profile-call',
                InvocationType = 'RequestResponse',
                Payload = json.dumps(inputParams)
                )
                response_payload = response['Payload'].read().decode('utf-8')
                
                data= json.loads(response_payload)
                return {
                    'statusCode': response["ResponseMetadata"]["HTTPStatusCode"],
                    'success': True,
                    'message': "Update Profile successfully",
                    'data': None
                    
                }
            except:
                
                response = client.invoke(
                FunctionName = 'arn:aws:lambda:ap-south-1:219435080300:function:isr-common-update-profile-call',
                InvocationType = 'RequestResponse',
                Payload = json.dumps(inputParams)
                )
                response_payload = response['Payload'].read().decode('utf-8')

                data= json.loads(response_payload)
                return {
                    'statusCode': response["ResponseMetadata"]["HTTPStatusCode"],
                    'success': True,
                    'message': "Update Profile successfully",
                    'data': None
                    
                }
        else:
            return {
                'statusCode': 400,
                'success': False,
                'message': "You are Not Admin",
                'data': None   
            }
    except Exception as e:
        return {
            'statusCode': 400,
            'success': False,
            'message': f"Token Expire{e}",
            'data': None   
        }