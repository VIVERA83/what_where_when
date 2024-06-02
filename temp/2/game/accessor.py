# from game import BaseGameAccessor
from game.start_game import StartSingleGame
from game.start_position import StartPosition


class MainGameAccessor(StartPosition, StartSingleGame): ...
