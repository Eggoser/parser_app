#!/bin/bash

chmod +x install_packages.sh
sudo ./install_packages.sh


sudo rm -rf /var/www/parser_app
sudo mkdir /var/www
sudo mkdir /var/www/parser_app

sudo cat parser_app.conf > /etc/apache2/conf-available/parser_app.conf

sudo cp -rf ../app /var/www/parser_app/app
sudo cp -rf ../venv /var/www/parser_app/venv
sudo cp ../configuration.ini /var/www/parser_app/configuration.ini
sudo cp ../parser_app.py /var/www/parser_app/parser_app.py
sudo chmod +x /var/www/parser_app/parser_app.py
sudo chmod 755 /var/www/parser_app/

chmod +x create_celery_autostart.sh
sudo ./create_celery_autostart.sh


sudo a2enconf parser_app
sudo a2enmod wsgi

sudo service apache2 restart 
