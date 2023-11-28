from PyQt5.QtWidgets import QMainWindow, QAction, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from customLevelDialog import CustomLevelDialog
from game import Game
from gameLevelUtilities import *
from imageLoaderUtilities import get_image_path
from level import Level


class MainWindow(QMainWindow):

    def __init__(self,  **kwargs):
        super(MainWindow, self).__init__(**kwargs)

        self.setWindowTitle("Minesweeper by Plavajs")
        self.__init_game(get_intermediate_game_level())
        self.__init_gui()
        self.show()
        self.setFixedSize(self.width(), self.height())

    def __init_gui(self):
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        self.setWindowIcon(QIcon(get_image_path("mine.png")))

        menuBar = self.menuBar()
        gameMenu = menuBar.addMenu("Game")
        newGameAction = QAction("New Game", self)
        beginnerAction = QAction("Beginner", self)
        beginnerAction.triggered.connect(lambda: self.setup_new_game(get_beginner_game_level()))
        intermediateAction = QAction("Intermediate", self)
        intermediateAction.triggered.connect(lambda: self.setup_new_game(get_intermediate_game_level()))
        expertAction = QAction("Expert", self)
        expertAction.triggered.connect(lambda: self.setup_new_game(get_expert_game_level()))
        customAction = QAction("Custom", self)
        customAction.triggered.connect(lambda: self.__open_custom_game_level_dialog())

        gameMenu.addAction(newGameAction)
        gameMenu.addSeparator()
        gameMenu.addAction(beginnerAction)
        gameMenu.addAction(intermediateAction)
        gameMenu.addAction(expertAction)
        gameMenu.addSeparator()
        gameMenu.addAction(customAction)

    def setup_new_game(self, gameLevel: Level):
        self.__init_game(gameLevel)
        self.setFixedSize(self.width(), self.height())

    def __init_game(self, gameLevel: Level):
        self.setFixedSize(0, 0)
        form = QWidget()
        formLayout = QVBoxLayout()
        form.setLayout(formLayout)
        self.__game = Game(gameLevel)

        formLayout.addStretch()
        formLayout.addLayout(self.__game)
        formLayout.addStretch()

        self.setCentralWidget(form)

    def __open_custom_game_level_dialog(self):
        dialogue = CustomLevelDialog(self, self.__game.get_game_level())
        dialogue.exec_()
