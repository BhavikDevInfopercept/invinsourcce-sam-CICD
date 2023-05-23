import json
import boto3
import boto3.exceptions
import os

# Define user pool details
USER_POOL_ID = os.environ['USER_POOL_ID']
REGION = os.environ['REGION']


def lambda_handler(event, context):
    
    try:
        
        # load lambda client
        lambda_client = boto3.client("lambda",region_name=REGION)
        
        # Load the Cognito IDP client
        client = boto3.client('cognito-idp',region_name=REGION)
        
        inputParams= {
            "acc_token": event["headers"]["Authorization"]
        }
        
        inputParams["acc_token"] = inputParams["acc_token"][7:]
        
        email = event["body"]["email"]
    
        
        response = lambda_client.invoke(
            FunctionName = os.environ['FUNCTION_ARN'],
            InvocationType = 'RequestResponse',
            Payload = json.dumps(inputParams)
        )
        
        response_payload = response['Payload'].read().decode('utf-8')
        
        datas = json.loads(response_payload)
        
        if "admin" in datas["data"]["roles"]:
            response = client.admin_remove_user_from_group(
                UserPoolId=USER_POOL_ID,
                Username=email,
                GroupName='user'
            )
            
            if response["ResponseMetadata"]["HTTPStatusCode"]:
                resp = client.admin_add_user_to_group(
                    UserPoolId=USER_POOL_ID,
                    Username=email,
                    GroupName='admin'
                )
            
                return {
                    'statusCode': resp["ResponseMetadata"]["HTTPStatusCode"],
                    'success': True,
                    'message' : f"You make {email} as admin",
                    'data': None
                }
            else:
                return {
                    'statusCode': 400,
                    'success': False,
                    'message' : "Operation Failed!!! Something Went Wrong",
                    'data': None
                }
        else:
            return {
                'statusCode': 400,
                'success': False,
                'message' : "You don't have rights to perform this operation",
                'data': None
            }
    except client.exceptions.InvalidParameterException as e:
        return {
            'statusCode': 400,
            'success': False,
            'message' : None,
            'data': str(e)
        }
    except client.exceptions.ResourceNotFoundException as e:
        return {
            'statusCode': 400,
            'success': False,
            'message' : None,
            'data': str(e)
        }
    except client.exceptions.TooManyRequestsException as e:
        return {
            'statusCode': 400,
            'success': False,
            'message' : None,
            'data': str(e)
        }
    except client.exceptions.NotAuthorizedException as e:
        return {
            'statusCode': 400,
            'success': False,
            'message' : None,
            'data': str(e)
        }
    except client.exceptions.UserNotFoundException as e:
        return {
            'statusCode': 400,
            'success': False,
            'message' : None,
            'data': str(e)
        }
    except client.exceptions.InternalErrorException as e:
        return {
            'statusCode': 400,
            'success': False,
            'message' : None,
            'data': str(e)
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'success': False,
            'message' : None,
            'data': str(e)
        }