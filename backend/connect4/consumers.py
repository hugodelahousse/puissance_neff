from dataclasses import dataclass, field
from typing import Optional, Dict

from connect4.game_consumer import GameConsumer
from connect4.game_logic import Board, BoardPlayer
from connect4.messages import (
    register_handler,
    UserJoinMessage,
    StartGameMessage,
    GameFullMessage,
    BoardStateMessage,
    PlayColumnMessage,
    YourTurnMessage,
    InvalidPlayMessage,
)


@dataclass
class Connect4GameState:
    game_uuid: Optional[str] = None
    players: Dict[int, str] = field(default_factory=dict)
    game_started: bool = False
    current_player: Optional[int] = None
    turn: int = 0
    board: Board = field(default_factory=Board)
    player_color: BoardPlayer = BoardPlayer.YELLOW


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

        if id(self) == self.game_state.current_player:
            self.game_state.player_color = BoardPlayer.YELLOW
            await self.send_message(YourTurnMessage())
        else:
            self.game_state.player_color = BoardPlayer.RED

    async def join_game(self, message):
        self.logger.debug(
            "Received join_game. Current players: %s", self.game_state.players
        )
        for id, username in self.game_state.players.items():
            self.logger.debug("Sending user id: %s username: %s", id, username)
            await self.group_send(
                {"type": "add_player", "player_id": id, "username": username}
            )

    async def play_position(self, message):
        self.game_state.board.set_position(
            message["row"], message["column"], message["color"]
        )

        # Ugly AF
        self.game_state.current_player = next(
            iter(set(self.game_state.players) - {self.game_state.current_player})
        )

        winner = message["color"] if message["winning_move"] else None

        await self.send_message(
            BoardStateMessage(board=self.game_state.board.to_list(), winner=winner)
        )

        if self.game_state.current_player == id(self):
            await self.send_message(YourTurnMessage())

    @register_handler(PlayColumnMessage)
    async def play_column(self, message: PlayColumnMessage):
        if id(self) != self.game_state.current_player:
            self.logger.info(
                "PlayColumn: Wrong player: expecting %s", self.game_state.current_player
            )
            return

        position, win = self.game_state.board.play(
            message.column, self.game_state.player_color
        )

        if not position:
            return await self.send_message(InvalidPlayMessage())

        row, column = position

        await self.group_send(
            {
                "type": "play_position",
                "row": row,
                "column": column,
                "color": self.game_state.player_color,
                "winning_move": win,
            }
        )
        self.logger.debug(self.game_state.board)
