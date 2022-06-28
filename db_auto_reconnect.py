import requests
from time import sleep

while True:
    response = requests.get('http://localhost:5000/keep_database/')
    print(response.text)
    sleep(10)
