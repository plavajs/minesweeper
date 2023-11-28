from PyQt5.QtWidgets import QVBoxLayout, QLabel

from board import Board
from endGameDialog import EndGameDialog
from field import Field
from hudBox import HudBox
from level import Level


class Game(QVBoxLayout):

    def __init__(self, gameLevel: Level, **kwargs):
        super(Game, self).__init__(**kwargs)

        self.__gameLevel = gameLevel

        self.__init_gui()

    def get_game_level(self):
        return self.__gameLevel

    def restart_button_clicked(self):
        self.__hudBox.reset_timer()
        self.__hudBox.set_bombs_count(self.__board.get_rest_of_bombs())
        fields = self.__board.get_fields()
        for i in range(self.__gameLevel.get_fields_count_V()):
            for j in range(self.__gameLevel.get_fields_count_H()):
                fields[i][j].reset()

        self.__board.regenerate_bombs()

    def field_left_clicked_game(self, clickedField: Field):
        if clickedField.is_left_clickable():
            isBomb = clickedField.get_is_bomb()
            clickedField.uncover(True, isBomb)

            if not self.__hudBox.get_is_timer_running():
                self.__hudBox.start_timer()

            if isBomb:
                self.__hudBox.stop_timer()
                self.__uncover_all_fields(clickedField, isBomb)
                endDialog = EndGameDialog(False)
                endDialog.exec_()

            elif self.__board.check_non_bomb_fields_uncovered():
                self.__hudBox.stop_timer()
                self.__uncover_all_fields(clickedField, isBomb)
                endDialog = EndGameDialog(True)
                endDialog.exec_()

    def __init_gui(self):
        self.__board = Board(self, self.__gameLevel)
        self.__hudBox = HudBox(self.__gameLevel)

        self.addStretch()
        self.addLayout(self.__hudBox)
        self.addLayout(self.__board)
        self.addStretch()

        self.__hudBox.get_restart_button().clicked.connect(self.restart_button_clicked)

    def __uncover_all_fields(self, clickedField: Field, blow: bool):
        fields = self.__board.get_fields()
        for i in range(len(fields)):
            fields_row = fields[i]
            for j in range(len(fields_row)):
                if not (i == clickedField.get_position_V() and j == clickedField.get_position_H()):
                    fields[i][j].set_uncovered_style(False, blow)

    def field_marked_bomb_game(self, marked: bool):
        self.__hudBox.decrement_bombs_count() if marked else self.__hudBox.increment_bombs_count()
