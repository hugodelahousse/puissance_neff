from dataclasses import dataclass, asdict
from typing import Mapping, List, Callable, ClassVar, Any, Tuple
from enum import Enum
from collections import defaultdict


class MessageType(str, Enum):
    start_game = "start_game"
    user_join = "user_join"
    play_column = "play_column"
    invalid_play = "invalid_play"
    player_win = "player_win"


@dataclass
class UserJoinMessage:
    type = MessageType.user_join
    username: str


@dataclass
class PlayColumnMessage:
    type = MessageType.play_column
    column: int


@dataclass
class StartGameMessage:
    type = MessageType.start_game
    first_player: bool


HANDLERS: Mapping[MessageType, List[Tuple[Callable, Any]]] = defaultdict(list)


def register_handler(message_type):
    def inner(func):
        HANDLERS[message_type.type.value].append((func, message_type))
        return func

    return inner


class MessageHandler:
    async def handle_message(self, message):
        message_type = message.pop("type")
        handlers = HANDLERS.get(message_type, [])
        if not handlers:
            self.logger.warning("No handlers found for message: %s", message)

        self.logger.debug("Received message: %s", message)

        for handler, structure in handlers:
            try:
                await handler(self, structure(**message))
            except Exception as e:
                self.logger.exception(e)
                await self.close()

    async def send_message(self, message):
        await self.send_json(asdict(message))
