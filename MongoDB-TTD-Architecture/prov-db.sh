#!/bin/bash
 
## TESTED: 6/7/2026
## TESTED BY: Maria
## TESTED ON: AWS
## AIM: Work as a script + user data on fresh Ubuntu 24.04 LTS VM
## PURPOSE: Provision the MongoDB 8.2.5 for TTT app
 
echo update the sources list...
sudo apt-get update -y
echo Done!
 
echo upgrade any packages available...
sudo apt-get upgrade -y
echo Done!

#sudo apt-get install gnupg curl #for another task you might need this but for this task, therse are already baked in

curl -fsSL https://pgp.mongodb.com/server-8.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-8.0.gpg \
   --dearmor
echo Done!

echo create list file...
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg ] https://repo.mongodb.org/apt/ubuntu noble/mongodb-org/8.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-8.2.list

echo update the sources list...
sudo apt-get update
echo Done!


echo install MongoDB...
sudo apt-get install -y \
   mongodb-org=8.2.5 \
   mongodb-org-database=8.2.5 \
   mongodb-org-server=8.2.5 \
   mongodb-mongosh \
   mongodb-org-shell=8.2.5 \
   mongodb-org-mongos=8.2.5 \
   mongodb-org-tools=8.2.5 \
   mongodb-org-database-tools-extra=8.2.5
echo Done!

sudo systemctl start mongod #To start
sudo systemctl enable mongod #To sucessfully enable

sudo systemctl is-enabled mongod #To check it is enabled

# sudo systemctl status mongod #Checking the status to be sure