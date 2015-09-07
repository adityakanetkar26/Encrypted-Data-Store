import os, base64
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto import Random

class EncryptFile():
	
	#Private methods
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
			print encryptedInfo
			
