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
    
    # Load the Cognito IDP client
    client = boto3.client('cognito-idp',region_name=REGION)
    
    
    acc_token = event["headers"]["Authorization"]
    
    
    acc_token = acc_token[7:]
    
    # Sign up the new user
    try:
        resp = client.global_sign_out(
            AccessToken=acc_token
        )
        
        return {
            'statusCode': resp["ResponseMetadata"]["HTTPStatusCode"],
            'success': True,
            'message' : "You are Logged Out Successfully Globally",
            'data': resp
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
    except client.exceptions.PasswordResetRequiredException as e:
        return {
            'statusCode': 400,
            'success': False,
            'message': str(e),
            'data': None
        }
    except client.exceptions.UserNotConfirmedException as e:
        return {
            'statusCode': 400,
            'success': False,
            'message': str(e),
            'data': None
        }
    except client.exceptions.ForbiddenException as e:
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