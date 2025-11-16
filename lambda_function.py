import json
import urllib.parse
import boto3

s3 = boto3.client("s3")

def lambda_handler(event, context):
    # Log the full event so we can see what S3 sends
    print("Received event:", json.dumps(event))

    # S3 can send multiple records, so we loop
    for record in event.get("Records", []):
        bucket_name = record["s3"]["bucket"]["name"]
        # Key is the file name/path
        object_key = urllib.parse.unquote_plus(
            record["s3"]["object"]["key"],
            encoding="utf-8"
        )

        # If it's already in the processed/ folder, do nothing
        if object_key.startswith("processed/"):
            print(f"Skipping already processed file: {object_key}")
            continue

        print(f"Processing file: {object_key} in bucket: {bucket_name}")

        # New key: put it inside processed/ folder
        new_key = f"processed/{object_key}"

        copy_source = {
            "Bucket": bucket_name,
            "Key": object_key,
        }

        # Copy the file to the new key
        s3.copy_object(
            Bucket=bucket_name,
            CopySource=copy_source,
            Key=new_key
        )

        # Delete the original file
        s3.delete_object(
            Bucket=bucket_name,
            Key=object_key
        )

        print(f"File renamed to: {new_key}")

    return {
        "statusCode": 200,
        "body": json.dumps("Success")
    }
