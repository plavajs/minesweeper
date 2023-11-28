from PyQt5.QtWidgets import QGridLayout

from field import Field
from level import Level


class Board(QGridLayout):

    def __init__(self, game, gameLevel: Level, **kwargs):
        super(Board, self).__init__(**kwargs)

        self.__game = game
        self.__gameLevel = gameLevel

        self.fields = self.__generate_fields()
        self.__load_neighbour_fields()
        self.regenerate_bombs()
        self.setSpacing(0)

    def get_fields_count_H_board(self):
        return self.__gameLevel.get_fields_count_H()

    def get_fields_count_V_board(self):
        return self.__gameLevel.get_fields_count_V()

    def get_rest_of_bombs(self):
        return self.__restOfBombs

    def get_fields(self):
        return self.fields

    def regenerate_bombs(self):
        self.__clean_bombs()
        self.__generate_bombs()
        self.__count_bombs()

    def field_left_clicked_board(self, field: Field):
        self.__game.field_left_clicked_game(field)

    def field_marked_bomb_board(self, marked: bool):
        self.__game.field_marked_bomb_game(marked)

    def check_non_bomb_fields_uncovered(self):
        for i in range(self.__gameLevel.get_fields_count_V()):
            for j in range(self.__gameLevel.get_fields_count_H()):
                field = self.fields[i][j]
                if not field.get_is_uncovered() and not field.get_is_bomb():
                    return False
        return True

    def __generate_fields(self):
        field_rows: list[list[Field]] = []
        for i in range(self.__gameLevel.get_fields_count_V()):
            field_row: list[Field] = []
            for j in range(self.__gameLevel.get_fields_count_H()):
                field_serial = i * self.__gameLevel.get_fields_count_V() + j + 1
                field = Field(field_serial, j, i, self)
                field_row.append(field)
                self.addWidget(field, i, j)
            field_rows.append(field_row)
        return field_rows

    def __load_neighbour_fields(self):
        for i in range(self.__gameLevel.get_fields_count_V()):
            for j in range(self.__gameLevel.get_fields_count_H()):
                self.fields[i][j].load_neighbour_fields()

    def __generate_bombs(self):
        import random as rnd
        self.__restOfBombs = 0
        while self.__restOfBombs < self.__gameLevel.get_bombs_count():
            rndI = rnd.randint(0, self.__gameLevel.get_fields_count_V() - 1)
            rndJ = rnd.randint(0, self.__gameLevel.get_fields_count_H() - 1)
            field = self.fields[rndI][rndJ]
            if not field.get_is_bomb():
                field.set_is_bomb(True)
                self.__restOfBombs += 1

    def __clean_bombs(self):
        for i in range(self.__gameLevel.get_fields_count_V()):
            for j in range(self.__gameLevel.get_fields_count_H()):
                self.fields[i][j].set_is_bomb(False)

    def __count_bombs(self):
        for i in range(self.__gameLevel.get_fields_count_V()):
            for j in range(self.__gameLevel.get_fields_count_H()):
                self.fields[i][j].count_neighbour_bombs()
