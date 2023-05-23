import boto3
import os

def lambda_handler(event, context):
    
    # Get the pre-signed URL from DynamoDB
    previous_presigned_url = event['url']
    
    s3 = boto3.client('s3',region_name = 'ap-south-1')
   
    filename = previous_presigned_url.split("/")[-1]
    
    filename = filename.split("?")[0]
    
    # Delete the object from the S3 bucket
    res = s3.delete_object(Bucket="invinsource.com", Key=f"profile-pic/{filename}")
    
    return res
