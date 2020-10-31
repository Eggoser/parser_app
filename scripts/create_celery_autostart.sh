#!/bin/bash

sudo touch /etc/default/celeryd
sudo cat celery_example_config > /etc/default/celeryd


sudo adduser celery_user


wget https://raw.githubusercontent.com/celery/celery/3.1/extra/generic-init.d/celeryd
chmod +x celeryd
sudo mv ./celeryd /etc/init.d/


sudo mkdir /var/log/celery
sudo chown celery_user /var/log/celery


sudo sh -x /etc/init.d/celeryd start &


sudo update-rc.d celeryd defaults
sudo service celeryd restart


