from level import Level

__beginnerLevel = Level(10, 10, 10)
__intermediateLevel = Level(16, 16, 40)
__expertLevel = Level(30, 16, 99)


def get_beginner_game_level():
    return __beginnerLevel


def get_intermediate_game_level():
    return __intermediateLevel


def get_expert_game_level():
    return __expertLevel
