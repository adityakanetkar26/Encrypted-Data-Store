import os, base64
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto import Random

class DecryptFile():
	
	#Private variables
	__fileName = None
	__chunkDetails = None
	__encChunks = None
	__privateKey = None
	__ptChunks = None
	__ptString = ""


	#Constructor
	def __init__(self, privateKeyPath, fileName):
		#self.__encChunks = encChunks
		self.__fileName = fileName
		self.__privateKey = RSA.importKey(open(privateKeyPath).read())
		print self.__fileName
		self.__chunkDetails = []
	
	#Decryption method
	def decrypt(self):
		self.__getChunkInfoFromManifest()
		#self.__downloadChunksFromGoogleDrive()

		#self.__decryptFile()

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
			chunkDetails["chunkId"] = splitDetails[2]	
			self.__chunkDetails.append(chunkDetails)
			i = i + 1

		print self.__chunkDetails

	#Method to download chunks from Google Drive
	#def __downloadChunksFromGoogleDrive():
				
			
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
		
		print self.__ptString
