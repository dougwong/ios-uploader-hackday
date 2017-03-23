import photos, requests
from objc_util import ObjCInstance

baseURL = "http://172.16.20.138:9080/api/jsonws/dlapp/"
userEmail = "test@liferay.com"
password = "test"
command = "add-file-entry"
data = {'repositoryId': 20147, 'folderId': 30848}

def uploadFileToLiferay(title, file):
	data = {
		'mimeType' : '', 
		'description' : 'Test picture', 
		'changeLog' : '', 
		'sourceFileName' : '', 
		'title' : title, 
		'serviceContext' : {}, 
		'repositoryId' : 20147, 
		'folderId' : 30848 }
	files = {
		'file' : file
	}

	response = requests.post(baseURL + command, 
		auth=(userEmail, password), 
		params=data, 
		files=files)

	if response.status_code != 200:
		print("Sorry, unable to upload file.") 
		print(response.status_code)
		print(response.text)

asset_collections = photos.get_albums()

for asset_collection in asset_collections:
	if asset_collection.title == 'Hackday':
		hackday_album = asset_collection

		break

if hackday_album:
	print(len(hackday_album.assets))
	for asset in hackday_album.assets:
		print(asset.local_id)
		filename = str(ObjCInstance(asset).filename())
		uploadFileToLiferay(filename, asset.get_image_data())
