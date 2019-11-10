#!/bin/sh

apt-get update

apt-get install -y python

apt-get install -y python-pip

apt-get install -y mongodb

pip install -r requirements.txt

service mongodb start

nohup python main.py &

nohup python index.py &
