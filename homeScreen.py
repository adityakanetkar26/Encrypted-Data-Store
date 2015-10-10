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
		
		self.uploadLabel = QLabel("Encrypt and Upload", self)
		self.uploadFilePath = QLineEdit(self)
	
		self.browseBtn = QPushButton("Browse", self)
		self.browseBtn.clicked.connect(self.browseBtnClick)
	
		self.encryptBtn = QPushButton('Encrypt and Upload', self)
		self.encryptBtn.setToolTip('Encrypt and upload the file. ')

		self.decryptLabel = QLabel("Choose which file to decrypt: ", self)
		self.decryptBtn = QPushButton('Decrypt', self)
		self.decryptBtn.setToolTip('Decrypt the selected file. ')
		
		self.quitBtn = QPushButton('Quit', self)
		self.quitBtn.setToolTip('Exit the application. ')
		self.quitBtn.clicked.connect(QCoreApplication.instance().quit)

		self.gridLayout = QGridLayout()
		self.gridLayout.setSpacing(10)
		
		self.gridLayout.addWidget(self.uploadLabel, 1, 0)
		self.gridLayout.addWidget(self.uploadFilePath, 1, 1)
		self.gridLayout.addWidget(self.browseBtn, 2, 0)
		self.gridLayout.addWidget(self.encryptBtn, 2, 1)
		
		self.gridLayout.addWidget(self.decryptLabel, 3, 0)
		self.gridLayout.addWidget(self.decryptBtn, 3, 1)

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

	def browseBtnClick(self):
		fileObj = QFileDialog.getOpenFileName(self, 'Open File', '.')
		__filePath = fileObj[0]

		if fileObj[0]:
			self.uploadFilePath.setText(fileObj[0])

if __name__ == '__main__':
	app = QApplication(sys.argv)
	homeScreen = HomeScreen()
	sys.exit(app.exec_())
