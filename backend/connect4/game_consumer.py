from typing import ClassVar
import logging

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from connect4.messages import MessageHandler


class ConsumerLoggingAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return msg, {"extra": self.extra["consumer"].get_logger_data()}


class GameConsumer(AsyncJsonWebsocketConsumer, MessageHandler):
    GameStateClass: ClassVar

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_group_name = None
        self.game_state = self.GameStateClass()
        self.logger = ConsumerLoggingAdapter(
            logging.getLogger("connect4.consumers"), {"consumer": self}
        )

    async def group_send(self, *args, **kwargs):
        return await self.channel_layer.group_send(
            self.game_group_name, *args, **kwargs
        )

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.game_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive_json(self, content, **kwargs):
        await self.handle_message(content)
