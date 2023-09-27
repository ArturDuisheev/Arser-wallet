"""
ASGI config for project-wallet project-wallet.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from wallet.api import routing as wallet_routing

from users.middleware import BaseAuthMiddleware

django.setup()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project-wallet.settings')
application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": BaseAuthMiddleware(
        URLRouter(
            wallet_routing.websocket_urlpatterns
        )
    ),
})
