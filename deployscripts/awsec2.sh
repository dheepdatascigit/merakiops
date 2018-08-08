#!/bin/bash
#
# Create ubuntu 16.04 ec2 instance (t2.micro should be enough)
#
# update and upgrade ubuntu
sudo apt-get -y update
sudo apt-get -y upgrade

# install python pip and virtual environment
sudo apt-get -y install python3-pip
pip3 install virtualenv

sudo apt-get -y install apache2
sudo apt-get -y install libapache2-mod-wsgi-py3

. mkdir -p ~/scripts/python/dev
. cd ~/scripts/python/dev

virtualenv venv_merakiops
source venv_merakiops/bin/activate

git clone https://bitbucket.org/ntw_app_team/merakiops.git
. cd merakiops/deployscripts
pip3 install -r requirements.txt
