import re

from game import BaseGameAccessor, UserState, check_cache


class TextAccessor(BaseGameAccessor):
    def init(self):
        self.add_text_event_handler(self.start, "start")  # noqa
        self.add_regex_text_event_handler(self.text_handler, re.compile(r".*"))

    @check_cache
    async def text_handler(self, user_state: UserState, *_, **__) -> UserState:
        print("text_handler", user_state)
        return user_state
