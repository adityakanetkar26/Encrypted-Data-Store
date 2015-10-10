import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QApplication, QWidget, 
			QToolTip, QPushButton, 
			QMessageBox, QDesktopWidget, 
			QHBoxLayout, QVBoxLayout, 
			QGridLayout, QLineEdit, 
			QTextEdit, QLabel, 
			QFileDialog, QAction, 
			QMainWindow)
from PyQt5.QtGui import (QFont, QIcon)
from PyQt5.QtCore import QCoreApplication
from encryptFile import EncryptFile
from decryptFile import DecryptFile

class HomeScreen(QWidget):

	#Private Variables
	__filePath = None
	__publicKeyPath = None
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
		self.uploadPublicKeyBtn = QPushButton("Upload", self)
		self.uploadPublicKeyBtn.clicked.connect(self.setPublicKeyPath)
		
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
		self.decryptBtn = QPushButton('Decrypt', self)
		self.decryptBtn.setToolTip('Decrypt the selected file. ')
		
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
		self.gridLayout.addWidget(self.uploadPublicKeyBtn, 1, 3)
		
		self.gridLayout.addWidget(self.uploadFileLabel, 2, 0)
		self.gridLayout.addWidget(self.browseFileBtn, 2, 1)
		self.gridLayout.addWidget(self.uploadFilePath, 2, 2)
		self.gridLayout.addWidget(self.encryptBtn, 2, 3)
		
		self.gridLayout.addWidget(self.decryptLabel, 4, 0)
		self.gridLayout.addWidget(self.decryptBtn, 4, 1)

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
		__filePath = fileObj[0]

		if fileObj[0]:
			self.uploadFilePath.setText(fileObj[0])

	#Event handler for browsing public key
        def browsePublicKeyBtnClick(self):
                fileObj = QFileDialog.getOpenFileName(self, 'Select Public Key', '.')
                __filePath = fileObj[0]

                if fileObj[0]:
                        self.uploadPublicKeyPath.setText(fileObj[0])

	#Event handler to select public key
	def setPublicKeyPath(self):
		print self.uploadPublicKeyPath.text()
		self.__publicKeyPath = self.uploadPublicKeyPath.text()

	#Event handler for encrypting file
	def encryptAndUploadFile(self):
		print self.uploadFilePath.text()
		self.__filePath = self.uploadFilePath.text()
		e = EncryptFile(self.__filePath, self.__publicKeyPath)
                t = e.encrypt()
	

if __name__ == '__main__':
	app = QApplication(sys.argv)
	homeScreen = HomeScreen()
	sys.exit(app.exec_())
