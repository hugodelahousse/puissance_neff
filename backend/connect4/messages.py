from dataclasses import dataclass, asdict, field
from typing import Mapping, List, Callable, Tuple
from enum import Enum
from collections import defaultdict


class MessageType(str, Enum):
    start_game = "start_game"
    game_full = "game_full"
    user_join = "user_join"
    play_column = "play_column"
    invalid_play = "invalid_play"
    player_win = "player_win"


@dataclass
class Message:
    type: MessageType = field(init=False)


@dataclass
class UserJoinMessage(Message):
    type = MessageType.user_join
    username: str


@dataclass
class PlayColumnMessage(Message):
    type = MessageType.play_column
    column: int


@dataclass
class StartGameMessage(Message):
    type = MessageType.start_game
    first_player: bool


@dataclass
class GameFullMessage(Message):
    type = MessageType.game_full


HANDLERS: Mapping[MessageType, List[Tuple[Callable, Message]]] = defaultdict(list)


def register_handler(message_type: Message):
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

    async def send_message(self, message: Message):
        await self.send_json(asdict(message))
