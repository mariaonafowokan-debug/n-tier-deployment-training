
# Steps to creating a new repo:
1. Create a new local repository

In Git Bash:

cd ~/Projects
mkdir tech610-terraform
cd tech610-terraform
git init
code .

Replace 610 with your cohort number if your trainer uses a different one.

2. Create a README

In VS Code, create a file called:

README.md

Add something simple like:

# Tech610 Terraform

This repository contains Terraform code created during the Tech610 Infrastructure as Code training.
3. Make the first commit

In Git Bash:

git add .
git commit -m "Initial commit"
4. Create a private GitHub repository

On GitHub:

Click New Repository

Repository name:

tech610-terraform
Set it to Private
Do not add a README (you already created one locally).
Click Create repository.
5. Connect your local repo to GitHub

GitHub will show commands similar to:

git remote add origin https://github.com/<your-username>/tech610-terraform.git
git branch -M main
git push -u origin main