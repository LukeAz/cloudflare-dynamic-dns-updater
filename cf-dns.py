from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import json

chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")

auth_email = ""
auth_password = ""
auth_key = ""
zone_identifier = ""
zone_name = ""
record_name = ""
proxy = True
ttl = 1
type = "AAAA" #ipv6 domain [for ipv4 use "AA"]

currentip = requests.get('https://ipv6.icanhazip.com/' if type == "AAAA" else 'https://ipv4.icanhazip.com/').text.strip()
namedns = requests.get('https://api.cloudflare.com/client/v4/zones/{}/dns_records?name={}'.format(zone_identifier, record_name), headers = {
  "X-Auth-Email": auth_email,
  "Authorization": "Bearer " + auth_key,
  "Content-Type": "application/json"
}).json()

if namedns['result'][0]['content'] != currentip:
  print('[DNS] change in progress')

  driver = webdriver.Chrome(options=chrome_options)
  driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': """
      Object.defineProperty(navigator, 'webdriver', {
        get: () => false,
      });
    """
  })
  driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'})

  try:
    driver.get('https://dash.cloudflare.com/login?lang=it-it')
    email = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.XPATH, """//input[@data-testid="login-input-email"]"""))
    )
    email.send_keys(auth_email)
    driver.find_element(By.XPATH,"""//input[@data-testid="login-input-password"]""").send_keys(auth_password)
    driver.find_element(By.XPATH,"""//button[@data-testid="login-submit-button"]""").click()
    time.sleep(5);

    payload = {
      "content": currentip,
      "data":{},
      "name": record_name,
      "proxiable": proxy,
      "proxied": proxy,
      "ttl": ttl,
      "type": type,
      "zone_id": zone_identifier,
      "zone_name": zone_name,
      "id": namedns['result'][0]['id']
    }
    url = "https://dash.cloudflare.com/api/v4/zones/{}/dns_records/{}".format(zone_identifier, namedns['result'][0]['id'])
    script = """
        xhr = new XMLHttpRequest();
        xhr.open('PUT', "{}", false);
        xhr.setRequestHeader("accept", "*/*");
        xhr.setRequestHeader("accept-encoding", "gzip, deflate, br");
        xhr.setRequestHeader("accept-language", "en-US,en;q=0.9");
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.setRequestHeader("origin", "https://dash.cloudflare.com");
        xhr.setRequestHeader("referer", "https://dash.cloudflare.com");
        xhr.setRequestHeader("sec-fetch-dest", "empty");
        xhr.setRequestHeader("sec-fetch-mode", "cors");
        xhr.setRequestHeader("sec-fetch-site", "same-origin");
        xhr.setRequestHeader("sec-gpc", "1");
        xhr.setRequestHeader("x-atok", window.bootstrap.atok);
        xhr.setRequestHeader("x-cross-site-security", "dash");
        xhr.send(JSON.stringify({}));
        return JSON.parse(xhr.responseText);
    """.format(url, json.dumps(payload))

    put = driver.execute_script(script);
    if put["result"]["content"] == currentip:
      print("[DNS] success change: ", currentip)
    else:
      print("[DNS] failed change: ", put["result"]["content"])

  except Exception as e:
    print("[DNS] failed change, error: ", e)
  finally:
    driver.close()
else:
  print('[DNS] no change: {}'.format(namedns['result'][0]['content']))
