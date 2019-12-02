from dataclasses import dataclass
from typing import Optional, Dict

from connect4.game_consumer import GameConsumer
from connect4.messages import (
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


class Connect4Consumer(GameConsumer):
    GameStateClass = Connect4GameState

    async def connect(self):
        self.game_state.game_uuid = self.scope["url_route"]["kwargs"]["game_id"]
        self.game_group_name = "game_%s" % self.game_state.game_uuid

        self.logger.debug("Connecting to game room")
        # Join room group
        await self.channel_layer.group_add(self.game_group_name, self.channel_name)
        await self.group_send({"type": "join_game"})

        await self.accept()

    @register_handler(UserJoinMessage)
    async def user_join(self, message: UserJoinMessage):
        if len(self.game_state.players) > 1:
            self.logger.warning("Two players already connected, exiting")
            return await self.send_message(GameFullMessage())

        await self.group_send(
            {"type": "add_player", "player_id": id(self), "username": message.username}
        )

    async def add_player(self, message):
        player_id, username = message["player_id"], message["username"]
        if player_id in self.game_state.players:
            return

        if (
            player_id not in self.game_state.players
            and len(self.game_state.players) > 1
        ):
            self.logger.warning(
                "Received add_player but two players are already present, skipping..."
            )
            return

        self.logger.debug("Setting %s to username: %s", player_id, username)
        self.game_state.players[player_id] = username

        self.logger.debug("Current players: %s", self.game_state.players)

        # Only one of the sockets sends the start game message
        if len(self.game_state.players) > 1 and id(self) == player_id:
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
