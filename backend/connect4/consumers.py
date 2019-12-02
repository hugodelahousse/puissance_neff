from dataclasses import dataclass
from typing import Mapping, Optional, Dict
from channels.generic.websocket import AsyncJsonWebsocketConsumer
import logging as _logging

from connect4.messages import (
    MessageHandler,
    register_handler,
    UserJoinMessage,
    StartGameMessage,
    GameFullMessage,
)


@dataclass
class Connect4GameState:
    game_uuid: Optional[str]
    players: Dict[int, str]
    game_started: bool
    current_player: Optional[int]
    turn: int
    board: None


class ConsumerLoggingAdapter(_logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return msg, {"extra": self.extra["consumer"].get_logger_data()}


class Connect4Consumer(MessageHandler, AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_group_name = None
        self.game_state: Connect4GameState = Connect4GameState(
            game_uuid=None,
            players={},
            game_started=False,
            current_player=None,
            turn=0,
            board=None,
        )
        self.logger = ConsumerLoggingAdapter(
            _logging.getLogger("connect4.consumers"), {"consumer": self}
        )

    def get_logger_data(self):
        return {"socket_id": id(self), "room_name": self.room_group_name}

    async def group_send(self, *args, **kwargs):
        return await self.channel_layer.group_send(
            self.room_group_name, *args, **kwargs
        )

    async def connect(self):
        self.game_state.game_uuid = self.scope["url_route"]["kwargs"]["game_id"]
        self.room_group_name = "game_%s" % self.game_state.game_uuid

        self.logger.debug("Connecting to game room: %s", self.room_group_name)
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.group_send({"type": "join_game"})

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive_json(self, content, **kwargs):
        await self.handle_message(content)

    @register_handler(UserJoinMessage)
    async def user_join(self, message: UserJoinMessage):
        if len(self.game_state.players) > 1:
            self.logger.warning("Two players already connected, exiting")
            return await self.send_message(GameFullMessage())

        await self.group_send(
            {"type": "add_player", "player_id": id(self), "username": message.username}
        )

    async def add_player(self, message):
        self.logger.debug(
            "Setting %s to username: %s", message["player_id"], message["username"]
        )
        self.game_state.players[message["player_id"]] = message["username"]

        self.logger.debug("Current players: %s", self.game_state.players)

        # Only one of the sockets sends the start game message
        if len(self.game_state.players) > 1 and id(self) == message["player_id"]:
            self.logger.debug("Sending start game message")
            await self.group_send(
                {
                    "type": "start_game",
                    "first_player_id": list(self.game_state.players.keys())[0],
                }
            )

    async def start_game(self, message):
        self.logger.debug("Starting game")
        self.game_state.current_player = message["first_player_id"]
        await self.send_message(
            StartGameMessage(first_player=id(self) == message["first_player_id"])
        )

    async def join_game(self, message):
        self.logger.debug(
            "Received join_game. Current players: %s", self.game_state.players
        )
        for id, username in self.game_state.players.items():
            self.logger.debug("Sending user id: %s username: %s", id, username)
            await self.group_send(
                {"type": "add_player", "player_id": id, "username": username}
            )
