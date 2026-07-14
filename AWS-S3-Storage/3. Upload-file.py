import boto3
 
BUCKET_NAME = "techxxx-firstname-test-boto3"
FILE_NAME = "test.txt"
 
s3 = boto3.client("s3")
 
# create a simple local file to upload
with open(FILE_NAME, "w") as f:
    f.write("Hello from boto3!")
 
s3.upload_file(FILE_NAME, BUCKET_NAME, FILE_NAME)
 
print(f"Uploaded {FILE_NAME} to {BUCKET_NAME}")
 