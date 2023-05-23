import json
import boto3
import botocore.exceptions
import os


# Define user pool details
USER_POOL_ID = os.environ['USER_POOL_ID']
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
REGION = os.environ['REGION']

def global_signout(acc_token):
    try:
        client = boto3.client('cognito-idp',region_name=REGION)
        resp = client.global_sign_out(
            AccessToken=acc_token
        )
        return resp
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
    except Exception as e:
        return {
            'statusCode': 400,
            'success': False,
            'message': str(e),
            'data': None
        }


def lambda_handler(event, context):
    try:
        
        # load lambda client
        lambda_client = boto3.client("lambda",region_name=REGION)
        
        # Load the Cognito IDP client
        client = boto3.client('cognito-idp',region_name=REGION)
        
        pre_password = event["body"]["pre_password"]
        new_password = event["body"]["new_password"]
        
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
        
        if "user" in datas["data"]["roles"] or "admin" in datas["data"]["roles"]:
        
            resp=client.change_password(
                    PreviousPassword=pre_password,
                    ProposedPassword=new_password,
                    AccessToken=inputParams["acc_token"]
            )
            
            if resp["ResponseMetadata"]["HTTPStatusCode"]:
                global_signout(inputParams["acc_token"])
                
            else:
                return {
                    'statusCode': 400,
                    'success': False,
                    'message': "Error Occurred!",
                    'data': None
                }
                
            return {
                'statusCode': resp["ResponseMetadata"]["HTTPStatusCode"],
                'success': True,
                'message' : "Your password has been changed",
                'data': resp
            }
        else:
            return {
                'statusCode': 400,
                'success': False,
                'message': "You Don't have rights to perform this operation",
                'data': None
            }
    except client.exceptions.UserNotFoundException as e:
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
    except client.exceptions.LimitExceededException as e:
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
    except client.exceptions.ResourceNotFoundException as e:
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
            'message': "Invlid Token Or Token Expired!",
            'data': None
        }