#!/bin/bash

chmod +x install_packages.sh
./install_packages.sh

sudo mkdir /var/www
sudo mkdir /var/www/parser_app

cp ../app /var/www/parser_app/app
cp ../venv /var/www/parser_app/venv
cp ../configuration.ini /var/www/parser_app/configuration.ini
cp ../parser_app.wsgi /var/www/parser_app/parser_app.wsgi


chmod +x create_celery_autostart.sh
./create_celery_autostart.sh
