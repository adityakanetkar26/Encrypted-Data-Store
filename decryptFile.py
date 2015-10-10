import os, base64
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto import Random

class DecryptFile():
	
	#Private variables
	__encChunks = None
	__privateKey = None
	__ptChunks = None
	__ptString = ""


	#Constructor
	def __init__(self, privateKeyPath, encChunks):
		self.__encChunks = encChunks
		self.__privateKey = RSA.importKey(open(privateKeyPath).read())
		
	#Decryption method
	def decrypt(self):
		self.__decryptFile()
	
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
