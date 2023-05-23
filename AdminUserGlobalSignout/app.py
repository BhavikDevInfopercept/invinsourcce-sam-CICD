import json
import boto3
import boto3.exceptions
import os
USER_POOL_ID = "ap-south-1_UQWQN01Qj"



def lambda_handler(event, context):
    
    try:
        
        # Load the Cognito IDP client
        client = boto3.client('cognito-idp',region_name="ap-south-1")
        
        # load lambda client
        lambda_client = boto3.client("lambda",region_name="ap-south-1")
        
        inputParams= {
            "acc_token": event["headers"]["Authorization"]
        }
        
        inputParams["acc_token"] = inputParams["acc_token"][7:]
        
        username = event["body"]["email"]
        
        response = lambda_client.invoke(
            FunctionName = os.environ['FUNCTION_ARN'],
            InvocationType = 'RequestResponse',
            Payload = json.dumps(inputParams)
        )
        
        response_payload = response['Payload'].read().decode('utf-8')
        
        datas = json.loads(response_payload)
        
        if "admin" in datas["data"]["roles"]:
            response = client.admin_user_global_sign_out(
                UserPoolId=USER_POOL_ID,
                Username=username
            )
            return {
                'statusCode': response["ResponseMetadata"]["HTTPStatusCode"],
                'success': True,
                'message' : "logout successfully",
                'data': response
            }
        else:
            return {
                'statusCode': 400,
                'success': False,
                'message': "You don't have rights to perform this operation",
                'data': None
            }
    except client.exceptions.ResourceNotFoundException as e:
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
    except client.exceptions.NotAuthorizedException as e:
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
    except client.exceptions.InternalErrorException as e:
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
    
