import json
import boto3
import string
import random
import base64
import os


REGION = os.environ['REGION']

def generate_random_string(length):
    # Define the set of characters to choose from
    characters = string.ascii_letters + string.digits
    
    # Use random.choices to select a random character from the set for each position in the string
    random_string = ''.join(random.choices(characters, k=length))
    
    return random_string
    
def lambda_handler(event, context):
      # TODO implement
      
    s3 = boto3.client('s3')
    
    inputParams= {
         "acc_token": event["headers"]["Authorization"]
        }
    
    inputParams["acc_token"] = inputParams["acc_token"][7:]
        
    client = boto3.client('lambda')
    response = client.invoke(
        FunctionName = os.environ['FUNCTION_ARN'],
        InvocationType = 'RequestResponse',
        Payload = json.dumps(inputParams)
    )
    dynamodb = boto3.resource('dynamodb')
    client = boto3.client('dynamodb',region_name=REGION)
    table = dynamodb.Table('user')
    try:
        response_payload = response['Payload'].read().decode('utf-8')
        data= json.loads(response_payload)
        email= data['data']['email']
        
        response = table.get_item(Key={'email': email})
        
        if 'Item' in response:
                    
            user_data = response['Item']
            if user_data['email'] == email:
                
                # s3 = boto3.client("s3")
                
                # base64_image = event["base64_image"]
                base64_image=event['body']['base64_image']
                filename=generate_random_string(25)
                image_data = base64.b64decode(base64_image)
                
                bucket_name = "invinsource.com"
                object_key = f"profile-pic/{filename}.jpg"
                s3.put_object(Bucket=bucket_name, Key=object_key, Body=image_data)
                s3_url = s3.generate_presigned_url(
                    ClientMethod="get_object",
                    Params={"Bucket": bucket_name, "Key": object_key},
                    ExpiresIn=None
                )
                
                updatekey={'email': email}
                update_expression = 'SET image = :image'
                expression_attribute_values = {':image': s3_url}
                response = table.update_item(Key=updatekey,UpdateExpression=update_expression,ExpressionAttributeValues=expression_attribute_values)
                return {
                    'statusCode': response["ResponseMetadata"]["HTTPStatusCode"],
                    'success': True,
                    'message': "Here is your profile image link",
                    'data': s3_url
                }
            return {
            'statusCode': 400,
            'success': False,
            'message': "Error",
            'data': None   
        }
        # {
        #     'statusCode': 200,
        #     'body': json.dumps('Hello from Lambda!'),
        #     'parent': json.loads(response_payload)
        # }
    except:
        return {
            'statusCode': 400,
            'success': False,
            'message': f"Token Expire{e}",
            'data': None   
        }
    
