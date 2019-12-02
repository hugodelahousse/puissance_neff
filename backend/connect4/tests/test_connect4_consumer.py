import asyncio
from dataclasses import asdict

import pytest
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from connect4.messages import UserJoinMessage, MessageType
from connect4.routing import websocket_urlpatterns


class MessageWebsocketCommunicator(WebsocketCommunicator):
    async def send_message_to(self, message):
        return await self.send_json_to(asdict(message))


async def connect_players(game_id, username1="player1", username2="player2"):
    application = URLRouter(websocket_urlpatterns)
    player1 = MessageWebsocketCommunicator(application, f"ws/game/{game_id}/")
    player2 = MessageWebsocketCommunicator(application, f"ws/game/{game_id}/")

    connected, _ = await player1.connect()
    connected, _ = await player2.connect()

    assert connected
    await player1.send_message_to(UserJoinMessage(username="player1"))

    assert connected
    await player2.send_message_to(UserJoinMessage(username="player2"))

    assert (await player1.receive_json_from())["type"] == MessageType.start_game
    assert (await player2.receive_json_from())["type"] == MessageType.start_game

    return player1, player2


@pytest.mark.asyncio
async def test_connection():
    await connect_players("game1")


@pytest.mark.asyncio
async def test_three_players_fail():
    player1, player2 = await connect_players("game2")

    application = URLRouter(websocket_urlpatterns)
    player3 = MessageWebsocketCommunicator(application, "ws/game/game2/")

    connected, _ = await player3.connect()
    assert connected

    await asyncio.sleep(0.2)
    await player3.send_message_to(UserJoinMessage(username="player3"))

    assert (await player3.receive_json_from())["type"] == MessageType.game_full
