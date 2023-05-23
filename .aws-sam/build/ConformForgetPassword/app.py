import json
import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import os


# Define user pool details
USER_POOL_ID = os.environ['USER_POOL_ID']
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
REGION = os.environ['REGION']

# Create secret hash
def get_shash(username):
    # convert str to bytes
    key = bytes(CLIENT_SECRET, 'latin-1')  
    msg = bytes(username + CLIENT_ID, 'latin-1')  
    digest = hmac.new(key, msg, hashlib.sha256).digest()   
    return base64.b64encode(digest).decode()
    
    


def lambda_handler(event, context):
    
    # Load the Cognito IDP client
    client = boto3.client('cognito-idp',region_name=REGION)
    
    email = event["body"]["email"]
    code = event["body"]["code"]
    new_password = event["body"]["new_password"]
    shash = get_shash(email)
    
    # Sign up the new user
    try:
        response = client.confirm_forgot_password(
            Username=email,
            ClientId=CLIENT_ID,
            ConfirmationCode=code,
            Password=new_password,
            SecretHash=get_shash(email)
            )
        
        return {
            'statusCode': response["ResponseMetadata"]["HTTPStatusCode"],
            'success': True,
            'message': "Forgot Password Successfully",
            'data': response
        }
    except client.exceptions.UserNotFoundException as e:
        return {
            'statusCode': 400,
            'success': False,
            'message': str(e),
            'data': None
        }
    except client.exceptions.InvalidPasswordException as e:
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
    except client.exceptions.UnexpectedLambdaException as e:
        return {
            'statusCode': 400,
            'success': False,
            'message': str(e),
            'data': None
        }
    except client.exceptions.InvalidLambdaResponseException as e:
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
    except client.exceptions.TooManyFailedAttemptsException as e:
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
    except client.exceptions.UserLambdaValidationException as e:
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
    except client.exceptions.LimitExceededException as e:
        return {
            'statusCode': 400,
            'success': False,
            'message': str(e),
            'data': None
        }
    except client.exceptions.ExpiredCodeException as e:
        return {
            'statusCode': 400,
            'success': False,
            'message': str(e),
            'data': None
        }
    except client.exceptions.CodeMismatchException as e:
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