import json
import boto3
import botocore.exceptions
import os


# Define user pool details
USER_POOL_ID = os.environ['USER_POOL_ID']
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
REGION = os.environ['REGION']


def lambda_handler(event, context):
    
    try:
        
        # load lambda client
        lambda_client = boto3.client("lambda",region_name="ap-south-1")
        
        # Load the Cognito IDP client
        client = boto3.client('cognito-idp',region_name="ap-south-1")
        
        inputParams= {
            "acc_token": event["headers"]["Authorization"]
        }
        
        inputParams["acc_token"] = inputParams["acc_token"][7:]
        
        response = lambda_client.invoke(
            FunctionName = os.environ['FUNCTION_ARN'],
            InvocationType = 'RequestResponse',
            Payload = json.dumps(inputParams)
        )
        
        response_payload = response['Payload'].read().decode('utf-8')
        
        datas = json.loads(response_payload)
        
        if "admin" in datas["data"]["roles"]:
        
            email = event['body']["email"]
        
            # Connect to the DynamoDB table
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('user')
            
            # Retrieve the user data based on the email
            response = table.get_item(
                Key={
                    'email': email
                }
            )
            
            if 'Item' in response:
                
                updatekey={'email': email}
                update_expression = 'SET userstatus = :status'
                expression_attribute_values = {':status': 'true'}
                
                response = table.update_item(
                    Key=updatekey,
                    UpdateExpression=update_expression,
                    ExpressionAttributeValues=expression_attribute_values
                )
                
                if response["ResponseMetadata"]["HTTPStatusCode"]:
                
                    response = client.admin_enable_user(
                        UserPoolId=USER_POOL_ID,
                        Username=email
                    )
                
                    return {
                        'statusCode': response["ResponseMetadata"]["HTTPStatusCode"],
                        'success': True,
                        'message' : "User Enabled Successfully",
                        'data': response
                    }
                else:
                    return {
                        'statusCode': 400,
                        'success': False,
                        'message' : "Error in DB",
                        'data': response
                    }
            else:
                return {
                'statusCode': 400,
                'success': False,
                'message': "Email address not found",
                'data': None
            }
        else:
            return {
                'statusCode': 400,
                'success': False,
                'message': "You don't have admin rights",
                'data': None
            }
    except client.exceptions.UserNotFoundException as e:
        return {
            'statusCode': 400,
            'success': False,
            'message': str(e),
            'data': None
        }
    except client.exceptions.InvalidParameterException as e:
        return {
            'statusCode': 400,
            'success': False,
            'message': str(e),
            'data': None
        }
    except client.exceptions.TooManyRequestsException as e:
        return {
            'statusCode': 400,
            'success': False,
            'message': str(e),
            'data': None
        }
    except client.exceptions.NotAuthorizedException as e:
        return {
            'statusCode': 400,
            'success': False,
            'message': str(e),
            'data': None
        }
    except client.exceptions.InternalErrorException as e:
        return {
            'statusCode': 400,
            'success': False,
            'message': str(e),
            'data': None
        }
    except client.exceptions.ResourceNotFoundException as e:
        return {
            'statusCode': 400,
            'success': False,
            'message': str(e),
            'data': None
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'success': False,
            'message': str(e),
            'data': None
        }