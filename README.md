![cloudflare](https://github.com/LukeAz/cloudflare-dynamic-dns-updater/blob/main/img/cloudflare.png)
# cloudflare-dynamic-dns-updater
This script allows to update ipv4/ipv6 dns on cloudflare also for free domains (.tk .ml .ga .cf .gq) that normally could not because the api is blocked.  
The dns value will be updated only in case it is different.

## Technologies
Project includes:
* Python
* Selenium webdriver
* Request

## Install and run
* Install python, Chromium, chromedriver (binary file in the same directory)
* pip install selenium requests
* nano cf-dns.py
* python cf-dns.py
* chmod +x cf-dns.py
* crontab -e
* add */5 * * * * /home/cloudflare/cf-dns.py
* crontab -l

## Configure
* nano cf-dns.py
* auth_email : Account email
* auth_password : Account password
* auth_key : API key, see https://www.cloudflare.com/a/account/my-account
* zone_identifier: Zone Id, get it from your account
* zone_name: Zone name, eg: example.com
* record_name: Hostname to update, eg: homeserver.example.com
* proxy: use https cloudflare proxy
* ttl: if you use the proxy leave the default value
* type: "AAAA" for ipv6, "AA" for ipv4

![arch](https://github.com/LukeAz/cloudflare-dynamic-dns-updater/blob/main/img/arch.png)
## Install chromium and chromdriver on archlinux
* sudo pacman -S chromium
* Download from https://chromedriver.chromium.org/downloads

## Chromedriver for ARM64 and other
* Download from assets: https://github.com/electron/electron/releases
