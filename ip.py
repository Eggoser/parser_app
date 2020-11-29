#!/usr/local/bin/python3

import requests

myip = requests.get("https://api.ipify.org").text

print(myip)