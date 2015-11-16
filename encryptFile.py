from __future__ import print_function

import os, base64, uuid
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import SHA256

#Imports for Google Drive Authentication
import httplib2

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools


class EncryptFile():
	
	#Private variables
	__filePath = None
	__fileName = None
	__padCount = 0
	__ptString = None
	__ptChunks = None
	__ctChunks = None
	__publicKey = None

	SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
	CLIENT_SECRET_FILE = 'client_secret.json'
	APPLICATION_NAME = 'Drive API Python Quickstart'

	#Constructor
	def __init__(self, fPath, keyPath):
		self.__filePath = fPath
		self.__fileName = os.path.basename(fPath)
		self.__padCount = 0
		self.__ptChunks = []
		self.__ctChunks = []
		self.__publicKey = RSA.importKey(open(keyPath).read())	
	
	#Encryption Method
	def encrypt(self):
		self.__readFile()
		self.__splitFile()
		self.__encryptChunks()
		self.__populateFilesAndManifest()
		return self.__ctChunks

	#Private method to read the file		
	def __readFile(self):
		ptFile = open(self.__filePath, "r")	
		self.__ptString = ptFile.read()

	#Pad Zeros + Split file into chunks
	def __splitFile(self):
		self.__padCount = len(self.__ptString) % 64
		i = 0
		while(i != 64 - self.__padCount):
			self.__ptString = self.__ptString + "0"
			i = i + 1
		
		self.__splitStringBy64()

	#Split a string into 64 byte chunks
	def __splitStringBy64(self):
		tempStr = self.__ptString
		while tempStr:
			self.__ptChunks.append(tempStr[:64])
			tempStr = tempStr[64:]

	#Method to encrypt chunks
	def __encryptChunks(self):
		
		for chunk in self.__ptChunks:
			encryptedInfo = {}
			sessKey = Random.new().read(32)
			iv = Random.new().read(AES.block_size)
			cipher = AES.new(sessKey, AES.MODE_CBC, iv)
			cipherText = cipher.encrypt(chunk)
			
			sessCipher = PKCS1_OAEP.new(self.__publicKey)
			sessCipherText = sessCipher.encrypt(sessKey)
		
			encryptedInfo["iv"] = base64.b64encode(iv)
			encryptedInfo["encSessKey"] = base64.b64encode(sessCipherText)
			encryptedInfo["cipherText"] = base64.b64encode(cipherText)
			self.__ctChunks.append(encryptedInfo)

	#Method to populate the manifest file
	def __populateFilesAndManifest(self):
		workingDirectory = os.getcwd()
		storeDirectory = os.path.join(workingDirectory, "Store")

		manifestLocation = os.path.join("AdminStore", "manifest.txt")
		manifestPath = os.path.join(workingDirectory, manifestLocation)
		manifestWrite = open(manifestPath, "a")
		manifestWrite.write(self.__fileName + "\n")

		self.__googleDriveAuth()
		
		for chunk in self.__ctChunks:
			salt = base64.urlsafe_b64encode(uuid.uuid4().bytes)		
	
			hashInput = salt + chunk["iv"] + chunk["encSessKey"] + chunk["cipherText"]
			hashObj = SHA256.new()
			hashObj.update(hashInput)
			encFileName = hashObj.hexdigest() + ".txt"
			encFilePath = os.path.join(storeDirectory, encFileName)
			
			fileWrite = open(encFilePath, "w")
			fileWrite.write("IV\n")
			fileWrite.write(chunk["iv"] + "\n")
						
			fileWrite.write("Encrypted Session Key\n")
			fileWrite.write(chunk["encSessKey"] + "\n")
			
			fileWrite.write("CipherText\n")
			fileWrite.write(chunk["cipherText"] + "\n")
		
			fileWrite.close()
			
					
			manifestWrite.write(hashObj.hexdigest() + "\t" + salt + "\n")

		manifestWrite.write("\n")
		manifestWrite.close()

	def __googleDriveAuth(self):
		credentials = self.__get_credentials()
		http = credentials.authorize(httplib2.Http())
		service = discovery.build('drive', 'v2', http=http)

		results = service.files().list(maxResults=10).execute()
		items = results.get('items', [])
		if not items:
			print('No files found.')
		else:
			print('Files:')
		for item in items:
			print('{0} ({1})'.format(item['title'], item['id']))
	
	def __get_credentials(self):
		"""Gets valid user credentials from storage.
		If nothing has been stored, or if the stored credentials are invalid,
		the OAuth2 flow is completed to obtain the new credentials.

		Returns:
		Credentials, the obtained credential.
		"""
		home_dir = os.path.expanduser('~')
		credential_dir = os.path.join(home_dir, '.credentials')
		if not os.path.exists(credential_dir):
			os.makedirs(credential_dir)
		credential_path = os.path.join(credential_dir, 'drive-python-quickstart.json')

		store = oauth2client.file.Storage(credential_path)
		credentials = store.get()
		if not credentials or credentials.invalid:
			flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
			flow.user_agent = APPLICATION_NAME
			if flags:
				credentials = tools.run_flow(flow, store, flags)
			else: # Needed only for compatibility with Python 2.6
				credentials = tools.run(flow, store)
			print('Storing credentials to ' + credential_path)
		return credentials
	
