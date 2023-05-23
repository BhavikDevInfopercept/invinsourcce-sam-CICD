import json
import boto3
import random
import base64
import string
import datetime
import time
import os



def lambda_handler(event, context):
    try:
        client=boto3.client('lambda')        
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

        data= json.loads(response_payload)
        
        
        if "user" in data['data']['roles']:
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
                FunctionName = os.environ['FUNCTION_ARN_Update'],
                InvocationType = 'RequestResponse',
                Payload = json.dumps(inputParams)
                )
                response_payload = response['Payload'].read().decode('utf-8')
                
                data= json.loads(response_payload)
                return {
                    'statusCode': response["ResponseMetadata"]["HTTPStatusCode"],
                    'success': True,
                    'message': "Update Profile successfully",
                    'data': data 
                }
            except:
                inputParams={
                    "email":email,
                    "name":name,
                    "phone":phone,
                    "nda":nda,
                    "work_experience":work_experience,
                    "bg_test":bg_test,
                    "apt_test":apt_test,
                    "technical_experience":technical_experience,
                    "meta":meta
                }
                response = client.invoke(
                FunctionName = os.environ['FUNCTION_ARN_Update'],
                InvocationType = 'RequestResponse',
                Payload = json.dumps(inputParams)
                )
                response_payload = response['Payload'].read().decode('utf-8')

                data= json.loads(response_payload)
                return {
                    'statusCode': response["ResponseMetadata"]["HTTPStatusCode"],
                    'success': True,
                    'message': "Update Profile successfully",
                    'data': data
                    
                }
        else:
            return {
                'statusCode': 400,
                'success': False,
                'message': "Record Not Found",
                'data': None   
            }
    except Exception as e:
        return {
                'statusCode': 400,
                'success': False,
                'message': f"Token Expire{e}",
                'data': None   
            }