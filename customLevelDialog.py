from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSpinBox

from imageLoaderUtilities import get_image_path
from level import Level


class CustomLevelDialog(QDialog):

    def __init__(self, parent, currentGameLevel: Level):
        super(CustomLevelDialog, self).__init__(parent)

        self.__init_gui(currentGameLevel)

    def __init_gui(self, currentGameLevel: Level):
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(get_image_path("mine.png")))
        self.setFixedSize(200, 150)

        mainLayout = QHBoxLayout()
        inputLayout = QVBoxLayout()
        buttonsLayout = QVBoxLayout()
        heightLayout = QHBoxLayout()
        widthLayout = QHBoxLayout()
        bombsCountLayout = QHBoxLayout()

        self.__heightSpinBox = QSpinBox()
        self.__heightSpinBox.setFixedSize(50, 20)
        self.__heightSpinBox.setMinimum(0)
        self.__heightSpinBox.setMaximum(99)
        self.__heightSpinBox.setValue(currentGameLevel.get_fields_count_V())
        self.__widthSpinBox = QSpinBox()
        self.__widthSpinBox.setFixedSize(50, 20)
        self.__widthSpinBox.setMinimum(0)
        self.__widthSpinBox.setMaximum(99)
        self.__widthSpinBox.setValue(currentGameLevel.get_fields_count_H())
        self.__bombsCountSpinBox = QSpinBox()
        self.__bombsCountSpinBox.setFixedSize(50, 20)
        self.__bombsCountSpinBox.setMinimum(0)
        self.__bombsCountSpinBox.setMaximum(999)
        self.__bombsCountSpinBox.setValue(currentGameLevel.get_bombs_count())

        heightLayout.addStretch()
        heightLayout.addWidget(QLabel("Height:"))
        heightLayout.addWidget(self.__heightSpinBox)
        heightLayout.addStretch()
        widthLayout.addStretch()
        widthLayout.addWidget(QLabel("Width:"))
        widthLayout.addWidget(self.__widthSpinBox)
        widthLayout.addStretch()
        bombsCountLayout.addStretch()
        bombsCountLayout.addWidget(QLabel("Bombs:"))
        bombsCountLayout.addWidget(self.__bombsCountSpinBox)
        bombsCountLayout.addStretch()

        okButton = QPushButton("OK")
        okButton.clicked.connect(self.__confirm_dialog)
        cancelButton = QPushButton("Cancel")
        cancelButton.clicked.connect(self.close)

        inputLayout.addStretch()
        inputLayout.addLayout(heightLayout)
        inputLayout.addLayout(widthLayout)
        inputLayout.addLayout(bombsCountLayout)
        inputLayout.addStretch()

        buttonsLayout.addStretch()
        buttonsLayout.addWidget(okButton)
        buttonsLayout.addWidget(cancelButton)
        buttonsLayout.addStretch()

        mainLayout.addStretch()
        mainLayout.addLayout(inputLayout)
        mainLayout.addLayout(buttonsLayout)
        mainLayout.addStretch()

        self.setLayout(mainLayout)
        self.setWindowTitle("Custom Game")

    def __confirm_dialog(self):
        gameLevel: Level = Level(self.__widthSpinBox.value(), self.__heightSpinBox.value(),
                                 self.__bombsCountSpinBox.value())
        self.close()
        self.parent().setup_new_game(gameLevel)
