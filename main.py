from PyQt5.QtWidgets import QApplication
import sys

from mainWindow import MainWindow

application = QApplication(sys.argv)
window = MainWindow()
sys.exit(application.exec_())
