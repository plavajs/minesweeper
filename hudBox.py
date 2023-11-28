from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import QTimer

from level import Level


class HudBox(QHBoxLayout):

    def __init__(self, gameLevel: Level, **kwargs):
        super(HudBox, self).__init__(**kwargs)

        self.__gameLevel = gameLevel

        self.__init_gui()

    def __init_gui(self):
        self.__restOfBombsCountLabel = QLabel()
        self.set_bombs_count(self.__gameLevel.get_bombs_count())
        self.__restartButton = QPushButton("Restart")
        self.__timerLabel = QLabel("000.000")

        self.__timer = QTimer(self)
        self.__timer.timeout.connect(self.__update_time_counter)

        self.addWidget(self.__restOfBombsCountLabel)
        self.addStretch()
        self.addWidget(self.__restartButton)
        self.addStretch()
        self.addWidget(self.__timerLabel)

    def get_restart_button(self):
        return self.__restartButton

    def get_is_timer_running(self):
        return self.__timer.isActive()

    def set_bombs_count(self, count: int):
        countStr = str(count)
        if int(count / 10) == 0:
            countStr = f"00{count}"
        elif int(count / 100) == 0:
            countStr = f"0{count}"

        self.__restOfBombsCountLabel.setText(countStr)

    def increment_bombs_count(self):
        currentBombsCount = int(self.__restOfBombsCountLabel.text())
        self.set_bombs_count(currentBombsCount + 1)

    def decrement_bombs_count(self):
        currentBombsCount = int(self.__restOfBombsCountLabel.text())
        self.set_bombs_count(currentBombsCount - 1)

    def reset_timer(self):
        self.__timer.stop()
        self.__timerLabel.setText("000.000")

    def __update_time_counter(self):
        time = self.__timerLabel.text()
        milliseconds = round(float(time) + 0.001, 3)
        if milliseconds > 999.999:
            self.__timerLabel.setText(f"{999.999}")
        else:
            millisecondsStr = str(f"{milliseconds}")
            if int(milliseconds / 10) == 0:
                millisecondsStr = f"00{millisecondsStr}"
            elif int(milliseconds / 100) == 0:
                millisecondsStr = f"0{millisecondsStr}"

            if milliseconds * 1000 % 100 == 0:
                millisecondsStr = f"{millisecondsStr}00"
            elif milliseconds * 1000 % 10 == 0:
                millisecondsStr = f"{millisecondsStr}0"
            self.__timerLabel.setText(f"{millisecondsStr}")

    def start_timer(self):
        self.__timer.start(1)

    def stop_timer(self):
        self.__timer.stop()


