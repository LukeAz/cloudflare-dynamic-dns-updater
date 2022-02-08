![cloudflare](https://github.com/LukeAz/cloudflare-dynamic-dns-updater/blob/main/img/cloudflare.png)
# cloudflare-dynamic-dns-updater
This script allows to update ipv4/ipv6 dns on cloudflare also for free domains (.tk .ml .ga .cf .gq) that normally could not because the api is blocked.  
The dns value will be updated only in case it is different.

## Technologies
Project includes:
* Python
* Selenium webdriver
* Request


## Requirements
* [Python3](https://www.python.org/downloads/)
* Chromium or Chrome
* [Chromedriver](https://chromedriver.chromium.org/downloads)

## Edit and configure config.json
* auth_email : `account email`
* auth_password : `account password`
* auth_key : `see below`
* zone_identifier: `see below`
* zone_name: `your domain, example: domain.it`
* record_name: `your subdomain, example: subdomain.domain.it`
* proxy: `do you want to use cloudflare proxy?`
* ttl: `if you use the proxy leave the default value`
* type: `"AAAA" for ipv6, "A" for ipv4`

## [Auth Key]
* Go in your profile in your dashboard
* Select “API Tokens”
* Create a new token api
* Select “Edit zone DNS” templates
* In “Permissions” select ZONE -> DNS -> READ
* In “Zone Resources” select INCLUDE -> your zone or all
* If you want you can define a TTL for your token
* Continue to summary
* Create Token
* Copy your token in the config.json file

## [Zone identifier]
* Go in your dashboard and select the correct domain
* In the overview pannel you can found this token

## Installation and start-up instructions
* Install dependencies:
  - pip install selenium requests
* Crontab:
  - crontab -e
  - add */5 * * * * /home/cloudflare/cf-dns.py
  - crontab -l

### Windows
* move chromedriver binary in the same directory
* edit config.json and insert the correct configuration
* python cf-dns.py

### Mac os
* insert chromedriver binary path on the system path
  - sudo nano /etc/paths
  - example: /Users/luca/chromedriver
* edit config.json and insert the correct configuration
* sudo chmod +x cf-dns.py
* ./cf-dns.py

### Linux
* move chromedriver binary in the same directory
* edit config.json and insert the correct configuration
* sudo chmod +x cf-dns.py
* ./cf-dns.py

![arch](https://github.com/LukeAz/cloudflare-dynamic-dns-updater/blob/main/img/arch.png)
## Install chromium and chromdriver on archlinux
* sudo pacman -S chromium

## Chromedriver for ARM64 and other
* Download from assets: https://github.com/electron/electron/releases
