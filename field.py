from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent

from buttonState import ButtonState
from imageLoaderUtilities import get_image_path


class Field(QPushButton):

    _width = 20
    _height = 20

    def __str__(self):
        return (f"Field(serial={self.__serial}, position=[{self.__positionV}, {self.__positionH}], "
                f"isBomb={self.__isBomb}")

    def __init__(self, serial, positionH: int, positionV: int, board, **kwargs):
        super(Field, self).__init__(**kwargs)
        self.setFixedSize(Field._width, Field._height)
        self.__serial = serial
        self.__positionH: int = positionH
        self.__positionV: int = positionV
        self.__board = board
        self.__isBomb = False
        self.__is_uncovered = False
        self.__neighbourFields: list[Field] = []
        self.__neighbourBombsCount: int = 0
        self.state = ButtonState.UNMARKED
        self.__init_gui()

    def reset(self):
        self.setStyleSheet(self.__get_normal_background_style())
        self.setChecked(False)
        self.setEnabled(True)
        self.__is_uncovered = False
        self.state = ButtonState.UNMARKED
        self.__neighbourBombsCount = 0
        self.setText("")

    def set_is_bomb(self, isBomb: bool):
        self.__isBomb = isBomb

    def get_is_bomb(self):
        return self.__isBomb

    def get_position_V(self):
        return self.__positionV

    def get_position_H(self):
        return self.__positionH

    def get_is_uncovered(self):
        return self.__is_uncovered

    def is_left_clickable(self):
        return self.state != ButtonState.MARKED_BOMB

    def load_neighbour_fields(self):
        deltas = [-1, 0, 1]
        for i in deltas:
            for j in deltas:
                if i == 0 and j == 0:
                    continue
                else:
                    neighbour = self.__get_neighbour(i, j)
                    if neighbour:
                        self.__neighbourFields.append(neighbour)

    def count_neighbour_bombs(self):
        count = 0
        for n in self.__neighbourFields:
            if n.get_is_bomb() and not self.__isBomb:
                count += 1
        self.__neighbourBombsCount = count

    def uncover(self, clicked: bool, blow: bool):
        self.set_uncovered_style(clicked, blow)
        self.__uncover_neighbours(blow)

    def set_uncovered_style(self, clicked: bool, blow: bool):
        if self.__isBomb:
            if blow:
                if clicked:
                    imagePath = get_image_path("mine_blow.png")
                else:
                    imagePath = get_image_path("mine.png")
            else:
                imagePath = get_image_path('mine_mark.png')

            style = f"background-image : url({imagePath}); background-position: center; background-repeat: no-repeat;"
        else:
            style = ""

        border_style = self.__get_border_style()
        style = style + border_style
        self.setStyleSheet(style)
        self.__is_uncovered = True
        text = "" if self.__neighbourBombsCount == 0 else str(self.__neighbourBombsCount)
        self.setText(text)
        self.setChecked(True)
        self.setEnabled(False)

    def eventFilter(self, obj, event: QMouseEvent):
        if obj == self and event.type() == 2:
            if event.button() == Qt.RightButton:
                self.__right_clicked()

        return super().eventFilter(obj, event)

    def __init_gui(self):
        self.reset()

        self.setCheckable(True)

        self.installEventFilter(self)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.clicked.connect(self.__left_clicked)

    def __left_clicked(self):
        self.__board.field_left_clicked_board(self)

    def __right_clicked(self):
        if not self.__is_uncovered:
            if self.state == ButtonState.MARKED_BOMB:
                self.state = ButtonState.MARKED_QUESTION
                self.__board.field_marked_bomb_board(False)
                self.setText("?")
                self.setStyleSheet(self.__get_normal_background_style() + " font-weight: bold;")
                self.setEnabled(True)
            elif self.state == ButtonState.MARKED_QUESTION:
                self.state = ButtonState.UNMARKED
                self.setText("")
                self.setStyleSheet(self.__get_normal_background_style())
            else:
                self.state = ButtonState.MARKED_BOMB
                self.__board.field_marked_bomb_board(True)
                self.setStyleSheet(f";{self.__get_border_style()} background-image : "
                                   f"url({get_image_path('mine_mark.png')}); background-position: center; "
                                   f"background-repeat: no-repeat;")
                self.setEnabled(False)

    def __get_normal_background_style(self):
        return "background-color: grey; color: black;"

    def __get_border_style(self):
        if self.__positionH == 0:
            leftBorderStyle = ""
        else:
            leftBorderStyle = " border-left: 0;"

        if self.__positionV == 0:
            topBorderStyle = ""
        else:
            topBorderStyle = " border-top: 0;"

        return f" border: 1px solid black;{leftBorderStyle}{topBorderStyle}"

    def __uncover_neighbours(self, blow: bool):
        if self.__neighbourBombsCount == 0 and not self.__isBomb:
            for n in self.__neighbourFields:
                if not n.__is_uncovered and not n.__isBomb:
                    n.uncover(False, blow)

    def __get_neighbour(self, deltaV, deltaH):
        neigbourPositionV = self.__positionV + deltaV
        neigbourPositionH = self.__positionH + deltaH

        if ((neigbourPositionV < 0 or neigbourPositionV > (self.__board.get_fields_count_V_board() - 1)) or
                (neigbourPositionH < 0 or neigbourPositionH > (self.__board.get_fields_count_H_board() - 1))):
            return None
        else:
            return self.__board.get_fields()[neigbourPositionV][neigbourPositionH]
