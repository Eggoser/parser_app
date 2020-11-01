#!/bin/bash

pip3 install virtualenv

virtualenv ../venv

source ../venv/bin/activate

pip3 install bs4 requests flask mysql-connector gunicorn


deactivate

