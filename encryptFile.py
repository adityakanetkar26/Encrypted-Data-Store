import os
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA

class EncryptFile():
	__filePath = None
	__fileName = None
	__padCount = 0
	__ptString = None
	__ptChunks = None
	__ctChunks = None

	#Constructor
	def __init__(self, fPath):
		self.__filePath = fPath
		self.__fileName = os.path.basename(fPath)
		self.__padCount = 0
		self.__ptChunks = []
		self.__ctChunks = []
	
	#Encryption Method
	def encrypt(self):
		self.__readFile()
		self.__splitFile()

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
			publicKey, privateKey = self.__generateRSAKeyPair()
			

	
	def __generateRSAKeyPair(self):
		RSAKey = RSA.generate(2048)
		publicKey = RSAKey.publickey().exportKey()
		privateKey = RSAKey.exportKey()
		return publicKey, privateKey
