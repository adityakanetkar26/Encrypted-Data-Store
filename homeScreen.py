import sys, os
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QApplication, QWidget, 
			QToolTip, QPushButton, 
			QMessageBox, QDesktopWidget, 
			QHBoxLayout, QVBoxLayout, 
			QGridLayout, QLineEdit, 
			QTextEdit, QLabel, 
			QFileDialog, QAction, 
			QMainWindow, QErrorMessage, 
			QComboBox)
from PyQt5.QtGui import (QFont, QIcon)
from PyQt5.QtCore import QCoreApplication
from encryptFile import EncryptFile
from decryptFile import DecryptFile

class HomeScreen(QWidget):

	#Constructor
	def __init__(self):
	        super(HomeScreen, self).__init__() 
	        self.initUI()

	#Initial buttons that should be present on the screen when the application is started. 
	def initUI(self):
		filePath = "/home/aditya/SpcPrblm/Encrypted-Data-Store/TestFiles/Stats.txt"
		publicKeyPath = "/home/aditya/SpcPrblm/Encrypted-Data-Store/TestFiles/public_key.pem"
		privateKeyPath = "/home/aditya/SpcPrblm/Encrypted-Data-Store/TestFiles/private_key.pem"
		
		#e = EncryptFile(filePath, publicKeyPath)
		#t = e.encrypt()
		#d = DecryptFile(privateKeyPath, t)
		#d.decrypt()
		
		self.setWindowTitle("Encrypted Data Store")

		QToolTip.setFont(QFont('SansSerif', 10))
		
		#GUI for uploading Public Key
		self.uploadPublicKeyLabel = QLabel("Upload Public Key", self)
		self.uploadPublicKeyPath = QLineEdit(self)
		self.browsePublicKeyBtn = QPushButton("Browse", self)
		self.browsePublicKeyBtn.clicked.connect(self.browsePublicKeyBtnClick)
		
		#GUI for selecting Plaintext File	
		self.uploadFileLabel = QLabel("Encrypt and Upload", self)
		self.uploadFilePath = QLineEdit(self)
		self.browseFileBtn = QPushButton("Browse", self)
		self.browseFileBtn.clicked.connect(self.browseFileBtnClick)

		#GUI for Encryption
		self.encryptBtn = QPushButton('Encrypt and Upload', self)
		self.encryptBtn.setToolTip('Encrypt and upload the file. ')
		self.encryptBtn.clicked.connect(self.encryptAndUploadFile)

		#GUI for Decryption
		self.decryptLabel = QLabel("Choose which file to decrypt: ", self)
		self.uploadPrivateKeyPath = QLineEdit(self)
		self.browsePrivateKeyBtn = QPushButton("Browse", self)
		self.browsePrivateKeyBtn.clicked.connect(self.browsePrivateKeyBtnClick)
		self.decryptFileList = QComboBox(self)
		self.decryptFileList.activated[str].connect(self.onActivated)
		self.populateFileNames()
		self.decryptBtn = QPushButton('Decrypt', self)
		self.decryptBtn.setToolTip('Decrypt the selected file. ')
		self.decryptBtn.clicked.connect(self.downloadAndDecryptFile)
		
		#GUI for Quitting Application
		self.quitBtn = QPushButton('Quit', self)
		self.quitBtn.setToolTip('Exit the application. ')
		self.quitBtn.clicked.connect(QCoreApplication.instance().quit)

		#Grid Layout to organize all buttons
		self.gridLayout = QGridLayout()
		self.gridLayout.setSpacing(10)
		
		self.gridLayout.addWidget(self.uploadPublicKeyLabel, 1, 0)
		self.gridLayout.addWidget(self.browsePublicKeyBtn, 1, 1)
		self.gridLayout.addWidget(self.uploadPublicKeyPath, 1, 2)
		
		self.gridLayout.addWidget(self.uploadFileLabel, 2, 0)
		self.gridLayout.addWidget(self.browseFileBtn, 2, 1)
		self.gridLayout.addWidget(self.uploadFilePath, 2, 2)
		self.gridLayout.addWidget(self.encryptBtn, 2, 3)
		
		self.gridLayout.addWidget(self.decryptLabel, 4, 0)
		self.gridLayout.addWidget(self.decryptFileList, 4, 1)
		self.gridLayout.addWidget(self.browsePrivateKeyBtn, 4, 2)
		self.gridLayout.addWidget(self.uploadPrivateKeyPath, 4, 3)
		self.gridLayout.addWidget(self.decryptBtn, 4, 4)

		self.gridLayout.addWidget(self.quitBtn, 5, 1)
		
		self.setLayout(self.gridLayout)
		self.setWindowState(QtCore.Qt.WindowMaximized)
		#self.setGeometry(300, 300, 300, 300)
		self.show()

	#Re-implementation of the closeEvent() event handler. 
	#Displaying a message when the user tries to quit the application. 
	def closeEvent(self, event):

		reply = QMessageBox.question(self, 'Message', 
				"Are you sure you want to quit?", 
				QMessageBox.Yes | QMessageBox.No, 
				QMessageBox.No)
		if reply == QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()

	#Ensuring that the window is displayed on the center of the screen. 
	def center(self):
		mainWindowGeometry = self.frameGeometry()
		centerPoint = QDesktopWidget().availableGeometry().center()
		
		mainWindowGeometry.moveCenter(centerPoint)
		self.move(mainWindowGeometry.topLeft())		

	#Event Handler for browsing file to encrypt
	def browseFileBtnClick(self):
		fileObj = QFileDialog.getOpenFileName(self, 'Open File', '.')

		if fileObj[0]:
			self.uploadFilePath.setText(fileObj[0])

	#Event handler for browsing public key
        def browsePublicKeyBtnClick(self):
                fileObj = QFileDialog.getOpenFileName(self, 'Select Public Key', '.')

                if fileObj[0]:
                        self.uploadPublicKeyPath.setText(fileObj[0])

	#Event handler for browsing private key
	def browsePrivateKeyBtnClick(self):
		fileObj = QFileDialog.getOpenFileName(self, "Select Private Key", ".")

		if fileObj[0]:
			self.uploadPrivateKeyPath.setText(fileObj[0])

	#Event handler for encrypting file and uploading chunks
	def encryptAndUploadFile(self):
		if self.uploadPublicKeyPath.text() == "" or self.uploadFilePath.text() == "":
			errorMsg = QErrorMessage(self)
			errorMsg.showMessage("Both the values should represent actual files. ")
		else:
			print self.uploadFilePath
			print self.uploadPublicKeyPath	
			print self.checkIfSameFileNameExists()			
			if self.checkIfSameFileNameExists():
				errorMsg = QErrorMessage(self)
				errorMsg.showMessage("File of the same name already exists. ")
			else:
				e = EncryptFile(self.uploadFilePath.text(), self.uploadPublicKeyPath.text())
        	        	t = e.encrypt()
	
	#Check if file with the same name has already been encrypted
	def checkIfSameFileNameExists(self):
		fileName = os.path.basename(self.uploadFilePath.text()) + "\n"
		workingDirectory = os.getcwd()
		filesPath = os.path.join(workingDirectory, "AdminStore")
		filesPath = os.path.join(filesPath, "files.txt")

		filePtr = open(filesPath, "r")
		files = filePtr.readlines()
	
		if fileName in files:
			return True
		else:
			return False

	#Populate files that can be decrypted or deleted in the ComboBox
	def populateFileNames(self):
		workingDirectory = os.getcwd()
		adminStorePath = os.path.join(workingDirectory, "AdminStore")
		adminStoreFiles = os.path.join(adminStorePath, "files.txt")
		
		filesList = open(adminStoreFiles, "r")
		fileLines = filesList.readlines()
		
		self.decryptFileList.addItem("")
		for fileName in fileLines:
			fileName = fileName[:-1]
			self.decryptFileList.addItem(fileName)

	#Event handler for downloading chunks and decrypting file
	def downloadAndDecryptFile(self):

		if not hasattr(self, "selectedFileName"):
			errorMsg = QErrorMessage(self)
			errorMsg.showMessage("Select a file. ")
		else:
			if self.uploadPrivateKeyPath.text() == "":
				errorMsg = QErrorMessage(self)
				errorMsg.showMessage("Should represent an actual file")
			else:
				d = DecryptFile(self.uploadPrivateKeyPath.text(), self.selectedFileName)
				d.decrypt()				

	def onActivated(self, text):
		self.selectedFileName = text
		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	homeScreen = HomeScreen()
	sys.exit(app.exec_())
