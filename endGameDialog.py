from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

from imageLoaderUtilities import get_image_path


class EndGameDialog(QDialog):

    def __init__(self, win: bool, **kwargs):
        super(EndGameDialog, self).__init__(**kwargs)

        self.__win = win

        self.__init_gui()

    def __init_gui(self):
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(get_image_path("mine.png")))
        self.setFixedSize(200, 100)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.__get_message_label())
        okButton = QPushButton("OK")
        okButton.clicked.connect(self.close)
        layout.addWidget(okButton)
        layout.addStretch()

        self.setLayout(layout)
        self.setWindowTitle("End Game")

    def __get_message_label(self):
        label = QLabel()
        styleSheet = "font-weight: bold"

        if self.__win:
            message = "YOU WON!\n"
            styleSheet += "; color: green"
        else:
            message = "YOU LOST!\n"
            styleSheet += "; color: red"

        label.setStyleSheet(styleSheet)
        label.setText(message)
        label.setAlignment(Qt.AlignCenter)

        return label
