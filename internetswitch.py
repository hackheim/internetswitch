from time import sleep
import RPi.GPIO as GPIO
import requests
import datetime
import socket
import fcntl
import struct
from random import randint
from firebase import firebase
firebase = firebase.FirebaseApplication('https://internetswitch-18792.firebaseio.com', None)

input_pin = 20

GPIO.setmode(GPIO.BCM)
GPIO.setup(input_pin, GPIO.IN)
last_input = GPIO.input(input_pin)

def get_ip_address(ifname):
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return_val = socket.inet_ntoa(fcntl.ioctl(
      s.fileno(),
      0x8915,  # SIOCGIFADDR
      struct.pack('256s', ifname[:15])
    )[20:24])
    return str(return_val)
  except Exception as error:
    print "error in get_ip_address:"
    print error
    return 'N/A'

def handle_push(status_string):
  print 'handle push'
  timestamp = datetime.datetime.fromtimestamp(int("1284101485")).strftime('%Y-%m-%d %H:%M:%S')
  r1 = str(randint(100,999))
  r2 = str(randint(100,999))
  gps_payload = '63 25.' + r1 + 'N 10 23.' + r2 + 'E'

  eth0 = get_ip_address('eth0')  # '192.168.0.110'
  wlan0 = get_ip_address('wlan0')  # '192.168.0.110'
  wifi_payload = '123'

  firebase.put('/mobile_alarm_payload', 'unit_216', {'status':status_string, 'gps':gps_payload, 'eth0':eth0, 'wlan0':wlan0})
  print 'payload sent'

print 'pin state of pin ' + str(input_pin) + ' is ' + str(last_input)
#r = requests.put('https://internetswitch-18792.firebaseio.com/alarm', 'status' + str(last_input))
print 'starting loop'
try:
  while True:
    input = GPIO.input(input_pin)
    if input != last_input:
      if input:
        print "Switch disabled"
        handle_push('disabled')
      else:
        print "Switch enabled"
        handle_push('enabled')
    last_input = input
    sleep(0.05)
except Exception as error:
  GPIO.cleanup()
  print 'error:' 
  print error
