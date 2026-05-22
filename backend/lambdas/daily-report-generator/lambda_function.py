import json
import boto3
from datetime import datetime

dynamodb = boto3.resource("dynamodb")

s3 = boto3.client("s3")

TABLE = dynamodb.Table("Attendance")

REPORT_BUCKET = "attendance-reports-jfn"

def lambda_handler(event, context):

    today_date = datetime.now().strftime("%Y-%m-%d")

    response = TABLE.scan()

    items = response.get("Items", [])

    daily_records = [

        item for item in items

        if item["date"] == today_date
    ]

    report_data = {

        "date": today_date,

        "total_records":
            len(daily_records),

        "records": daily_records
    }

    file_name = f"reports/{today_date}.json"

    s3.put_object(

        Bucket=REPORT_BUCKET,

        Key=file_name,

        Body=json.dumps(
            report_data,
            indent=4
        ),

        ContentType="application/json"
    )

    print("Daily report uploaded")

    return {
        "statusCode": 200,
        "body": "Report generated"
    }