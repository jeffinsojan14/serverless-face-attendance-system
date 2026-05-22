import json
import boto3

dynamodb = boto3.resource("dynamodb")

TABLE = dynamodb.Table("Attendance")

def lambda_handler(event, context):

    try:

        response = TABLE.scan()

        items = response.get("Items", [])

        return {
            "statusCode": 200,

            "headers": {
                "Access-Control-Allow-Origin": "*"
            },

            "body": json.dumps(items)
        }

    except Exception as error:

        return {
            "statusCode": 500,
            "body": str(error)
        }