import requests
import time
import random

BASE_URL = 'https://wearables-rest.appspot.com'
EMAIL = 'test@test.com'
PASSWORD = 'password'

print('Starting sim...')

# Log in
r = requests.post(BASE_URL + '/users/login/', data={'email': EMAIL, 'password': PASSWORD})
res = r.json()
print(res['message'])
token = res['token']

# get the list of device IDs that the user owns
r = requests.get(BASE_URL + '/devices', params={'type': 'owner'}, headers={'Authorization': 'Bearer ' + token})
device_response = r.json()['devices']
devices = [dev['_id'] for dev in device_response]
print(devices)

# Keep track of whatever we last posted so we can base future data off it
last_payload = {devid:{'temp':0, 'humidity': 0} for devid in devices}

# Post until user quits the program
while True:
    for device in devices:
        # generate some random numbers for each device and post it
        temp = random.uniform(-2, 2) + last_payload[device]['temp']
        last_payload[device]['temp'] = temp
        humidity = random.uniform(-2, 2) + last_payload[device]['humidity']
        last_payload[device]['humidity'] = humidity

        payload = {'temp': {'value': temp, 'units': 'F'}, 'humidity': {'value': humidity, 'units': 'g/m3'}}
        print(f'Setting temp: {temp}, humidity: {humidity} for device {device}')
        r = requests.post(
            BASE_URL + '/devices/' + device, json={'payload': payload}, headers={'Authorization': 'Bearer ' + token})
        print(r.json()['message'])
    time.sleep(random.uniform(2, 5))