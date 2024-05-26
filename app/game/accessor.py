from game.players_setting import PlayersSettingPosition
from game.questions_setting import QuestionsSettingPosition
from game.start import StartPosition
from game.main_menu import MainMenuPosition
from game.wait_players import WaitPlayersPosition


class MainGameAccessor(
    StartPosition,  # начальная точка для всех пользователей
    MainMenuPosition,  # меню выбора режима игры, начать новую или присоединится
    QuestionsSettingPosition,  # выбрали начать новую, занимаемся настройкой кол-ва вопросов
    PlayersSettingPosition,  #
    WaitPlayersPosition,
):
    pass
