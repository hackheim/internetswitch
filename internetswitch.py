from time import sleep
import RPi.GPIO as GPIO
import requests
import datetime
from random import randint
from firebase import firebase
firebase = firebase.FirebaseApplication('https://internetswitch-18792.firebaseio.com', None)

input_pin = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(input_pin, GPIO.IN)
last_input = GPIO.input(input_pin)

def handle_push(status_string):
  print 'handle push'
  timestamp = datetime.datetime.fromtimestamp(int("1284101485")).strftime('%Y-%m-%d %H:%M:%S')
  r1 = str(randint(100,999))
  r2 = str(randint(100,999))
  gps_payload = '63 25.' + r1 + 'N 10 23.' + r2 + 'E'
  firebase.put('/mobile_alarm_payload', 'unit_216', {'status':status_string, 'gps':gps_payload})
  print 'payload sent'

#r = requests.put('https://internetswitch-18792.firebaseio.com/alarm', 'status' + str(last_input))
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
