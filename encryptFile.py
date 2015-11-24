import os, base64, uuid
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import SHA256

#Imports for Google Drive Authentication
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class EncryptFile():
	
	#Private variables
	__filePath = None
	__fileName = None
	__padCount = 0
	__ptString = None
	__ptChunks = None
	__ctChunks = None
	__publicKey = None

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
		manifestWrite.write(self.__fileName +  "\t" + str(self.__padCount) + "\n")

		filesLocation = os.path.join("AdminStore", "files.txt")
		filesPath = os.path.join(workingDirectory, filesLocation)
		filesWrite = open(filesPath, "a")
		filesWrite.write(self.__fileName)
		filesWrite.write("\n")
		filesWrite.close()

		gauth = GoogleAuth()
		gauth.LocalWebserverAuth()
		drive = GoogleDrive(gauth)
		
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

			file = drive.CreateFile({'title': encFileName})
			file.SetContentFile(encFilePath)
			file.Upload()

			os.remove(encFilePath)
			
		manifestWrite.write("\n")
		manifestWrite.close()
