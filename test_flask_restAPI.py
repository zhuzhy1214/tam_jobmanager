#!/usr/bin/env python
# coding: utf-8

# In[35]:


import requests
import json
import sys

url = 'http://localhost:5000/api'

try:
    response = requests.get(url)
    response_data = response.json()
    print(response_data)

except Exception:
    e = sys.exc_info()[1]
    print(e.args[0])


url = 'http://127.0.0.1:5000/post'

params = {
    "text": "posts Example"
}

try:
    response = requests.post(url, json = params)
    response_data = response.json()
    print(response_data)
except Exception:
    e = sys.exc_info()[1]
    print(e.args[0])
