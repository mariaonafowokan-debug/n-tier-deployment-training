
The further we go, the higher the leveel of automation

Why do we automate?
* For BAU tasks to keep things running with minimal interference
* Efficiency, make things more time efficient
* Cost-effectiveness

When should we automate?
* If automating something would be more cost effective
* If automating would save time for a team, organisation

What should we consider?
- Is automating this thing going to be worth it?  






# Virtualised deployment vs Containerised deployment 
We are using...


## Architecture for an aws autoscaling group
[image]

The reason that the app image is reliable is because it gets the app running in seconds as opposed to going stage by stage with many instances
You won't need the big user data in the image, just a small one

### Onto creating our launch image for autoscaling:
1. Go to launch instances

2. Create your launch template for the app and name it

3. Use your AMI image as the OS

3. Select your usual security type that allows HTTP and SSH, can allow port 3000


4. Then in advanced settings include this into user to get the right location (**really important!!**): 

```bash
 #!/bin/bash

cd /tech610-tic-tac-toe/app
pm2 start index.js --name tic
```

### Note: 
You **MUST** check and test things along the way
1. Go to actions tab

2. Select launch instance from template
Check everything is in the right place!

3. Click launch instance

4. Expand the instance link

4. Copy the public ip address and open it 

### Now the ttt app with just user data is working!!


### Note we did not name it, as autoscaling will name it for us 


Go to Launch template
1. Select your template from earlier (...asg....-lt)

1. Actions 

1. Create autoscaling group

1. Name it e.g. `tech610-maria-ttt-app-asg`
1. Choose instance launch options 


**click next**

1. Use default vpc

1. Availability zones and subnet: in the availability vpc there's an a, b, and  subnet:
- Select ALL subnets: *This is so you can spread out your vms across all those availability zones in the region*

1. Leave it on balance best effort (so if it fails in one zone it will try in a healthier zone)

1. Leave on default *(?)*

1. We want our own load balance "attach to a new load balance"
-*for replicating it, you can search for your load balance from last time.* 

1. Load balancer type: you want application load balancer

1. On the end of the 'Load balancer name'
- change the end part to '-lb' instead of '1' so you know it's a a load balance associated with that group

1. Load balancer scheme must be internet facing because people are coming on from the internet

1. Default port for http is port 80, so make sure it says this

1. Beside port 80, the tab to the right will say `Default routing (forward to)`
- create a target group
- it will name this automatically, so you should see something similar to your title there: 
e.g. `tech610-maria-ttt-app-asg-lb`
This is so the load balance knows the healthy instances in the target group and can target them instead of any unhealthy ones

1. For additional health check, tic: `Turn on Elastic Load Balancing health checks`
- this gets rid of any unhealthy instances and removes, then replaces the unhealthy ones 

1. Health check grace period
- This time period delays the first health check until your instances finish initializing
It will try a few times until it gets status 200 code
We don't want it to start checking as soon as we boot up the machine because we need to make sure the app is running 
- We can give it 90 seconds (but you must know your application, roughly how long it takes to boot up and decide based on that)

## Group size
1. For desired capacity, select 2 
1. Minimum will be 2, maximum will be 3 
### Note: keep in mind that these cost moneyb so when your working in devOps and doing testing, be mindful of how many you use

-We want it to scale dynamically so we want a scaling policy 

1. For `Automatic scaling` select: Target tracking scaliing policy
1. For `Instance warmup`: Specify the number of second you want it to take until you want the metrics of that app to be included, so how long do you want the INSTANCE to take until it scales: `90 seconds`

1. For instance maintenance policy: 
Choose a replacement behavior depending on your availability requirements
- We  want `Mixed behaviour`:
`No policy`

**Next:**

-  We didnt choose a notification

**Next:**


Tags: if we do not give a tab then all the instances you create will not have a nametag... chaotic!

1. Put name in left tab and for value, put the name you can recognise e.g. `tech610-maria-ttt-app-asg-lb-HA-SC`

1. Click next, review details
Click CREATE AUTOSCALING GROUP

1. Scroll down and find yours 


## Post autoscaling launch

Note: There should be 1 front door into your system and this should be the load balancer
- You can go to the public ip of your autoscaling group
*You can familiarise yourself with the tabs*

### Next: 
1. Click integrations
1. You'll see load balancer target group
1. Open link to `Load balancer`
1. Find `DNS name` in the row beneath `Details`
1. Copy the name that you see in the form of a link
1. Paste- and your app should be running

### Last step
How to delete autoscaling group so that it stops running:


Delete load balancer
Delete target group
Delete Autoscaling groups




At the end of the day, you need to delete your atuoscaling group. 
If you don't want to delete because you are still working- edit the minimum and maximum in your autoscaling group to zero.




1. If you terminate one, it notices and gets another one running for you. 
### Troubleshooting 
1. `Cannot be detected`,`Tags`
This would mean there's an issue with the tag, so go back to the part where you had to out 'Name'.


You had an app vm originally using bash script, user, data, then we created an app ami from this 

Types of scaling


