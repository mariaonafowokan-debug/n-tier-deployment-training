import boto3
 
BUCKET_NAME = "techxxx-firstname-test-boto3"  # change this to something unique
REGION = "eu-west-1"  # change to your region
 
s3 = boto3.client("s3", region_name=REGION)
 
s3.create_bucket(
    Bucket=BUCKET_NAME,
    CreateBucketConfiguration={"LocationConstraint": REGION}
)
 
print(f"Created bucket: {BUCKET_NAME}")
 