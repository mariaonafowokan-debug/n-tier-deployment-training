#!/bin/bash
sudo apt update
sudo apt-get install apache2-utils
ab
ab -n 1000 -c 100 http://PUBLIC_INSTANCE_IP/