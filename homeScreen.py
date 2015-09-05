import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon

class HomeScreen(QWidget):
	def __init__(self):
	        super(HomeScreen, self).__init__() 
	        self.initUI()

	def initUI(self):
		self.setWindowTitle("Encrypted Data Store")
		self.show()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	homeScreen = HomeScreen()
	sys.exit(app.exec_())
