import os, base64
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto import Random

#Imports for Google Drive Authentication
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class DecryptFile():
	
	#Private variables
	__fileName = None
	__chunkDetails = None
	__encChunks = None
	__privateKey = None
	__ptChunks = None
	__padCount = 0
	__ptString = ""
	__plainTextPath = None


	#Constructor
	def __init__(self, privateKeyPath, fileName):
		self.__fileName = fileName
		self.__privateKey = RSA.importKey(open(privateKeyPath).read())
		self.__chunkDetails = []
		self.__encChunks = []
		self.__padCount = 0
	
	#Decryption method
	def decrypt(self):
		self.__getChunkInfoFromManifest()
		self.__downloadChunksFromGoogleDrive()
		self.__extractDataFromDownloadedFiles()
		self.__decryptFile()
		self.__removePadding()
		self.__populatePlainTextFile()
		return self.__plainTextPath

	#Get information about chunk names from the manifest
	def __getChunkInfoFromManifest(self):
		workingDirectory = os.getcwd()
		manifestDirectory = os.path.join(workingDirectory, "AdminStore")
		manifestPath = os.path.join(manifestDirectory, "manifest.txt")
		manifestRead = open(manifestPath, "r")

		fileDetails = manifestRead.readlines()
		manifestRead.close()

		i = 0
		fileFound = False
		while i < len(fileDetails):
			splitDetails = fileDetails[i].split("\t")
			
			j = 0
			while j < len(splitDetails):
				print splitDetails[j]
				if self.__fileName in splitDetails[j]:
					padCountStr = splitDetails[j + 1]
					padCountStr = padCountStr[:-1]
					self.__padCount = int(padCountStr)
					fileFound = True
					break
				
				j = j + 1
			if fileFound == True:
				i = i + 1
				break	
			i = i + 1

		while i < len(fileDetails) and fileDetails[i] != "\n":
			splitDetails = fileDetails[i].split("\t")
			chunkDetails = {}
			chunkDetails["FileName"] = splitDetails[0] + ".txt"
			chunkId = splitDetails[2]
			chunkId = chunkId[:-1]
			chunkDetails["chunkId"] = chunkId	
			self.__chunkDetails.append(chunkDetails)
			i = i + 1

	#Method to download chunks from Google Drive
	def __downloadChunksFromGoogleDrive(self):
		gauth = GoogleAuth()
		gauth.LocalWebserverAuth()
		drive = GoogleDrive(gauth)

		workingDirectory = os.getcwd()

		for chunkInfo in self.__chunkDetails:
			downloadFile = drive.CreateFile({"id": chunkInfo["chunkId"]})
			downloadFile.GetContentFile(chunkInfo["FileName"])
			
			srcPath = os.path.join(workingDirectory, chunkInfo["FileName"])
			destDirPath = os.path.join(workingDirectory, "Store")
			destPath = os.path.join(destDirPath, chunkInfo["FileName"])
			os.rename(srcPath, destPath)				

	#Method to retrieve encrypted data from the downloaded chunks
	def __extractDataFromDownloadedFiles(self):
		workingDirectory = os.getcwd()
		storePath = os.path.join(workingDirectory, "Store")
		for chunkInfo in self.__chunkDetails:
			encFilePath = os.path.join(storePath, chunkInfo["FileName"])
			fileReader = open(encFilePath, "r")
			fileLines = fileReader.readlines()
			
			chunkInfo = {}
			i = 0
			while i < len(fileLines):
				if "IV\n" in fileLines[i]:
					iv = fileLines[i + 1]
					chunkInfo["iv"] = iv[:-1]
				if "Encrypted Session Key\n" in fileLines[i]:
					sessKey = fileLines[i + 1]
					chunkInfo["encSessKey"] = sessKey[:-1]
				if "CipherText\n" in fileLines[i]:
					cipherText = fileLines[i + 1]
					chunkInfo["cipherText"] = cipherText[:-1]
				i = i + 2	
			self.__encChunks.append(chunkInfo)
			fileReader.close()
			os.remove(encFilePath)
			
	#Method for decryption of chunks
	def __decryptFile(self):
		for ctChunk in self.__encChunks:
			iv = base64.b64decode(ctChunk["iv"])
			encSessionKey = base64.b64decode(ctChunk["encSessKey"])
			cipherText = base64.b64decode(ctChunk["cipherText"])
			
			sessCipher = PKCS1_OAEP.new(self.__privateKey)
			sessionKey = sessCipher.decrypt(encSessionKey)
		
			cipher = AES.new(sessionKey, AES.MODE_CBC, iv)
			plainText = cipher.decrypt(cipherText)
			self.__ptString = self.__ptString + plainText
		
	#Method to remove extra padding
	def __removePadding(self):
		if self.__padCount != 0:
			self.__ptString = self.__ptString[:-1 * self.__padCount]

	#Method to populate plaintext file
	def __populatePlainTextFile(self):
		workingDirectory = os.getcwd()
		plainTextDir = os.path.join(workingDirectory, "Store")
		self.__plainTextPath = os.path.join(plainTextDir, self.__fileName)
		plainTextFile = open(self.__plainTextPath, "w")
		plainTextFile.write(self.__ptString)
		plainTextFile.close()

