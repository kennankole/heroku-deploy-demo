import boto3
from app.config import Config as AppConfig
from botocore.client import Config


acl = 'public-read'
fields = {"acl": acl, "Content-Type":  "image/jpeg"}
conditions = [
    {"acl": acl},
    ["starts-with", "$Content-Type", ""]
]

def s3_direct_upload(file_name):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AppConfig.AWS_ACCESS_ID,
        aws_secret_access_key=AppConfig.AW_SECRET_KEY,
        config=Config(signature_version='s3v4'),
        region_name='eu-central-1'
        
    )

    response = s3_client.generate_presigned_post(
                    Bucket=AppConfig.AWS_BUCKET_NAME,
                    Key=file_name,
                    ExpiresIn=3600,
                    Fields=fields,
                    Conditions=conditions
                )
    return response