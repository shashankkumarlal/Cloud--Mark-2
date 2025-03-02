import json
import boto3
import urllib3
import datetime

# Initialize S3 client
s3 = boto3.client('s3')

# URL to check
URL_TO_MONITOR = "https://www.reva.edu.in/"  # Change this to the website you want to monitor
BUCKET_NAME = "website-uptime-logs-04112004"

def lambda_handler(event, context):
    http = urllib3.PoolManager()
    response = http.request('GET', URL_TO_MONITOR)
    
    # Check if the website is up
    status = "UP" if response.status == 200 else "DOWN"
    
    # Create log entry
    log_data = {
        "timestamp": str(datetime.datetime.now()),
        "website": URL_TO_MONITOR,
        "status": status,
        "status_code": response.status
    }
    
    # Convert log to JSON format
    log_json = json.dumps(log_data, indent=4)
    
    # Generate a unique log file name
    file_name = f"uptime_log_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
    
    # Upload log file to S3
    s3.put_object(Bucket=BUCKET_NAME, Key=file_name, Body=log_json, ContentType="application/json")
    
    return {
        'statusCode': 200,
        'body': json.dumps(f"Website {URL_TO_MONITOR} is {status}. Log saved to S3.")
    }