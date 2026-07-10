##Troubleshoot app not connecting
* Environment variable - is it set correctly? does it have the right ip address
* DB security group rules?
* Does the app run witthout the database?
* BindIP - set correctly?
* Is the database actually running?

## Extra

### General troubleshooting advice
* Is it a sytemic approach?
* What is the easiest thing to check?
* What is most likely thing it could be?
* Will your approach lead to the root cause of the problem?

### What to expect when launching app VM with user data
How long to expect before app runs? approx. 4 mins

1. An error (not being about to connect)
2. Nginx home/ welcome page (reverse procy has not started working yet)
3. 502 error: Bad gateway (Reverse proxy has started working to redirect traffic from port 80 to port 3000. You get an error because the app that should be running on port 3000 is not running yet)
4. App display (app connects and starts working)
(might want to move things around)


# Virtualised deployment vs Containerised deployment 