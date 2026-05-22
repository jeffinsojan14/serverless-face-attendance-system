import json
import boto3
from datetime import datetime

dynamodb = boto3.resource("dynamodb")

EMPLOYEE_TABLE = dynamodb.Table("Employees")
ATTENDANCE_TABLE = dynamodb.Table("Attendance")


def lambda_handler(event, context):

    today_date = datetime.now().strftime("%Y-%m-%d")

    employees_response = EMPLOYEE_TABLE.scan()

    employees = employees_response.get("Items", [])

    for employee in employees:

        employee_id = employee["employee_id"]

        attendance_response = ATTENDANCE_TABLE.get_item(
            Key={
                "employee_id": employee_id,
                "date": today_date
            }
        )

        attendance_item = attendance_response.get("Item")

        if not attendance_item:

            ATTENDANCE_TABLE.put_item(
                Item={
                    "employee_id": employee_id,
                    "date": today_date,
                    "status": "absent"
                }
            )

            print(f"{employee_id} marked absent")

    return {
        "statusCode": 200,
        "body": "Absent marking completed"
    }