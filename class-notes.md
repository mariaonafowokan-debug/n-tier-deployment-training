# AWS CLI + Python boto3 S3 Task

## Overview
This document covers:

1. Setting up an EC2 instance
2. Installing dependencies for AWS CLI
3. Authenticating with AWS CLI
4. Basic S3 manipulation with AWS CLI
5. Six simple boto3 scripts that do the same things in Python


- [AWS CLI + Python boto3 S3 Task](#aws-cli--python-boto3-s3-task)
  - [Overview](#overview)
- [AWS CLI + Python boto3 S3 Task](#aws-cli--python-boto3-s3-task-1)
  - [0. What is S3?](#0-what-is-s3)
  - [1. Launch the EC2 instance](#1-launch-the-ec2-instance)
  - [2. Install dependencies for AWS CLI](#2-install-dependencies-for-aws-cli)
  - [3. Authenticate using AWS CLI](#3-authenticate-using-aws-cli)
  - [4. Manipulating S3 with the AWS CLI](#4-manipulating-s3-with-the-aws-cli)
  - [🤯 Dangerous commands 🤯](#-dangerous-commands-)
  - [4a. (Optional) Making files in your bucket publicly accessible](#4a-optional-making-files-in-your-bucket-publicly-accessible)
  - [5. Python boto3 scripts](#5-python-boto3-scripts)
    - [How the scripts work](#how-the-scripts-work)
  - [7. Definition of Done Checklist](#7-definition-of-done-checklist)
    - [EC2 and Dependencies](#ec2-and-dependencies)
    - [Authentication](#authentication)
    - [AWS CLI Operations](#aws-cli-operations)
    - [Python Boto3 Scripts](#python-boto3-scripts)
    - [Delivery](#delivery)
  - [8. Scripts Folder](#8-scripts-folder)

---
# AWS CLI + Python boto3 S3 Task


---

## 0. What is S3?

S3 (Simple Storage Service) is used to securely store and retrieve any amount of data, at any time, from anywhere over the internet. A few key points:

- It can be used to host a static website by storing HTML, CSS, JS and other static files.
- It provides built-in redundancy: by default, 3 copies of your data are stored, each in a different Availability Zone (AZ) within the region.
- It can be accessed via the AWS Console, the AWS CLI, or Python (boto3) — this document covers the last two.

---

## 1. Launch the EC2 instance

If you don't already have one, launch a new **Ubuntu** EC2 instance from the AWS Console (or CLI):

- AMI: Ubuntu Server 24.04 LTS
- Instance type: t2.micro (free tier is fine)
- Name: `techxxx-firstname-s3-boto3-task`
- Security group: allow SSH (port 22) from your IP

Connect to it:

```bash
ssh -i your-key.pem ubuntu@<EC2-PUBLIC-IP>
```

---

## 2. Install dependencies for AWS CLI

On the EC2 instance, first update and upgrade the system before installing anything:

```bash
sudo apt update -y      # updates the package list
sudo apt upgrade -y     # installs the latest versions of software already on the system
```

Install `unzip`, which is needed to extract the AWS CLI installer:

```bash
sudo apt install unzip -y
```

Install AWS CLI v2:

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

> Expected output: `You can now run: /usr/local/bin/aws --version`

Check the version is correct:

```bash
aws --version
```

> Expected output (version numbers will vary): `aws-cli/2.35.22 Python/3.14.6 Linux/6.17.0-1017-aws exe/x86_64.ubuntu.24`

Install Python and boto3 for the Python scripts:

```bash
sudo apt install -y python3 python3-pip
pip3 install boto3
```

---

## 3. Authenticate using AWS CLI

This step gives the CLI (and boto3) your credentials so you can run commands as yourself, without going through the AWS Console.

Run:

```bash
aws configure
```

You'll be prompted for:

1. **AWS Access Key ID** — from an IAM user with S3 permissions
2. **AWS Secret Access Key**
3. **Default region name** — e.g. `eu-west-1`
4. **Default output format** — `json`

This writes credentials to `~/.aws/credentials` and config to `~/.aws/config`. boto3 automatically picks these up, which is why the Python scripts below don't need any credentials in the code.

Once done, run `clear` to wipe the terminal so the credentials you just typed aren't left sitting on screen.

Check it works:

```bash
aws s3 ls
```

> Expected output: a list of your existing buckets (or nothing, if you have none yet)

Other useful reference commands:

```bash
aws help          # general AWS CLI help (press q to exit)
aws s3 help       # S3-specific help
aws s3 mb help    # help for a specific subcommand, e.g. "mb" (make bucket)
```

---

## 4. Manipulating S3 with the AWS CLI

Step-by-step walkthrough of creating a bucket, uploading a file, downloading it back, and cleaning up — this mirrors what the Python scripts do further down.

**Create a bucket:**

```bash
aws s3 mb s3://techxxx-firstname-test-boto3
```

**Check it exists:**

```bash
aws s3 ls
```

> Expected output: your new bucket listed alongside any others, e.g. `2026-07-14 11:21:00 techxxx-firstname-test-boto3`

**Look inside it** (empty right after creation, so this returns no output):

```bash
aws s3 ls s3://techxxx-firstname-test-boto3
```

**Create and upload a test file:**

```bash
echo "This is a test file" > test.txt
cat test.txt          # check the contents
aws s3 cp test.txt s3://techxxx-firstname-test-boto3
```

**Check it uploaded:**

```bash
aws s3 ls s3://techxxx-firstname-test-boto3
```

> Expected output: `2026-07-14 11:32:52   38 test.txt`

**Download / retrieve a file back from the bucket:**

```bash
mkdir downloads
cd downloads
aws s3 sync s3://techxxx-firstname-test-boto3 .
ls -l
cd ..
```

**Delete a single file from the bucket:**

```bash
aws s3 rm s3://techxxx-firstname-test-boto3/test.txt
```

> ⚠️ This deletes the file immediately with no confirmation prompt.

**Delete the bucket itself:**

```bash
aws s3 rb s3://techxxx-firstname-test-boto3
```

If the bucket still has files in it, this will fail — `aws s3 rb help` shows you need `--force` to delete a non-empty bucket in one go.

---

## 🤯 Dangerous commands 🤯

These delete things immediately, with no confirmation prompt and no undo:

```bash
# Deletes every object in the bucket at once
aws s3 rm s3://techxxx-firstname-test-boto3 --recursive

# Deletes the bucket itself, even if it still has files in it
aws s3 rb s3://techxxx-firstname-test-boto3 --force
```

Double-check the bucket name before running either of these.

---

## 4a. (Optional) Making files in your bucket publicly accessible

By default, every S3 bucket and object is private. If you need to make something public (e.g. to host static website assets), there are two routes:

- **Through the console**: select the object → Actions → Make public (this only works if the bucket's "Block Public Access" settings allow it).
- **Through the CLI**: set a bucket policy or object ACL, e.g. `aws s3api put-object-acl --bucket <bucket> --key <file> --acl public-read`.

This isn't required for this task's DoD, but it's worth knowing it exists.

---

## 5. Python boto3 scripts

Six separate, deliberately minimal scripts (no error handling) live in this folder:

| Script | What it does |
|---|---|
| `list_buckets.py` | Lists all S3 buckets in the account |
| `create_bucket.py` | Creates a new bucket |
| `upload_file.py` | Uploads a local file to the bucket |
| `download_file.py` | Downloads the file back from the bucket |
| `delete_file.py` | Deletes the file from the bucket |
| `delete_bucket.py` | Deletes the (now-empty) bucket |

Run them in this order on the EC2 instance:

```bash
python3 list_buckets.py
python3 create_bucket.py
python3 upload_file.py
python3 download_file.py
python3 delete_file.py
python3 delete_bucket.py
```

Before running, update the `BUCKET_NAME` variable at the top of `create_bucket.py` (and match it in the other scripts) to something like `techxxx-firstname-test-boto3` — bucket names must be globally unique across all of AWS, so pick something that includes your name.

### How the scripts work

All of them use `boto3.client("s3")`, which is boto3's low-level S3 client — it maps almost one-to-one onto the AWS S3 API calls.

- `boto3.client("s3")` reads credentials automatically from `~/.aws/credentials` (set up by `aws configure`), so no keys appear in the code.
- `list_buckets()` returns a dict; the buckets are under `["Buckets"]`, each with a `["Name"]`.
- `create_bucket()` needs a `LocationConstraint` if your region isn't `us-east-1` — the script includes this.
- `upload_file(local_path, bucket, key)` and `download_file(bucket, key, local_path)` handle the file transfer for you (streaming under the hood).
- `delete_object(Bucket=..., Key=...)` removes a single file (object).
- `delete_bucket(Bucket=...)` removes the bucket itself — this only works once it's empty.

## 7. Definition of Done Checklist

### EC2 and Dependencies

- [ ] An existing Ubuntu EC2 instance was used or a new instance was launched.
- [ ] The instance was named appropriately.
- [ ] AWS CLI version 2 was installed.
- [ ] Python 3 was installed.
- [ ] A Python virtual environment was created.
- [ ] Boto3 was installed.

### Authentication

- [ ] AWS credentials were configured using `aws configure`.
- [ ] Authentication was tested using `aws sts get-caller-identity`.
- [ ] S3 access was tested using `aws s3 ls`.
- [ ] No credentials were included in the scripts or GitHub repository.

### AWS CLI Operations

- [ ] Listed the S3 buckets.
- [ ] Created an S3 bucket.
- [ ] Uploaded a file.
- [ ] Downloaded the file.
- [ ] Deleted the file.
- [ ] Deleted the bucket.

### Python Boto3 Scripts

- [ ] Created a script to list buckets.
- [ ] Created a script to create a bucket.
- [ ] Created a script to upload a file.
- [ ] Created a script to download a file.
- [ ] Created a script to delete a file.
- [ ] Created a script to delete the bucket.
- [ ] Tested each script successfully.
- [ ] Can explain what each line of code does.

### Delivery

- [ ] All scripts were committed and pushed to GitHub.
- [ ] The repository contains no AWS access keys or secret keys.
- [ ] A link to the working scripts is included below.

---

## 8. Scripts Folder

The completed Python scripts are available here:

```text
<INSERT-GITHUB-REPOSITORY-LINK>
```

The repository should contain:

- the six separate Python scripts
- `test.txt`
- `requirements.txt`
- a README explaining how to run the project