import json
import boto3
from urllib.parse import unquote_plus

rekognition = boto3.client("rekognition")
dynamodb = boto3.resource("dynamodb")

EMPLOYEE_TABLE = dynamodb.Table("Employees")

COLLECTION_ID = "employee-face-collection"

def lambda_handler(event, context):

    for record in event['Records']:

        bucket = record['s3']['bucket']['name']

        key = unquote_plus(
            record['s3']['object']['key']
        )

        employee_id = key.split("/")[-1].split(".")[0]

        response = rekognition.index_faces(

            CollectionId=COLLECTION_ID,

            Image={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': key
                }
            },

            ExternalImageId=employee_id,

            MaxFaces=1,

            QualityFilter="AUTO",

            DetectionAttributes=[]
        )

        EMPLOYEE_TABLE.put_item(

            Item={
                "employee_id": employee_id,
                "image_key": key
            }
        )

        print("Employee Registered:", employee_id)

    return {
        "statusCode": 200
    }