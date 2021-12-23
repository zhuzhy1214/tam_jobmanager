

import requests
import sys



url = 'http://localhost:5000'


params = {
    'ID':1,
    'PMstring': 'ALA_101_35.38R'
}

try:
    response = requests.get(url+'/pm-validate/describe')
    response_data = response.json()
    print(response_data)
except Exception:
    e = sys.exc_info()[1]
    print(e.args[0])

for i in range(3):
    try:
        response = requests.post(url+'/pm-validate/submit', json=params)
        response_data = response.json()
        print(response_data)
    except Exception:
        e = sys.exc_info()[1]
        print(e.args[0])

try:
    response = requests.get(url+'/taskmanager')
    response_data = response.json()
    print(response_data)
except Exception:
    e = sys.exc_info()[1]
    print(e.args[0])


# print('add first taskthe function with name pm_validation')
# try:
#     response = requests.post(url+'/tm_add/pm_validation', params)
#     response_data = response.json()
#     print(response_data)
# except Exception:
#     e = sys.exc_info()[1]
#     print(e.args[0])
#
# print("add task with the function with name '1'")
# try:
#     response = requests.post(url+'/tm_add/1', params)
#     response_data = response.json()
#     print(response_data)
# except Exception:
#     e = sys.exc_info()[1]
#     print(e.args[0])
#
# print('check the status of first task')
# try:
#     response = requests.get(url+'/tm_ck/1')
#     response_data = response.json()
#     print(response_data)
# except Exception:
#     e = sys.exc_info()[1]
#     print(e.args[0])


# url = 'http://localhost:5000/todos'
#
# try:
#     response = requests.get(url+'/todo3')
#     response_data = response.json()
#     print(response_data)
# except Exception:
#     e = sys.exc_info()[1]
#     print(e.args[0])

# url = 'http://localhost:5000/todos'

# try:
#     response = requests.post(url, {'task':'additional work'})
#     response_data = response.json()
#     print(response_data)
# except Exception:
#     e = sys.exc_info()[1]
#     print(e.args[0])
#
# try:
#     response = requests.get(url)
#     response_data = response.json()
#     print(response_data)
# except Exception:
#     e = sys.exc_info()[1]
#     print(e.args[0])
#
# try:
#     response = requests.put(url+'/todo2', {'task':'finish work'})
#     response_data = response.json()
#     print(response_data)
# except Exception:
#     e = sys.exc_info()[1]
#     print(e.args[0])
#
# try:
#     response = requests.get(url)
#     response_data = response.json()
#     print(response_data)
# except Exception:
#     e = sys.exc_info()[1]
#     print(e.args[0])

# url = 'http://localhost:5000/todos'
#
# try:
#     response = requests.get(url)
#     response_data = response.json()
#     print(response_data)
# except Exception:
#     e = sys.exc_info()[1]
#     print(e.args[0])
#


url = 'http://localhost:5000/todos'

# try:
#     response = requests.get(url+'/todo3')
#     response_data = response.json()
#     print(response_data)
# except Exception:
#     e = sys.exc_info()[1]
#     print(e.args[0])


#
# url = 'http://localhost:5000/postmile'
#
# params = {
#     "data": ['ALA_101_35.38R', 'SF_1_32.323']
# }
# # params = {
# #     "data": 'ALA_101_35.38R'
# # }
# try:
#     response = requests.put(url+'/2', data=params)
#     response_data = response.json()
#     print(response_data)
# except Exception:
#     e = sys.exc_info()[1]
#     print(e.args[0])
#
url = 'http://localhost:5000/'
#
# params = {
#     'ID':1,
#     'PMstring': 'ALA_101_35.38R'
# }
#
# try:
#     response = requests.put(url+'postmile/1', params)
#     response_data = response.json()
#     print(response_data)
# except Exception:
#     e = sys.exc_info()[1]
#     print(e.args[0])
#
#
# params = {
#     'ID':2,
#     'PMstring': 'ALA_101_35.38R'
# }
# try:
#     response = requests.put(url+'postmile/2', params)
#     response_data = response.json()
#     print(response_data)
# except Exception:
#     e = sys.exc_info()[1]
#     print(e.args[0])


# try:
#     response = requests.get(url+'postmile/5')
#     response_data = response.json()
#     print(response_data)
# except Exception:
#     e = sys.exc_info()[1]
#     print(e.args[0])

# try:
#     func_name = 'verification'
#     response = requests.get(url+'postmile/'+func_name)
#     response_data = response.json()
#     print(response_data)
# except Exception:
#     e = sys.exc_info()[1]
#     print(e.args[0])
#
#
# try:
#     func_name = '5'
#     response = requests.get(url+'postmile/'+func_name)
#     response_data = response.json()
#     print(response_data)
# except Exception:
#     e = sys.exc_info()[1]
#     print(e.args[0])


#
# url = 'http://localhost:5000/api'
#
# try:
#     response = requests.get(url)
#     response_data = response.json()
#     print(response_data)
#
# except Exception:
#     e = sys.exc_info()[1]
#     print(e.args[0])
#
#
# url = 'http://127.0.0.1:5000/pm-validate'
#
# params = {
#     'ID':1,
#     'PMstring': ['ALA_101_35.38R']
# }
#
# try:
#     response = requests.post(url+'/pm-validate/1', json=params)
#     response_data = response.json()
#     print(response_data)
# except Exception:
#     e = sys.exc_info()[1]
#     print(e.args[0])
#
# # try:
# #     response = requests.get(url+'/pm-validate/1')
# #     response_data = response.json()
# #     print(response_data)
# # except Exception:
# #     e = sys.exc_info()[1]
# #     print(e.args[0])
#
#
# try:
#     response = requests.get(url+'/pm-validate/3')
#     response_data = response.json()
#     print(response_data)
# except Exception:
#     e = sys.exc_info()[1]
#     print(e.args[0])