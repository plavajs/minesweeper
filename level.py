class Level:

    __minFieldsCountH = 9
    __maxFieldsCountH = 24
    __minFieldsCountV = 9
    __maxFieldsCountV = 24
    __minBombsCount = 10
    __maxBombDensity = 0.3

    def __init__(self, fieldsCountH: int, fieldsCountV: int, bombsCount: int):
        self.__fieldsCountH = 0
        self.__set_fields_count_H(fieldsCountH)
        self.__fieldsCountV = 0
        self.__set_fields_count_V(fieldsCountV)
        self.__bombsCount = 0
        self.__set_bombs_count(bombsCount)

    def __set_fields_count_H(self, fieldsCountH: int):
        if fieldsCountH > Level.__maxFieldsCountH:
            self.__fieldsCountH = Level.__maxFieldsCountH
        elif fieldsCountH < Level.__minFieldsCountH:
            self.__fieldsCountH = Level.__minFieldsCountH
        else:
            self.__fieldsCountH = fieldsCountH

    def get_fields_count_H(self):
        return self.__fieldsCountH

    def __set_fields_count_V(self, fieldsCountV: int):
        if fieldsCountV > Level.__maxFieldsCountV:
            self.__fieldsCountV = Level.__maxFieldsCountV
        elif fieldsCountV < Level.__minFieldsCountV:
            self.__fieldsCountV = Level.__minFieldsCountV
        else:
            self.__fieldsCountV = fieldsCountV

    def get_fields_count_V(self):
        return self.__fieldsCountV

    def __set_bombs_count(self, bombsCount: int):
        maxBombsCount = int(self.__fieldsCountH * self.__fieldsCountV * Level.__maxBombDensity)
        if bombsCount > maxBombsCount:
            self.__bombsCount = maxBombsCount
        elif bombsCount < Level.__minBombsCount:
            self.__bombsCount = Level.__minBombsCount
        else:
            self.__bombsCount = bombsCount

    def get_bombs_count(self):
        return self.__bombsCount
