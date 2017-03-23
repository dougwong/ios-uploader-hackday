import requests

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
		'file' : open(file, 'rb')
	}

	try:
		response = requests.post(baseURL + command, 
			auth=(userEmail, password), 
			params=data, 
			files=files)

		# print(response.status_code)
		# print(response.text)
		
		response.raise_for_status()
	except requests.exceptions.HTTPError as e:
		print("Sorry, unable to upload file.")
		print(e)


if __name__ == '__main__':
    import  argparse
    parser = argparse.ArgumentParser()

    #Required
    parser.add_argument("-t", "--title", dest="title", type=str, help="Set the file name.")
    parser.add_argument("-f", "--file", dest="file", type=str, help="Set the file to upload.")

    parser.add_argument("command", nargs=1, choices=['upload', 'check'],  help="Specify a command. e.g. upload, check.")

    args = parser.parse_args()

    if args.command[0] == 'upload':
    	print("Uploading " + args.file + " as " + args.title + " to liferay.")
    	uploadFileToLiferay(args.title, args.file)
