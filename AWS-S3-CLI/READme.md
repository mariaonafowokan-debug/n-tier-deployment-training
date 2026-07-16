# AWS CLI and Python Boto3: Managing Amazon S3

## Overview

This explains how to manage Amazon S3 from an Ubuntu EC2 instance using:

- the **AWS Command Line Interface (AWS CLI)**
- the **AWS SDK for Python, Boto3**

The tasks covered are:

1. Launching and connecting to an EC2 instance
2. Installing the AWS CLI and Python dependencies
3. Authenticating with AWS
4. Managing S3 using AWS CLI commands
5. Managing S3 using six separate Python Boto3 scripts
6. Uploading the completed scripts to GitHub

---

## Table of Contents

- [0. What is Amazon S3?](#0-what-is-amazon-s3)
- [1. Launch the EC2 Instance](#1-launch-the-ec2-instance)
- [2. Install the AWS CLI](#2-install-the-aws-cli)
- [3. Set Up the Python Environment](#3-set-up-the-python-environment)
- [4. Authenticate with AWS](#4-authenticate-with-aws)
- [5. Manage S3 Using the AWS CLI](#5-manage-s3-using-the-aws-cli)
- [6. Manage S3 Using Python Boto3](#6-manage-s3-using-python-boto3)
- [7. Definition of Done Checklist](#7-definition-of-done-checklist)
- [8. Scripts Repository](#8-scripts-repository)

---

## What is S3?

#### S3 (Simple Storage Service) is used to securely store and retrieve any amount of data, at any time, from anywhere over the internet. 

- It can be used to store application files, images, backups, log files, data archives and host a static website by storing HTML, CSS, JS and other static files.
- It provides built-in redundancy: by default, 3 copies of your data are stored, each in a different Availability Zone (AZ) within the region.
- It can be accessed via the AWS Console, the AWS CLI, or Python (boto3) and this document covers the last two.


### In S3:

- A **bucket** is the container used to store data.
- An **object** is a file stored inside a bucket.
- An **object key** is the name or path used to identify the object.

Example:

```text
Bucket: techxxx-firstname-test-boto3
└── test.txt
```




### S3 can be accessed through:

- the AWS Management Console
- the AWS CLI
- AWS SDKs, including Python Boto3

This guide focuses on the AWS CLI and Boto3.

---

## 1. Launch the EC2 Instance

An existing Ubuntu EC2 instance can be used. Alternatively, launch a new instance with the following settings:

| Setting | Value |
|---|---|
| Name | `tech610-maria-s3-boto3-task` |
| AMI | Ubuntu Server 24.04 LTS |
| Instance type | A suitable free-tier-eligible instance type |
| Security group | Allow SSH on port 22 from your IP address |

### Connect to the instance

From the machine containing your private key:

```bash
ssh -i "your-key.pem" ubuntu@<EC2-PUBLIC-IP>
```

Replace:

- `your-key.pem` with the name of your private key
- `<EC2-PUBLIC-IP>` with the instance's public IP address

---

## 2. Install the AWS CLI

### Step 1: Update the package list

```bash
sudo apt update -y
```

This refreshes Ubuntu's list of available packages.

### Step 2: Upgrade existing packages

```bash
sudo apt upgrade -y
```

This installs available updates for packages already on the instance.

Although upgrading is not strictly required to install the AWS CLI, it helps ensure that the system has current security fixes and software updates.

### Step 3: Install the required utilities

```bash
sudo apt install unzip curl -y
```

These utilities are needed because:

- `curl` downloads the AWS CLI installation file.
- `unzip` extracts the downloaded ZIP archive.

### Step 4: Download AWS CLI version 2

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
```


### Step 5: Extract the installer

```bash
unzip awscliv2.zip
```

### Step 6: Run the installer

```bash
sudo ./aws/install
```

> **Expected Output**
> `You can now run: /usr/local/bin/aws --version`

### Step 7: Verify the installation of the correct AWS version

```bash
aws --version
```

> **Expected Output**
> **aws-cli/2.35.22 Python/3.14.6 Linux/6.17.0-1017-aws exe/x86_64.ubuntu.24


### Step 8: Remove the installation files

After confirming that the AWS CLI works:

```bash
rm -rf aws awscliv2.zip
```

---

## 3. Set Up the Python Environment

Boto3 is the official AWS SDK for Python. It allows Python programs to communicate with services such as Amazon S3.

### Step 1: Install Python and virtual environment support

```bash
sudo apt install python3 python3-pip python3-venv -y
```

### Step 2: Create a project directory

```bash
mkdir s3-boto3-task
cd s3-boto3-task
```

### Step 3: Create a virtual environment

```bash
python3 -m venv venv
```

A virtual environment keeps the packages for this project separate from Ubuntu's system Python installation.

### Step 4: Activate the virtual environment

```bash
source venv/bin/activate
```

When it is active, the terminal prompt should begin with:

```text
(venv)
```

### Step 5: Install Boto3

```bash
pip install boto3
```

### Step 6: Confirm that Boto3 is installed

```bash
pip show boto3
```

Alternatively:

```bash
python3 -c "import boto3; print(boto3.__version__)"
```

The virtual environment must be activated before running the Boto3 scripts in this guide.

---

## 4. Authenticate with AWS

#### Log in to gain access to AWS CLI (Command Line interface) and give it your credentials
*This is so that you can run commands using AWS. AWS CLI and Boto3 must have valid AWS credentials and permission to access S3.*


```bash
aws configure
```


**Note:** There's some things you can do on AWS CLI that you can't on GUI, which is why we follow the next steps to give us access to do what we would usually do in an AWS console, but locally:

#### Enter the following values when prompted:

```text
AWS Access Key ID: <your-access-key>
AWS Secret Access Key: <your-secret-key>
Default region name: eu-west-1
Default output format: json
```
> Then '`clear`' to clear the terminal, so that credentials are not in plain sight


The command stores the information in:

```text
~/.aws/credentials
~/.aws/config
```

Boto3 checks these files automatically, so access keys do not need to be written inside the Python scripts.

> **Security:** Never add access keys to Python files, screenshots, documentation, or GitHub. Never share the contents of `~/.aws/credentials`.


### Then test access to S3:

```bash
aws s3 ls
```
> **Expected output:**
> This displays the buckets the IAM identity has permission to view. No output may be shown if the account does not yet contain any buckets.

---

## 5. Manage S3 Using the AWS CLI

This section demonstrates the same basic S3 operations that will later be completed using Python Boto3.

> **Important:** S3 bucket names must be globally unique e.g.:

```text
tech610-maria-test-boto3
```

### Step 1: Create an S3 bucket


```bash
aws s3 mb s3://techxxx-firstname-test-boto3 
```


### Step 2: List the account's buckets

```bash
aws s3 ls
```

> **Expected Output:**
> Among the other buckets (aws storage spaces) you should see yours e.g.`2026-07-14 11:21:00 tech610-maria-first-bucket`


The newly created bucket should appear in the output.

### Step 3: List the contents of the bucket

```bash
aws s3 ls s3://tech610-maria-test-boto3
```
> **Expected Output:**
> It should come back with all the files in your bucket. If there's nothing in the bucket, it will not give any output, it will be blank and just jump to the next command line. 


### Step 4: Create a test file

```bash
echo "This is a test file for the S3 task." > test.txt
```

Check its contents:

```bash
cat test.txt
```

### Step 5: Upload the file

```bash
aws s3 cp test.txt s3://tech610-maria-test-boto3/test.txt
```

> **Expected Output:**
> test-boto3
Completed 38 Bytes/38 Bytes (419 Bytes/s) with 1 file(s) remaininupload: ./test.txt to s3://tech610-maria-first-bucket/test.txt    


In S3 terminology, the uploaded file is now an **object**.

### Step 6: Confirm that the object was uploaded

```bash
aws s3 ls s3://techxxx-firstname-test-boto3
```

>**Expected Output:**
>ket
2026-07-14 11:32:52         38 test.txt


### Check:
Listed files inside the bucket:
```bash
ls
```
>**Expected Output:**
> aws  awscliv2.zip  test.txt


### The directory:
```bash
pwd
```
>**Expected Output:**
> /home/ubuntu


### Step 7: Download the object

Create a directory for downloaded files:

```bash
mkdir -p downloads
```

Download the object:

```bash
aws s3 cp s3://techxxx-firstname-test-boto3/test.txt downloads/downloaded-test.txt
```

Confirm that it was downloaded:

```bash
ls -l downloads
cat downloads/downloaded-test.txt
```

### ⚠️ Step 8: Delete the object

```bash
aws s3 rm s3://tech610-maria-test-boto3/test.txt
```

Confirm that the bucket is empty:

```bash
aws s3 ls s3://tech610-maria-test-boto3
```

### ⚠️ Step 9: Delete the empty bucket

```bash
aws s3 rb s3://tech610-maria-test-boto3
```

Confirm that the bucket has been removed:

```bash
aws s3 ls
```

### 🤯 Dangerous S3 Commands 🤯

The following commands can immediately delete multiple resources:

```bash
aws s3 rm s3://tech610-maria-test-boto3 --recursive
```

This deletes every object in the named bucket.

```bash
aws s3 rb s3://tech610-maria-test-boto3 --force
```

This deletes the objects and then removes the bucket.

Always check the bucket name carefully before using either command.

---

## 6. Manage S3 Using Python Boto3

The Definition of Done requires a separate Python script for each operation.

The project should contain:

```text
s3-boto3-task/
├── create_bucket.py
├── delete_bucket.py
├── delete_file.py
├── download_file.py
├── list_buckets.py
├── upload_file.py
├── test.txt
└── requirements.txt
```

The six scripts are:

| Script | Purpose |
|---|---|
| `list_buckets.py` | Lists the S3 buckets the user can access |
| `create_bucket.py` | Creates a new S3 bucket |
| `upload_file.py` | Uploads `test.txt` to the bucket |
| `download_file.py` | Downloads the object from S3 |
| `delete_file.py` | Deletes the object from the bucket |
| `delete_bucket.py` | Deletes the empty bucket |

### Shared bucket name

Use the same globally unique bucket name in all relevant scripts:

```python
BUCKET_NAME = "tech610-maria-test-boto3"
```

The name used in one script must match the name used in the others.

### Run the scripts

Activate the virtual environment:

```bash
cd ~/s3-boto3-task
source venv/bin/activate
```

Run the scripts in this order:

```bash
python3 list_buckets.py
python3 create_bucket.py
python3 upload_file.py
python3 download_file.py
python3 delete_file.py
python3 delete_bucket.py
```

### How the scripts work

Each script begins by importing Boto3:

```python
import boto3
```

It then creates an S3 client:

```python
s3 = boto3.client("s3")
```

The client allows the script to send requests to the Amazon S3 API.

The main methods used are:

| Boto3 method | Purpose |
|---|---|
| `list_buckets()` | Returns the S3 buckets available to the authenticated identity |
| `create_bucket()` | Creates an S3 bucket |
| `upload_file()` | Uploads a local file as an S3 object |
| `download_file()` | Downloads an S3 object |
| `delete_object()` | Deletes an object from a bucket |
| `delete_bucket()` | Deletes an empty bucket |

Boto3 automatically uses the credentials and Region configured through the AWS CLI. Therefore, credentials must not be hard-coded into any script.

## Save the dependency

Create a record of the Python dependency:

```bash
pip freeze > requirements.txt
```

Another user can then install the dependency using:

```bash
pip install -r requirements.txt
```

---

## Reflection: 
I learnt to use the AWS CLI and Python Boto3 to manage Amazon S3 resources. The task helped me to understand how to authenticate with AWS, perform common S3 operations, and automate those tasks using simple Python scripts. Overall, it strengthened my understanding of how S3 can be managed both manually and programmatically.
