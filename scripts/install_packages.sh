#!/bin/bash

sudo apt-get install redis-server -y

pip3 install virtualenv

virtualenv ../venv

source ../venv/bin/activate

pip3 install eventlet
pip3 install celery
pip3 install bs4 requests flask mysql-connector redis


deactivate

