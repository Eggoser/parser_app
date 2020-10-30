#!/bin/bash

chmod +x install_packages.sh
sudo ./install_packages.sh

sudo mkdir /var/www
sudo mkdir /var/www/parser_app

sudo cat parser_app.conf > /etc/apache2/sites-available/parser_app.conf

sudo cp -rf ../app /var/www/parser_app/app
sudo cp -rf ../venv /var/www/parser_app/venv
sudo cp ../configuration.ini /var/www/parser_app/configuration.ini
sudo cp ../parser_app.wsgi /var/www/parser_app/parser_app.wsgi


chmod +x create_celery_autostart.sh
sudo ./create_celery_autostart.sh

sudo service apache2 restart 
