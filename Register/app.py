import json
import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import datetime
import os

# Define user pool details
USER_POOL_ID = os.environ['USER_POOL_ID']
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
REGION = os.environ['REGION']

dynamodb = boto3.resource('dynamodb')
table_name = 'user'

# Create secret hash
def get_shash(username):
    # convert str to bytes
    key = bytes(CLIENT_SECRET, 'latin-1')  
    msg = bytes(username + CLIENT_ID, 'latin-1')  
    digest = hmac.new(key, msg, hashlib.sha256).digest()   
    return base64.b64encode(digest).decode()


def throwError(e):
    return {
        'statusCode': 400,
        'success': False,
        'message': str(e),
        'data': None
    }


def lambda_handler(event, context):
    try:
        client = boto3.client("cognito-idp",region_name=REGION)
        
        name=event["body"]["name"]
        phone=event["body"]["phone"]
        password = event["body"]["password"]
        email=event["body"]["email"]
        nda=event["body"]['nda']
        work_exprience=event["body"]['work_experience']
        bg_test=event["body"]['bg_test']
        apt_test=event["body"]['apt_test']
        technical_experience=event["body"]['technical_experience']
        meta=event["body"]['meta']
        
        table = dynamodb.Table(table_name)
        
        user_attributes = [
            {
                "Name": "email",
                "Value": email
            }
        ]
        
        secret_hash = get_shash(email)
        
        resp = client.sign_up(
            ClientId=CLIENT_ID,
            Username=email,
            Password=password,
            UserAttributes=user_attributes,
            SecretHash = secret_hash
        )
        
        if resp["ResponseMetadata"]["HTTPStatusCode"]:
            response = client.admin_add_user_to_group(
                UserPoolId=USER_POOL_ID,
                Username=email,
                GroupName='user'
            )
            
            if response["ResponseMetadata"]["HTTPStatusCode"]:
            
                item = {
                    'username': name,
                    'phone': phone,
                    'email': email,
                    'nda':nda,
                    'work_experience':work_exprience,
                    'bg_test':bg_test,
                    'apt_test':apt_test,
                    'userstatus':True,
                    'userrole':'user',
                    'technical_experience':technical_experience,
                    'meta':meta,
                    'image':''
                }
                
                table.put_item(Item=item)
        
            return {
                'statusCode': resp["ResponseMetadata"]["HTTPStatusCode"],
                'success': True,
                'message': "Please check your email for sign up confirmation code",
                'data': resp
            }
    except client.exceptions.ResourceNotFoundException as e:
        throwError(e)
    except client.exceptions.InvalidParameterException as e:
        throwError(e)
    except client.exceptions.UnexpectedLambdaException as e:
        throwError(e)
    except client.exceptions.UserLambdaValidationException as e:
        throwError(e)
    except client.exceptions.NotAuthorizedException as e:
        throwError(e)
    except client.exceptions.InvalidPasswordException as e:
        throwError(e)
    except client.exceptions.UsernameExistsException as e:
        throwError(e)
    except client.exceptions.TooManyRequestsException as e:
        throwError(e)
    except client.exceptions.InternalErrorException as e:
        throwError(e)
    except client.exceptions.InvalidSmsRoleAccessPolicyException as e:
        throwError(e)
    except client.exceptions.InvalidSmsRoleTrustRelationshipException as e:
        throwError(e)
    except client.exceptions.InvalidEmailRoleAccessPolicyException as e:
        throwError(e)
    except client.exceptions.CodeDeliveryFailureException as e:
        throwError(e)
    except client.exceptions.ForbiddenException as e:
        throwError(e)
    except Exception as e:
        throwError(e)