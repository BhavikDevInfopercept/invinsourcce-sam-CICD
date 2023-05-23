import json
import boto3
import datetime
from decimal import Decimal
import os



dynamodb = boto3.resource('dynamodb')
client = boto3.client('dynamodb')
table = dynamodb.Table('user')
client1=boto3.client('lambda')


REGION = os.environ['REGION']
USER_POOL_ID = os.environ['USER_POOL_ID']



class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)
        
        
def lambda_handler(event, context):
    item={}
    itemdata=[]
    try:
        inputParams= {
            "acc_token": event["headers"]["Authorization"]
            }
            
        inputParams["acc_token"] = inputParams["acc_token"][7:]    
        
        response = client1.invoke(
        FunctionName = os.environ['FUNCTION_ARN'],
        InvocationType = 'RequestResponse',
        Payload = json.dumps(inputParams)
        )
        response_payload = response['Payload'].read().decode('utf-8')
    
        responcse= json.loads(response_payload)
        if responcse['statusCode']==200 and "admin" in responcse["data"]["roles"]:
            
            # Load the Cognito IDP client
            client = boto3.client('cognito-idp',region_name=REGION)
            
            response = client.list_users(
                UserPoolId=USER_POOL_ID,
            )
            
            # json_data = json.dumps(tuple(response["Users"]), cls=CustomJSONEncoder)
            data=response["Users"]
            for item in data:
                for key, value in item.items():
                    if key=="UserCreateDate" or key=="UserLastModifiedDate":
                        item[key] = value.isoformat()
            
    
            
            for item in data:
                attributes = item.get('Attributes', [])
                for attr in attributes:
                    user_dict = {
                        'UserCreateDate': item.get('UserCreateDate'),
                        'UserLastModifiedDate': item.get('UserLastModifiedDate'),
                        'UserStatus': item.get('UserStatus')
                    }
                    if attr.get('Name') == 'email':
                        email = attr.get('Value')
                        response = table.get_item(Key={'email': email})
                        if 'Item' in response:
                            user_data = response['Item']
                            if user_data['email'] == email:
                                # store item data in item dictionary
                                item={
                                    'email':user_data['email'],
                                    
                                    'apt_test':user_data['apt_test'],
                                    'bg_test':user_data['bg_test'],
                                    'meta':user_data['meta'],
                                    'nda':user_data['nda'],
                                    'phone':user_data['phone'],
                                    'technical_experience':user_data['technical_experience'],
                                    'updatedate':user_data['updatedate'],
                                    'name':user_data['username'],
                                    'role':user_data['userrole'],
                                    'status':user_data['userstatus'],
                                    'work_exprience':user_data['work_exprience']
                                }
                                item.update(user_dict)
                                itemdata.append(item)
            data=json.loads(json.dumps(itemdata, cls=DecimalEncoder))
            dict_object = {}
            for i, user in enumerate(itemdata):
                dict_object[f"user{i+1}"] = user
    
            # return data
            return {
            	'statusCode': 200,
            	'success': True,
            	'message' : "Invinsource all users",
            	'data': data
            }
            
        else:
            return {
            	'statusCode': 400,
            	'success': False,
            	'message' : "Token Expire",
            	'data': None
            }
    except:
        return {
            	'statusCode': 400,
            	'success': False,
            	'message' : "Something Went Wrong",
            	'data': None
            }

    
    
    
    
    
    
    
    
    
    
    
    # try:
    #         token = event["headers"]["Authorization"]
    #         identifier=event['identifier']
    #         dynamodb = boto3.resource('dynamodb')
    #         client = boto3.client('dynamodb')
    #         table = dynamodb.Table('user')
    #         response = table.get_item(
    #             Key={
    #                 'email': identifier
                   
    #                 }
    #             )
    #         # if item is there 
    #         if 'Item' in response:
    #             item = response['Item']
    #             expected_token = item['logintoken']
    #             if expected_token == token:
    #                 if(int(item['expirationtime'])>int(time.time())) and item['userrole']=='admin':
    #                         response = client.scan(TableName='user')
    #                         items = response['Items']
    #                         for item in items:
    #                             if 'password' in item:
    #                                 del item['password']
    #                                 del item['logintoken']
    #                         return {
    #                         'statusCode': 200,
    #                         'body': items,
                            
                            
    #                         }
    #                 else:
    #                     return {
    #                     'statusCode': 400,
    #                     'body': 'You are not Admin!'
    #                 }
    #             else:
    #                 return {
    #                     'statusCode': 400,
    #                     'body': 'Invalid token'
    #                 }
    # except Exception as e:
    #     return {'statusCode': 400,'body': 'Provide token','exception':f'{e}'}
