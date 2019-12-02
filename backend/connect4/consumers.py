from typing import Mapping
from channels.generic.websocket import AsyncJsonWebsocketConsumer
import logging as _logging

from connect4.messages import (
    MessageHandler,
    register_handler,
    UserJoinMessage,
    StartGameMessage,
    PlayColumnMessage,
)


class Connect4Consumer(MessageHandler, AsyncJsonWebsocketConsumer):
    logger = _logging.getLogger("connect4.consumers")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_name = None
        self.room_group_name = None
        self.players: Mapping[int, str] = {}
        self.game_started = False
        self.current_player = None

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["game_id"]
        self.room_group_name = "game_%s" % self.room_name

        self.logger.debug("Connecting to game room: %s", self.room_group_name)
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive_json(self, content, **kwargs):
        await self.handle_message(content)

    @register_handler(UserJoinMessage)
    async def user_join(self, message: UserJoinMessage):
        if len(self.players) > 1:
            self.logger.warning("Two players already connected, exiting")
            await self.close()
            return

        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "add_player", "player_id": id(self), "username": message.username},
        )

    async def add_player(self, message):
        self.logger.debug(
            "Setting %s to username: %s", message["player_id"], message["username"]
        )
        self.players[message["player_id"]] = message["username"]

        self.logger.debug("Current players: %s", self.players)

        # Only one of the sockets sends the start game message
        if len(self.players) > 1 and id(self) == message["player_id"]:
            self.logger.debug("Sending start game message")
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "start_game", "first_player_id": list(self.players.keys())[0]},
            )

    async def start_game(self, message):
        self.logger.debug("Starting game")
        self.current_player = message["first_player_id"]
        await self.send_message(
            StartGameMessage(first_player=id(self) == message["first_player_id"])
        )
