import requests

data = {'repositoryId': 20147, 'folderId': 30848}

response = requests.get('http://172.16.20.138:9080/api/jsonws/dlapp/get-subfolder-ids', auth=('test@liferay.com', 'test'), json=data)

print(response.text)