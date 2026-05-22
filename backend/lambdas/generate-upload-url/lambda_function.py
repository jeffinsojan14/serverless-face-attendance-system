import json
import boto3
import uuid

s3 = boto3.client("s3")

BUCKET_NAME = "attendance-images-jfn"

def lambda_handler(event, context):

    file_name = f"incoming/{uuid.uuid4()}.jpg"

    upload_url = s3.generate_presigned_url(
        ClientMethod='put_object',
        Params={
            'Bucket': BUCKET_NAME,
            'Key': file_name,
            'ContentType': 'image/jpeg'
        },
        ExpiresIn=60
    )

    return {
        "statusCode": 200,

        "headers": {
            "Access-Control-Allow-Origin": "*"
        },

        "body": json.dumps({
            "uploadURL": upload_url,
            "imageKey": file_name
        })
    }