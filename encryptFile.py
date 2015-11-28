import os, base64, uuid, time
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
	__lastBlockLength = 0
	__ptString = None
	__ptChunks = None
	__ctChunks = None
	__publicKey = None
	__chunkSize = 0

	#Constructor
	def __init__(self, fPath, keyPath):
		self.__filePath = fPath
		self.__fileName = os.path.basename(fPath)
		self.__lastBlockLength = 0
		self.__ptChunks = []
		self.__ctChunks = []
		self.__publicKey = RSA.importKey(open(keyPath).read())
		self.__chunkSize = 64	
	
	#Encryption Method
	def encrypt(self):
		beforeEncTime = time.time()
		self.__readFile()
		self.__splitFile()
		self.__encryptChunks()
		afterEncTime = time.time()
		print "Difference: Time for Encryption: " + str(afterEncTime - beforeEncTime)
		self.__populateFilesAndManifest()

	#Private method to read the file		
	def __readFile(self):
		ptFile = open(self.__filePath, "r")	
		self.__ptString = ptFile.read()

	#Pad Zeros + Split file into chunks
	def __splitFile(self):
		self.__lastBlockLength = len(self.__ptString) % self.__chunkSize
		i = 0
		while(i != self.__chunkSize - self.__lastBlockLength):
			self.__ptString = self.__ptString + "0"
			i = i + 1
		
		self.__splitStringByChunkSize()

	#Split a string into chunks determined by the chunk size
	def __splitStringByChunkSize(self):
		tempStr = self.__ptString
		while tempStr:
			self.__ptChunks.append(tempStr[:self.__chunkSize])
			tempStr = tempStr[self.__chunkSize:]
	
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
		manifestWrite.write(self.__fileName +  "\t" + str(self.__chunkSize - self.__lastBlockLength) + "\n")

		filesLocation = os.path.join("AdminStore", "files.txt")
		filesPath = os.path.join(workingDirectory, filesLocation)
		filesWrite = open(filesPath, "a")
		filesWrite.write(self.__fileName)
		filesWrite.write("\n")
		filesWrite.close()

		gauth = GoogleAuth()
		gauth.LocalWebserverAuth()
		drive = GoogleDrive(gauth)

		beforeUploadTime = time.time()
		
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
					
			manifestWrite.write(hashObj.hexdigest() + "\t" + salt + "\t")

			uploadFile = drive.CreateFile({'title': encFileName})
			uploadFile.SetContentFile(encFilePath)
			uploadFile.Upload()
		
			manifestWrite.write(uploadFile["id"] + "\n")
			
			os.remove(encFilePath)

		afterUploadTime = time.time()
		print "Difference: Time to upload: " + str(afterUploadTime - beforeUploadTime)
			
		manifestWrite.write("\n")
		manifestWrite.close()
