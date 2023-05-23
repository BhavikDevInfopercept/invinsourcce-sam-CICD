import json
import boto3
import random
import base64
import string
import datetime
import time
def generate_random_string(length):
    # Define the set of characters to choose from
    characters = string.ascii_letters + string.digits
    
    # Use random.choices to select a random character from the set for each position in the string
    random_string = ''.join(random.choices(characters, k=length))
    
    return random_string


def lambda_handler(event, context):
    try:
        
        client = boto3.client('lambda')
        dynamodb = boto3.resource('dynamodb')
        table_name = 'user'
        table = dynamodb.Table(table_name)
        
        email = event['email']
        name = event["name"]
        phone = event["phone"]
        nda = event['nda']
        work_experience = event['work_experience']
        bg_test = event['bg_test']
        apt_test = event['apt_test']
        technical_experience = event['technical_experience']
        meta = event['meta']
        
        try:
            base64_image = event['base64_image']
            filename = generate_random_string(25)
            
            response = table.get_item(
                Key={
                    'email': email
                }
            )
            
            
            try:
                previous_presigned_url= response['Item']['image']
                s3 = boto3.client('s3',region_name = 'ap-south-1')
   
                filename = previous_presigned_url.split("/")[-1]
                
                filename = filename.split("?")[0]
                
                # Delete the object from the S3 bucket
                res = s3.delete_object(Bucket="invinsource.com", Key=f"profile-pic/{filename}")
            except:
                pass
            # Set update key value
            image_data = base64.b64decode(base64_image)
                        
            bucket_name = "invinsource.com"
            object_key = f"profile-pic/{filename}.jpg"
            s3.put_object(Bucket=bucket_name, Key=object_key, Body=image_data)
            s3_url = s3.generate_presigned_url(
                ClientMethod="get_object",
                Params={"Bucket": bucket_name, "Key": object_key},
                ExpiresIn=None
            )
            updatekey = {
                'email': email
            }
            
            update_expression = 'SET username = :username, phone = :phone, nda = :nda, work_experience = :work_experience, bg_test = :bg_test, apt_test = :apt_test, technical_experience = :technical_experience, meta = :meta, image = :image'
            
            expression_attribute_values = {
                ':username': name,
                ':phone': phone,
                ':nda': nda,
                ':work_experience': work_experience,
                ':bg_test': bg_test,
                ':apt_test': apt_test,
                ':technical_experience': technical_experience,
                ':meta': meta,
                ':image': s3_url
            }
            
            response = table.update_item(Key=updatekey,UpdateExpression=update_expression,ExpressionAttributeValues=expression_attribute_values)
            
            return {
                'statusCode': response["ResponseMetadata"]["HTTPStatusCode"],
                'success': True,
                'message': "Update Profile successfully with image",
                'data': response
            }
        
        except:
            response = table.get_item(
                Key={
                    'email': email
                }
            )
            updatekey = {
                'email': email
            }
            
            update_expression = 'SET username = :username, phone = :phone, nda = :nda, work_experience = :work_experience, bg_test = :bg_test, apt_test = :apt_test, technical_experience = :technical_experience, meta = :meta'
            
            expression_attribute_values = {
                ':username': name,
                ':phone': phone,
                ':nda': nda,
                ':work_experience': work_experience,
                ':bg_test': bg_test,
                ':apt_test': apt_test,
                ':technical_experience': technical_experience,
                ':meta': meta
                
            }
            
            return {
                'statusCode': response["ResponseMetadata"]["HTTPStatusCode"],
                'success': True,
                'message': "Update Profile successfully",
                'data': None
            }
    
    except Exception as e:
        return {
            'statusCode': 400,
            'success': False,
            'message': f"Token Expire {event}",
            'data': str(e)
        }
