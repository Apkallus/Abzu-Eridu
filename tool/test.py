#!/bin/python
import urllib.request
import os

host = 'http://challenge.localhost:80'
path = '/pwn'
target_url = host + path
req = urllib.request.Request(target_url)
req.add_header('User-Agent', 'Firefox')

response_data = urllib.request.urlopen(req)
request_body = response_data.read().decode('utf-8')

print(response_data)
print(request_body)
