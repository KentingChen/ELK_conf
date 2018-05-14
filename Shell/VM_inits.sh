#!/bin/sh

## YUM 
# Basic
yum install nc
yum install curl
yum install wget

# For Pythons
yum install python-pip
pip install --upgrade pip
pip install elasticsearch


# Settings
timedatectl set-timezone "Asia/Taipei"
hwclock -w
