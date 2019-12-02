from channels.routing import ProtocolTypeRouter, URLRouter
import connect4.routing

application = ProtocolTypeRouter(
    {"websocket": URLRouter(connect4.routing.websocket_urlpatterns)}
)
