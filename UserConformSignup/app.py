import json
import boto3
import boto3.exceptions
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
    
    try:
        client = boto3.client('cognito-idp',region_name=REGION)
        
        email = event["body"]["email"]
        code = event["body"]["code"]
    
        secret_hash = get_shash(email)
        resp = client.confirm_sign_up(
            ClientId = CLIENT_ID,
            SecretHash=secret_hash,
            Username=email,
            ConfirmationCode=code,
            ForceAliasCreation=False
        )

        return {
            'statusCode': resp["ResponseMetadata"]["HTTPStatusCode"],
            'success': True,
            'message': f"Signup confirmed for user: {email}",
            'data': resp
            
        }

    except client.exceptions.UserNotFoundException as e:
        return {
            'statusCode': 400,
            'success': False,
            'message': "Username doesnt exists",
            'data': None   
        }
    except client.exceptions.CodeMismatchException as e:
        return {
            'statusCode': 400,
            'success': False,
            'message': "Username doesnt exists",
            'data': None   
        }
    except client.exceptions.NotAuthorizedException as e:
        return {
            'statusCode': 400,
            'success': False,
            'message': "Username doesnt exists",
            'data': None   
        }
    except client.exceptions.ResourceNotFoundException as e:
        return {
            'statusCode': 400,
            'success': False,
            'message': "Username doesnt exists",
            'data': None   
        }
    except client.exceptions.InvalidParameterException as e:
        return {
            'statusCode': 400,
            'success': False,
            'message': "Username doesnt exists",
            'data': None   
        }
    except client.exceptions.UnexpectedLambdaException as e:
        return {
            'statusCode': 400,
            'success': False,
            'message': "Username doesnt exists",
            'data': None   
        }
    except client.exceptions.UserLambdaValidationException as e:   
        return {
            'statusCode': 400,
            'success': False,
            'message': "Username doesnt exists",
            'data': None   
        }
    except client.exceptions.TooManyFailedAttemptsException as e:
        return {
            'statusCode': 400,
            'success': False,
            'message': "Username doesnt exists",
            'data': None   
        }
    except client.exceptions.ExpiredCodeException as e:
        return {
            'statusCode': 400,
            'success': False,
            'message': "Username doesnt exists",
            'data': None   
        }
    except client.exceptions.InvalidLambdaResponseException as e:
        return {
            'statusCode': 400,
            'success': False,
            'message': "Username doesnt exists",
            'data': None   
        }
    except client.exceptions.AliasExistsException as e:
        return {
            'statusCode': 400,
            'success': False,
            'message': "Username doesnt exists",
            'data': None   
        }
    except client.exceptions.TooManyRequestsException as e:
        return {
            'statusCode': 400,
            'success': False,
            'message': "Username doesnt exists",
            'data': None   
        }
    except client.exceptions.LimitExceededException as e:
        return {
            'statusCode': 400,
            'success': False,
            'message': "Username doesnt exists",
            'data': None   
        }
    except client.exceptions.InternalErrorException as e:
        return {
            'statusCode': 400,
            'success': False,
            'message': "Username doesnt exists",
            'data': None   
        }
    except client.exceptions.ForbiddenException as e:
        return {
            'statusCode': 400,
            'success': False,
            'message': "Username doesnt exists",
            'data': None   
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'success': False,
            'message': "Username doesnt exists",
            'data': None   
        }
