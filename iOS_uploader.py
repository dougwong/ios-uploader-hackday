import photos, requests
from objc_util import ObjCInstance

base_url = "http://portal.dougtest.wedeploy.io"
user_email = "test@liferay.com"
password = "test1234"
repository_id = 20147
folder_id = 30723
album_name = 'Hackday'
keeper_album_name = 'Keeper'

def upload_file(title, file):
	data = {
		'mimeType': '', 
		'description': '', 
		'changeLog': '', 
		'sourceFileName': '', 
		'title': title, 
		'serviceContext': {}, 
		'repositoryId': repository_id, 
		'folderId': folder_id
	}

	files = {
		'file': file
	}

	response = requests.post(
		base_url + "/api/jsonws/dlapp/add-file-entry", 
		auth=(user_email, password), 
		params=data, 
		files=files)

	if response.status_code != 200:
		json = response.json()

		if json['throwable'].startswith("com.liferay.document.library.kernel.exception.DuplicateFileEntryException"):
			print("Sorry, unable to upload file: %s. A file with the name '%s' already exists." % (title, title))
		else:
			print("Sorry, unable to upload file: %s. %i - %s" % (title, response.status_code, response.text))
	
	return response.status_code

hackday_album = None
keeper_album = None

asset_collections = photos.get_albums()

for asset_collection in asset_collections:
	if asset_collection.title == album_name:
		hackday_album = asset_collection
		
	if asset_collection.title == keeper_album_name:
		keeper_album = asset_collection

	if hackday_album and keeper_album:
		break

keeper_filenames = []

if keeper_album:
	for asset in keeper_album.assets:
		filename = str(ObjCInstance(asset).filename())

		keeper_filenames.append(filename)

if hackday_album:
	print("%i files found in the album" % (len(hackday_album.assets)))

	delete_assets = []

	for asset in hackday_album.assets:
		filename = str(ObjCInstance(asset).filename())

		print("Uploading file '%s'" % (filename))

		status_code = upload_file(filename, asset.get_image_data())

		if status_code == 200:
			if filename not in keeper_filenames:
				delete_assets.append(asset)
			else:
				print("%s was found in the 'Keeper' album and will not be deleted" % (filename))

	photos.batch_delete(delete_assets)			

	print("Upload complete.")
