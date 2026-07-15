elete file · PY
import boto3
 
BUCKET_NAME = "techxxx-firstname-test-boto3"
FILE_NAME = "test.txt"
 
s3 = boto3.client("s3")
 
s3.delete_object(Bucket=BUCKET_NAME, Key=FILE_NAME)
 
print(f"Deleted {FILE_NAME} from {BUCKET_NAME}")
 