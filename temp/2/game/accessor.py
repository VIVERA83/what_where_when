# from game import BaseGameAccessor
from game.start_game import StartGame
from game.start_position import StartPosition


class MainGameAccessor(StartPosition, StartGame): ...
