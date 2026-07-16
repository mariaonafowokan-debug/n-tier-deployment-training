# Installing Terraform:

## 1. Find the official site
> `https://developer.hashicorp.com/terraform/install`

## 2. Install the correct version
> `AMD64
> Version: 1.15.8`

## 3. Unzip 
> Open the downloaded zip file and `Extract all`

## 4. Rename path 
> e.g. `C:\Users\maria\Terraform` and save

## 5. Check the Terraform version
 In terminal e.g. bash, check for the terraform version using the correct path:
```bash
/c/Users/maria/Terraform/terraform.exe --version
```
**Expected output:**
> /c/Users/maria/Terraform/terraform.exe --version
> Terraform v1.15.8
> on windows_amd64


## 6. Edit your environment variables 
This is so that you can access Terraform from anywhere

### Step 1
* Press the Windows key and type **environment variables**

### Step 2
*  Click **Edit the system environment variables**.

### Step 3
A window called System Properties will open on the Advanced tab:
 * Click the Environment Variables... button near the bottom.

### Step 4
* In the User variables for maria section:
    * Select Path
    * Click Edit...
    * Click New

### Step 5
Enter:
* C:\Users\maria\Terraform

### Step 6
* Click OK on all the windows until they're closed.

### Step 7
* Close Git Bash completely and open a new Git Bash window.

## 7. Check it has worked

Test it by running:
```bash
terraform --version
```
**Expected output:**
[Terraform running on this version:](Images/Terraform-version-running.png)


## 8. Install the official HashiCorp Terraform extension in VS Code


## Troubleshooting:

### Issue 1- `echo $PATH` does not show the Terraform folder
If you attempt this command right after you check run the command to check which version  of terraform you have (Step 5), and you do not see your path:

`/c/Users/maria/Terraform`

Terraform has not yet been added to your PATH, or your terminal has not refreshed the updated environment variables. Go to step 6. 

#### Resolution:  6. Edit your environment variables 
Confirm that /c/Users/maria/Terraform now appears.


### Issue 2 `terraform: command not found`
#### Error
This is the result of Issue 1. Since the PATH doesn't include the Terraform folder, Git Bash can't find the terraform command.

1. Press Windows + R.

2. Type:
```bash
sysdm.cpl
```
and press Enter.

3. Go to the Advanced tab.

4. Click Environment Variables....

5. Under User variables for maria, click Path → Edit.

6. Close all Git Bash and PowerShell terminals.

7. Close VS Code completely.

8. Reopen VS Code.

9. Open a brand-new Git Bash terminal.
Run:
`terraform --version`

**Expected output:**
```bash
Terraform v1.15.8 on windows_amd64
```