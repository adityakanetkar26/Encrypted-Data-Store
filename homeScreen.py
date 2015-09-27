import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QApplication, QWidget, 
			QToolTip, QPushButton, 
			QMessageBox, QDesktopWidget, 
			QHBoxLayout, QVBoxLayout, 
			QGridLayout, QLineEdit, 
			QTextEdit, QLabel)
from PyQt5.QtGui import QFont
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
		
		e = EncryptFile(filePath, publicKeyPath)
		t = e.encrypt()
		d = DecryptFile(privateKeyPath, t)
		d.decrypt()
		
		self.setWindowTitle("Encrypted Data Store")

		QToolTip.setFont(QFont('SansSerif', 10))
		
		uploadLabel = QLabel("Encrypt and Upload", self)
		uploadFilePath = QLineEdit(self)
		
		encryptBtn = QPushButton('Encrypt and Upload', self)
		encryptBtn.setToolTip('Encrypt and upload the file. ')
		encryptBtn.resize(encryptBtn.sizeHint())

		decryptLabel = QLabel("Choose which file to decrypt: ", self)
		decryptBtn = QPushButton('Decrypt', self)
		decryptBtn.setToolTip('Decrypt the selected file. ')
		decryptBtn.resize(decryptBtn.sizeHint())
		
		quitBtn = QPushButton('Quit', self)
		quitBtn.setToolTip('Exit the application. ')
		quitBtn.clicked.connect(QCoreApplication.instance().quit)
		quitBtn.resize(quitBtn.sizeHint())

		gridLayout = QGridLayout()
		gridLayout.setSpacing(10)
		
		gridLayout.addWidget(uploadLabel, 1, 0)
		gridLayout.addWidget(uploadFilePath, 1, 1)
		gridLayout.addWidget(encryptBtn, 2, 1)
		
		gridLayout.addWidget(decryptLabel, 3, 0)
		gridLayout.addWidget(decryptBtn, 3, 1)

		gridLayout.addWidget(quitBtn, 5, 1)
		
		self.setLayout(gridLayout)
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

if __name__ == '__main__':
	app = QApplication(sys.argv)
	homeScreen = HomeScreen()
	sys.exit(app.exec_())
