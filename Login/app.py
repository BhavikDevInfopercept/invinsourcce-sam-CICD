import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import json
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
    

# Initiate authentication
def initiate_auth(client, username, password):
    secret_hash = get_shash(username)
    
    try:
        resp = client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'SECRET_HASH': secret_hash,
                'PASSWORD': password,
            }
        )
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
    except client.exceptions.InvalidSmsRoleAccessPolicyException as e:
        return {
            'statusCode': 400,
            'success': False,
            'message': str(e),
            'data': None
        }
    except client.exceptions.InvalidSmsRoleTrustRelationshipException as e:
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
    except client.exceptions.InvalidUserPoolConfigurationException as e:
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
    except Exception as e:
        return {
            'statusCode': 400,
            'success': False,
            'message': str(e),
            'data': None
        }
    return resp

def lambda_handler(event, context):

    # Load the Cognito IDP client
    client = boto3.client('cognito-idp',region_name=REGION)
    
    email = event["email"]
    password = event["password"]
    
    resp = initiate_auth(client, email, password)
    
    if resp.get("AuthenticationResult"):
        return {
            'statusCode': resp["ResponseMetadata"]["HTTPStatusCode"],
            'success': True,
            'message' : "Login Successfull",
            'data': {
                'id_token': resp["AuthenticationResult"]["IdToken"],
                'refresh_token': resp["AuthenticationResult"]["RefreshToken"],
                'access_token': resp["AuthenticationResult"]["AccessToken"],
                'expires_in': resp["AuthenticationResult"]["ExpiresIn"],
                'token_type': resp["AuthenticationResult"]["TokenType"] 
            }
        }
    else:
        return {
            'statusCode': 400,
            'success': False,
            'message' : "Login Failed",
            'data': resp
        }
    