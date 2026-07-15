import boto3
 
BUCKET_NAME = "techxxx-firstname-test-boto3"
FILE_NAME = "test.txt"
DOWNLOAD_AS = "downloaded_test.txt"
 
s3 = boto3.client("s3")
 
s3.download_file(BUCKET_NAME, FILE_NAME, DOWNLOAD_AS)
 
print(f"Downloaded {FILE_NAME} from {BUCKET_NAME} as {DOWNLOAD_AS}")
 