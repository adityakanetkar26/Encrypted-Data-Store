import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QApplication, QWidget, 
			QToolTip, QPushButton, 
			QMessageBox, QDesktopWidget)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QCoreApplication

class HomeScreen(QWidget):
	#Constructor
	def __init__(self):
	        super(HomeScreen, self).__init__() 
	        self.initUI()

	#Initial buttons that should be present on the screen when the application is started. 
	def initUI(self):
		self.setWindowTitle("Encrypted Data Store")

		QToolTip.setFont(QFont('SansSerif', 10))
		
		encryptBtn = QPushButton('Encrypt', self)
		encryptBtn.setToolTip('Encrypt and upload the file. ')
		encryptBtn.resize(encryptBtn.sizeHint())
		encryptBtn.move(50, 50)
		
		quitBtn = QPushButton('Quit', self)
		quitBtn.setToolTip('Exit the application. ')
		quitBtn.clicked.connect(QCoreApplication.instance().quit)
		quitBtn.resize(quitBtn.sizeHint())

		self.setWindowState(QtCore.Qt.WindowMaximized)
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
