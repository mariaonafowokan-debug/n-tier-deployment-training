import boto3
 
BUCKET_NAME = "techxxx-firstname-test-boto3"
 
s3 = boto3.client("s3")
 
s3.delete_bucket(Bucket=BUCKET_NAME)
 
print(f"Deleted bucket: {BUCKET_NAME}")
 