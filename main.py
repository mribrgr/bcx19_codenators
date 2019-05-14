from network import WLAN
import urequests as requests
import machine
import time
import pycom
import pycom           # we need this module to control the LED

pycom.heartbeat(False) # disable the blue blinking
pycom.rgbled(0x0000ff) # make the LED light up red in colour

# Your WiFi network credentials
WIFI_SSID = 'BCX19'
WIFI_KEY = ''

# local apache address
APACHE_ADDRESS = '192.168.43.14'

DEVICE_SECRET_KEY = 'd_sk_NBHcRbvRYwEiZpK63bp52SJH' # pysense
#DEVICE_SECRET_KEY = 'd_sk_7jbbGidquAFyOsPyhjh4O9B9' # pytrack

# Delay between each event
DELAY = 1

wlan = WLAN(mode=WLAN.STA)
nets = wlan.scan()

# Connect to the WiFi network
for net in nets:
    if net.ssid == WIFI_SSID:
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, WIFI_KEY), timeout=5000)
        print('Connecting...')
        while not wlan.isconnected():
             machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        break

def post_event_fab(name, data):
    try:
        #pycom.rgbled(0x00ff00)
        url = "http://" + APACHE_ADDRESS
        headers = {"Content-Type": "application/json"}
        json_data = {"name": name, "data": data}
        if json_data is not None:
            req = requests.post(url=url, headers=headers, json=json_data)
            if req.status_code is not 200:
                print("Status code is not 200")
                machine.reset()
            else:
                pycom.rgbled(0x00ff00)
                if DELAY > 1:
                    time.sleep(1)
                else:
                    time.sleep(0)
                print('Data send to fab')
                pycom.rgbled(0x0000ff)
            #return req.json()
            #print(req.status_code)
        else:
            print('JSON Data is None')
            pass
    except:
       #pycom.rgbled(0xff0000) # make the LED light up red in colour
       raise

while True:
    name = 'message'
    content = 'content'
    post_event_fab(name, content)
    if not wlan.isconnected():
         print("Not connected to WiFi")
    time.sleep(DELAY)
    machine.idle()
