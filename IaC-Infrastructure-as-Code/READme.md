## Overview

This guide introduces **Infrastructure as Code (IaC)**, the problems it
solves, its benefits, and the tools commonly used to automate
infrastructure provisioning and software configuration. It also
introduces **Terraform**, one of the most widely used Infrastructure as
Code tools.

------------------------------------------------------------------------

## Table of Contents

- [What Problem Does IaC Solve?](#what-problem-does-iac-solve)
- [What Have We Automated So Far?](#what-have-we-automated-so-far)
- [What is Infrastructure as Code?](#what-is-infrastructure-as-code)
- [Declarative vs Imperative](#declarative-vs-imperative)
  - [Declarative](#declarative)
    - [Restaurant Analogy](#restaurant-analogy)
  - [Imperative](#imperative)
- [Benefits of IaC](#benefits-of-iac)
- [When Should IaC Be Used?](#when-should-iac-be-used)
- [Infrastructure Provisioning vs Configuration Management](#infrastructure-provisioning-vs-configuration-management)
  - [Infrastructure Provisioning](#infrastructure-provisioning)
  - [Configuration Management](#configuration-management)
- [Common IaC Tools](#common-iac-tools)
  - [Configuration Management](#configuration-management-1)
  - [Infrastructure Provisioning](#infrastructure-provisioning-1)
    - [Cloud-Agnostic](#cloud-agnostic)
    - [Cloud-Specific](#cloud-specific)
- [Why Terraform?](#why-terraform)
- [Reflection](#reflection)

------------------------------------------------------------------------

# What Problem Does IaC Solve?

Traditionally, cloud infrastructure has been created manually through
the AWS Management Console.

Examples include:

-   Launching EC2 instances
-   Creating VPCs
-   Creating Subnets
-   Configuring Security Groups
-   Setting up networking

Although we have automated software installation, creating the
infrastructure itself is still largely manual.

Manual provisioning is:

-   Time-consuming
-   Repetitive
-   Prone to human error
-   Difficult to reproduce consistently

Infrastructure as Code (IaC) automates this process by allowing
infrastructure to be created from code.

------------------------------------------------------------------------

# What Have We Automated So Far?

  -----------------------------------------------------------------------
  Task                          Automated?          How?
  --------------------- --------------------------- ---------------------
  Create Virtual                    **No**            Launch Templates help
  Machines                                          automate VM creation,
                                                    but they are still
                                                    launched manually.

  Create Infrastructure            **No**          VPCs, Security Groups
                                                    and networking are
                                                    still created
                                                    manually.

  Configure Software              **Yes**            Using Bash scripts,
                                                    User Data and AMIs.
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# What is Infrastructure as Code?

Infrastructure as Code (IaC) is the practice of managing and
provisioning infrastructure using machine-readable configuration files
instead of manually creating resources.

Infrastructure includes resources such as:

-   EC2 instances
-   VPCs
-   Subnets
-   Security Groups
-   Route Tables
-   Load Balancers
-   Auto Scaling Groups

> **Note:** Infrastructure refers to the cloud resources applications
> run on, not the software installed on them.

------------------------------------------------------------------------

# Declarative vs Imperative

## Declarative

You describe **what** you want, and the IaC tool determines **how** to
build it.

Example:

> Create two EC2 instances behind a Load Balancer.

Terraform works out the order automatically.

### Restaurant Analogy

Even if you order:

1.  Dessert
2.  Starter
3.  Main

the kitchen still serves the courses in the correct order. Declarative
tools work the same way.

## Imperative

You describe every step required.

Example:

1.  Create a VPC
2.  Create a Subnet
3.  Create a Security Group
4.  Launch an EC2 instance
5.  Attach the Security Group

------------------------------------------------------------------------

# Benefits of IaC

-   Faster deployments
-   Consistent environments
-   Reduced human error
-   Version control with Git
-   Easier collaboration
-   Easier auditing
-   Simpler scaling

------------------------------------------------------------------------

# When Should IaC Be Used?

IaC is useful when:

-   infrastructure is deployed frequently
-   environments must remain consistent
-   teams collaborate
-   deployments need to be repeatable
-   infrastructure needs to scale

------------------------------------------------------------------------

# Infrastructure Provisioning vs Configuration Management

## Infrastructure Provisioning

Creates cloud infrastructure such as:

-   EC2
-   VPCs
-   Subnets
-   Security Groups
-   Load Balancers

## Configuration Management

Configures software after infrastructure exists.

Examples:

-   Installing software
-   Updating packages
-   Editing configuration files
-   Starting services
-   Deploying applications

------------------------------------------------------------------------

# Common IaC Tools

## Configuration Management

-   Ansible
-   Puppet
-   Chef

## Infrastructure Provisioning

### Cloud-Agnostic

-   Terraform

### Cloud-Specific

**AWS**

-   CloudFormation

**Microsoft Azure**

-   ARM Templates
-   Bicep

------------------------------------------------------------------------

# Why Terraform?

Terraform is a cloud-agnostic Infrastructure as Code tool that works
with AWS, Azure, Google Cloud Platform and many other cloud providers.

It uses a **declarative** approach, allowing you to describe the
infrastructure you want while Terraform determines the correct order to
create it.

Terraform can provision:

-   EC2 instances
-   VPCs
-   Subnets
-   Security Groups
-   Route Tables
-   Load Balancers
-   Auto Scaling Groups
-   Databases
-   Storage

Because everything is stored as code, infrastructure can be version
controlled, shared with a team, reused and recreated quickly.

------------------------------------------------------------------------

# Reflection

This lesson helped me understand the difference between provisioning
infrastructure and configuring software. I also learned how
Infrastructure as Code improves consistency, reduces manual work and
makes cloud deployments easier to automate.