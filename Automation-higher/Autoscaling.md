# Auto Scaling (High Availability)

## Overview

This documentation covers the process of autoscaling: creating an **Application AMI**, **Launch Template**, **Application Load Balancer** and **Auto Scaling Group** in AWS.

The purpose is to create a highly available application that can:

- distribute incoming traffic across multiple EC2 instances
- automatically replace unhealthy instances
- scale when required
- reduce manual intervention

---

## Why do we automate?

As we move through the deployment process, we gradually increase the level of automation.

Automation is useful because it can:

- reduce repetitive BAU (Business As Usual) tasks
- improve efficiency
- save time
- reduce human error
- improve consistency across deployments
- reduce long-term operational costs

---

## When should we automate?

Automation is worth considering when:

- a task is performed regularly
- it would save time for a team or organisation
- it is more cost-effective than performing the task manually
- the effort required to automate is justified

Before automating something, think:

> **"Is automating this task actually worth it?"**

---

## Virtualised vs Containerised Deployment

For this project we are using **virtualised deployment**.

This means our application runs on EC2 virtual machines, with each instance having its own operating system.

**Containerised deployment** works **differently**. Rather than creating an entire virtual machine, the application runs inside lightweight containers that share the host operating system.

Containerisation is generally faster and uses fewer resources, but for this project we are focusing on virtual machines.

---

## Architecture

The architecture consists of:

- an **Application Load Balancer**
- an **Auto Scaling Group**
- multiple EC2 application instances created from the same Application AMI

Unlike our previous deployment, users no longer connect directly to an EC2 instance.

Instead, all traffic first reaches the **Load Balancer**, which then decides which healthy instance should receive the request.

---

## Why create an Application AMI?

Earlier in the project, our application relied on a large User Data script to:

- install Node.js
- clone the Git repository
- install dependencies
- start PM2
- launch the application

While this worked, every new EC2 instance had to repeat the same setup process.

For Auto Scaling, this isn't ideal.

Instead, we create an **Application AMI**, which is a snapshot of our fully configured application server.

New EC2 instances can then be launched from this image, meaning they already contain:

- the application
- Node.js
- PM2
- installed dependencies

This significantly reduces the time needed to launch replacement instances.

---

# Creating the Launch Template

The Launch Template tells AWS how new EC2 instances should be created.

### Step 1 - Create the Launch Template

1. Go to the **EC2 Dashboard**.
2. Select **Launch Templates**.
3. Click **Create launch template**.
4. Enter a suitable name.

Example:

```
tech610-maria-ttt-app-asg-lt
```

5. Under **Application and OS Images (Amazon Machine Image)**, select your **Application AMI**.

6. Choose your normal security group.

This should allow:

- HTTP (80)
- SSH (22)

Port 3000 can also be allowed if required.

---

### Step 2 - Add User Data

Under **Advanced details**, add the following User Data script.

```bash
#!/bin/bash

cd /tech610-tic-tac-toe/app
pm2 start index.js --name tic
```

Because the AMI already contains everything the application needs, this script simply starts the application.

Click **Create launch template**.

---

### Step 3 - Test the Launch Template

Before creating the Auto Scaling Group, test that the Launch Template works correctly.

1. Select the Launch Template.
2. Click **Actions**.
3. Select **Launch instance from template**.
4. Launch the instance.

Once the instance has finished starting:

- copy the Public IP
- open it in your browser
- check that the Tic Tac Toe application loads successfully

> **Expected outcome**
>
> The application should be running exactly as it did before creating the AMI.
![Tictactoe app running with app AMI](Images/ttt-running-with-app-ami.png)

### Before moving on...

Only continue once you've confirmed that the application is working.

Testing each stage before building on top of it makes troubleshooting much easier if something goes wrong later.

---

# Creating the Auto Scaling Group

Once you've confirmed that the Launch Template is working correctly, the next step is to create the Auto Scaling Group.

### Step 1 - Create the Auto Scaling Group

1. Go to **Launch Templates**.
2. Select the Launch Template created earlier.
3. Click **Actions**.
4. Select **Create Auto Scaling Group**.
5. Give the Auto Scaling Group a meaningful name.

Example:

```
tech610-maria-ttt-app-asg
```

6. Click **Next**.

---

### Step 2 - Configure the network

Choose the default **VPC**.

For **Availability Zones and subnets**, select **all available subnets**.

#### Why?

Selecting all subnets allows AWS to spread EC2 instances across multiple Availability Zones.

This improves availability because if one Availability Zone experiences an issue, instances in the remaining zones can continue serving traffic.

Leave the balancing option as:

- **Balance Best Effort**

Click **Next**.

---

## Creating the Load Balancer

The Load Balancer becomes the single entry point into the application.

Instead of users connecting directly to an EC2 instance, all traffic first passes through the Load Balancer, which then forwards requests to healthy instances.

### Step 1 - Configure the Load Balancer

1. Select **Attach to a new load balancer**.
2. Choose **Application Load Balancer**.
3. Rename the Load Balancer if required.

Example:

```
tech610-maria-ttt-app-lb
```

Adding **-lb** to the name makes it easier to identify later.

4. Set the scheme to:

- **Internet-facing**

5. Confirm the listener is using:

- HTTP
- Port **80**

---

## Creating the Target Group

A Target Group is required so the Load Balancer knows where traffic should be sent.

### Step 1

Create a new Target Group.

Example:

```
tech610-maria-ttt-app-tg
```

Adding **-tg** to the name makes it easier to identify later.

#### Why do we need a Target Group?

The Target Group keeps track of healthy EC2 instances.

If an instance becomes unhealthy, the Load Balancer automatically stops directing traffic to it and instead sends requests to another healthy instance.

---

## Configuring Health Checks

Health checks allow AWS to monitor whether each EC2 instance is responding correctly.

### Step 1

Enable:

**Elastic Load Balancing health checks**

If an instance repeatedly fails its health checks, the Auto Scaling Group removes it and launches a replacement.

### Step 2

Set the **Health Check Grace Period** to:

```
90 seconds
```

#### Why?

A newly launched EC2 instance needs time to boot and start the application.

The grace period delays the first health check, preventing AWS from marking a healthy instance as unhealthy simply because it hasn't finished starting yet.

Click **Next**.

---

## Configuring Group Size

For this deployment we used the following settings.

| Setting | Value |
|---------|------:|
| Desired capacity | 2 |
| Minimum capacity | 2 |
| Maximum capacity | 3 |

#### What do these values mean?

- **Desired capacity** is the number of instances AWS aims to keep running.
- **Minimum capacity** is the lowest number of instances allowed.
- **Maximum capacity** is the highest number of instances AWS is allowed to launch.

> **Note**
>
> Running additional EC2 instances increases AWS costs, so remember to remove or scale down resources when you've finished.

---

## Configuring Automatic Scaling

To allow AWS to automatically increase or decrease capacity:

1. Select **Target tracking scaling policy**.
2. Set the **Instance warmup** period to:

```
90 seconds
```

#### Why?

The warmup period gives newly launched instances enough time to become fully operational before AWS includes them in scaling decisions.

Click **Next**.

---

## Notifications

AWS allows notifications to be sent using Amazon SNS whenever scaling activities occur.

For this deployment we **did not configure notifications**, so simply click **Next**.

---

## Tags

Before creating the Auto Scaling Group, add a Name tag.

Example:

| Key | Value |
|-----|-------|
| Name | tech610-maria-ttt-app-ha-sc |

#### Why are tags important?

Without tags, every EC2 instance launched by the Auto Scaling Group will have a randomly generated name.

Adding a Name tag makes resources much easier to identify when managing multiple instances.

Click **Next**.

Review the configuration.

Click **Create Auto Scaling Group**.

---

# Testing the Auto Scaling Group

Once the Auto Scaling Group has finished creating, confirm that everything has been configured correctly.

### Step 1

Open your Auto Scaling Group.

### Step 2

Select the **Integrations** tab.

### Step 3

Open the linked **Load Balancer**.

### Step 4

Locate the **DNS name**.

Copy the DNS name and paste it into your browser.

> **Expected outcome**
>
> The Tic Tac Toe application should load successfully.
![Tictactoe app running from the load balance](Images/ttt-running-load-balance.png)
---

## Why use the DNS name?

The Load Balancer is now the **front door** to the application.

Users should no longer access the application using the Public IP address of an EC2 instance.

Instead, all requests should be made through the Load Balancer's DNS name.

---

# Testing High Availability

One of the easiest ways to test the Auto Scaling Group is to terminate one of the running EC2 instances.

### Expected behaviour

The Auto Scaling Group should:

- detect that an instance has been lost
- automatically launch a replacement
- register the new instance with the Target Group
- continue serving traffic through the Load Balancer

This demonstrates **High Availability**, as the application remains available even when an instance fails.

---

# Cleaning Up Resources

To avoid unnecessary AWS charges, delete the resources once testing has finished.

Delete them in the following order:

1. Load Balancer
2. Target Group
3. Auto Scaling Group

---

## Still working?

If you aren't ready to delete everything, another option is to edit the Auto Scaling Group and change:

| Setting | Value |
|---------|------:|
| Minimum capacity | 0 |
| Maximum capacity | 0 |

This stops EC2 instances from running while keeping the Auto Scaling Group configuration.

---

# Types of Scaling

There are three common types of scaling used in AWS.

### Manual Scaling

The number of EC2 instances is increased or decreased manually.

---

### Scheduled Scaling

AWS scales according to a predefined schedule.

For example:

- increase capacity every weekday morning
- reduce capacity overnight

---

### Dynamic Scaling

AWS automatically scales based on CloudWatch metrics such as:

- CPU utilisation
- network traffic
- request count

This deployment uses **Target Tracking Scaling**, which is an example of dynamic scaling.

---

# Reflection

Through this deployment I gained practical experience:

- creating an Application AMI for faster deployments
- creating a Launch Template
- configuring an Application Load Balancer
- creating a Target Group
- configuring Auto Scaling Groups
- using health checks to detect unhealthy instances
- understanding how AWS automatically replaces failed EC2 instances

Overall, this demonstrated how multiple AWS services work together to create a highly available application that can recover automatically from failures while reducing the amount of manual intervention required.