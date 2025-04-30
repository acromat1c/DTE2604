import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import programmingCourse.routing  


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            programmingCourse.routing.websocket_urlpatterns
        )
    ),
})

ASGI_APPLICATION = 'mysite.asgi.application'