from dataclasses import dataclass, asdict, field
from typing import Mapping, List, Callable, Tuple, Optional
from enum import Enum
from collections import defaultdict

from connect4.game_logic import BoardState, BoardPlayer


class MessageType(str, Enum):
    start_game = "start_game"
    game_full = "game_full"
    user_join = "user_join"
    play_column = "play_column"
    invalid_play = "invalid_play"
    player_win = "player_win"
    board_state = "board_state"
    your_turn = "your_turn"


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


@dataclass
class BoardStateMessage(Message):
    type = MessageType.board_state
    board: List[List[BoardState]]
    winner: Optional[BoardPlayer]


@dataclass
class YourTurnMessage(Message):
    type = MessageType.your_turn


@dataclass
class InvalidPlayMessage(Message):
    type = MessageType.invalid_play


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
            await handler(self, structure(**message))

    async def send_message(self, message: Message):
        await self.send_json(asdict(message))
