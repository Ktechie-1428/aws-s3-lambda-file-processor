# S3 File Processor – Serverless Rename Pipeline

## 🚀 Highlights

- Event-driven serverless architecture  
- Triggered by S3 ObjectCreated events  
- Uses Python AWS Lambda for file processing  
- Implements IAM least-privilege role  
- Automatically renames/moves files into `processed/`  
- Includes CloudWatch logging for debugging  


## Overview
This project is a simple serverless file-processing pipeline built on AWS.

When a file is uploaded to an S3 bucket, an S3 event automatically triggers an AWS Lambda function written in Python. The function moves the file into a `processed/` folder by copying it to the new key and deleting the original object.

This pattern can be extended for virus scanning, image resizing, metadata tagging, and other backend file-processing workflows.

---

## Architecture

- **Amazon S3**
  - Stores uploaded files.
  - Emits `ObjectCreated` events to trigger the Lambda function.
- **AWS Lambda (Python 3.14)**
  - Handles the file processing logic.
  - Copies files into `processed/` and deletes the original.
- **AWS IAM**
  - Lambda execution role with:
    - `AWSLambdaBasicExecutionRole` (CloudWatch Logs)
    - Custom inline S3 policy (List, Get, Put, Delete for this bucket only).
- **Amazon CloudWatch Logs**
  - Captures Lambda logs for debugging and monitoring.

**Flow:**

1. User uploads a file to the S3 bucket.
2. S3 generates an `ObjectCreated` event.
3. The event triggers the `s3-file-processor` Lambda function.
4. The Lambda function:
   - Reads the bucket and object key from the event.
   - Skips any object already under `processed/`.
   - Copies the object to `processed/<original_key>`.
   - Deletes the original object.
5. The processed file is now stored under the `processed/` prefix.

---

## Technologies Used

- AWS S3
- AWS Lambda (Python 3.14)
- AWS IAM
- Amazon CloudWatch Logs
- Python
- boto3 (AWS SDK for Python)

---

## Deployment Steps (Console-Based)

1. **Create S3 bucket**
   - Region: `us-east-2` (Ohio)
   - Block all public access: ON
   - Default encryption: SSE-S3 (default)

2. **Create IAM role for Lambda**
   - Trusted entity: AWS service → Lambda
   - Attach policy: `AWSLambdaBasicExecutionRole`
   - Add inline S3 policy with:
     - Actions: `ListBucket`, `GetObject`, `PutObject`, `DeleteObject`
     - Resources: the specific S3 bucket and all its objects.

3. **Create Lambda function**
   - Runtime: Python 3.14
   - Use the existing IAM role from above.
   - Paste `lambda_function.py` code and deploy.

4. **Add S3 trigger**
   - Event source: S3
   - Event type: **All object create events**
   - Bucket: the S3 bucket created earlier.

5. **Test**
   - Upload a file to the bucket.
   - Verify that it ends up under the `processed/` prefix.
   - Check CloudWatch Logs to confirm the Lambda execution details.

---

## What I Learned

- How to build a basic serverless architecture with S3 + Lambda.
- How to configure IAM roles with least-privilege access.
- How to trigger Lambda from S3 events.
- How to debug Lambda executions using CloudWatch Logs.
