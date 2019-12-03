import asyncio
from dataclasses import asdict

import pytest
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from connect4.messages import UserJoinMessage, MessageType, PlayColumnMessage
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


@pytest.mark.asyncio
async def test_moves():

    player1, player2 = await connect_players("game3")

    current_player = None
    try:
        await player1.receive_json_from()
        current_player = player1
    except TimeoutError:
        pass

    if current_player is None:
        await player2.receive_json_from()
        current_player = player2

    def switch_players():
        return player1 if current_player is player2 else player2

    await current_player.send_message_to(PlayColumnMessage(column=1))
    await current_player.receive_json_from()

    current_player = switch_players()

    await current_player.send_message_to(PlayColumnMessage(column=1))
    await current_player.receive_json_from()

    current_player = switch_players()

    await current_player.send_message_to(PlayColumnMessage(column=1))
    await current_player.receive_json_from()
