#!/bin/bash

chmod +x install_packages.sh
sudo ./install_packages.sh

sudo mkdir /var/www
sudo mkdir /var/www/parser_app

sudo cp ../app /var/www/parser_app/app
sudo cp ../venv /var/www/parser_app/venv
sudo cp ../configuration.ini /var/www/parser_app/configuration.ini
sudo cp ../parser_app.wsgi /var/www/parser_app/parser_app.wsgi


chmod +x create_celery_autostart.sh
sudo ./create_celery_autostart.sh
