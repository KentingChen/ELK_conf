#!/bin/sh

## YUM 
# Basic
yum -y install nc
yum -y install curl
yum -y install wget

# For Pythons
yum -y install python-pip
pip install --upgrade pip
pip install elasticsearch


# Settings
timedatectl set-timezone "Asia/Taipei"
hwclock -w
