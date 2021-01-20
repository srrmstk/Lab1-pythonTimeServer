import requests
import json

url = 'http://127.0.0.1:8000'
print('Task 1:')
print('GET /:', requests.get(url).text)

print('\nTask 2:')
print('GET /America/Chicago:', requests.get(url + '/America/Chicago').text)

print('GET /<wrong argument>:', requests.get(url + '/gusli').text)

print('\nTask 3:')
input_data = {'type' : 'time', 'tz' : 'Europe/Moscow'}
print('POST /time/Europe/Moscow:', requests.post(url, json.dumps(input_data)).text)
input_data = {'type' : 'time'}
print('POST /time:', requests.post(url, json.dumps(input_data)).text)

print('\nTask 4:')
input_data = {'type' : 'date', 'tz' : 'Pacific/Midway'}
print('POST /date/Pacific/Midway:', requests.post(url, json.dumps(input_data)).text)
input_data = {'type' : 'date'}
print('POST /date:', requests.post(url, json.dumps(input_data)).text)

print('\nTask 5:')
input_data = {
    'type' : 'datediff', 
    'start' : {'date' : '12.20.2021 12:30:00', 'tz' : 'Europe/Moscow'},
    'end' : {'date' : '12.22.2021 22:21:05', 'tz' : 'America/Chicago'}
    }
print('POST /datediff w/ start and end:', requests.post(url,json.dumps(input_data)).text)

input_data = {
    'type' : 'datediff', 
    'start' : {'date' : '12.22.2021 22:21:05', 'tz' : 'America/Chicago'},
    'end' : {'date' : '12:30pm 2021-12-20', 'tz' : 'Europe/Moscow'}
    }
print('POST /datediff reversed:', requests.post(url, json.dumps(input_data)).text)

input_data = {
    'type' : 'datediff', 
    'start' : {'date' : '12.20.2021 22:21:05'},
    'end' : {'date' : '12:30pm 2021-12-01', 'tz' : 'Pacific/Midway'}
    }
print('POST /datediff w/o one tz:', requests.post(url, json.dumps(input_data)).text)

input_data = {
    'type' : 'datediff', 
    'start' : {'date' : '12.20.2021 22:21:05'},
    'end' : {'date' : '12:30pm 2020-12-01'}
    }
print('POST /datediff w/o tz at all:', requests.post(url, json.dumps(input_data)).text)