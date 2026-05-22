import json
import boto3
from urllib.parse import unquote_plus
from datetime import datetime
from zoneinfo import ZoneInfo

rekognition = boto3.client("rekognition")

dynamodb = boto3.resource("dynamodb")

ATTENDANCE_TABLE = dynamodb.Table("Attendance")

COLLECTION_ID = "employee-face-collection"

CONFIDENCE_THRESHOLD = 90


def lambda_handler(event, context):

    for record in event['Records']:

        bucket = record['s3']['bucket']['name']

        key = unquote_plus(
            record['s3']['object']['key']
        )

        try:

            response = rekognition.search_faces_by_image(

                CollectionId=COLLECTION_ID,

                Image={
                    'S3Object': {
                        'Bucket': bucket,
                        'Name': key
                    }
                },

                FaceMatchThreshold=CONFIDENCE_THRESHOLD,

                MaxFaces=1
            )

            matches = response['FaceMatches']

            if len(matches) == 0:

                print("Unknown Face")

                return {
                    "statusCode": 404,
                    "body": "Face not recognized"
                }

            matched_face = matches[0]

            employee_id = matched_face['Face'][
                'ExternalImageId'
            ]

            confidence = matched_face['Similarity']

            print("Matched Employee:",
                  employee_id)

            print("Confidence:",
                  confidence)

            process_attendance(employee_id)

        except Exception as error:

            print("Recognition Error:", error)

            return {
                "statusCode": 500,
                "body": str(error)
            }

    return {
        "statusCode": 200,
        "body": "Attendance processed"
    }


def process_attendance(employee_id):

    india_timezone = ZoneInfo("Asia/Kolkata")

    current_datetime = datetime.now(india_timezone)

    today_date = current_datetime.strftime("%Y-%m-%d")

    current_time = current_datetime.strftime("%H:%M:%S")

    print("Current IST Date:", today_date)

    print("Current IST Time:", current_time)

    response = ATTENDANCE_TABLE.get_item(

        Key={
            "employee_id": employee_id,
            "date": today_date
        }
    )

    item = response.get("Item")

    if not item:

        status = determine_status(current_time)

        ATTENDANCE_TABLE.put_item(

            Item={
                "employee_id": employee_id,
                "date": today_date,
                "clock_in": current_time,
                "status": status
            }
        )

        print("Clock-In Added")

    else:

        if "clock_out" in item:

            print("Attendance Already Completed For Today")

            return

        ATTENDANCE_TABLE.update_item(

            Key={
                "employee_id": employee_id,
                "date": today_date
            },

            UpdateExpression=
            "SET clock_out = :clock_out",

            ExpressionAttributeValues={
                ":clock_out": current_time
            }
        )

        print("Clock-Out Added")


def determine_status(current_time):

    office_start_time = "09:30:00"

    if current_time > office_start_time:

        return "late"

    return "present"