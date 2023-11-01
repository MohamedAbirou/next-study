"""
ASGI config for nextstudy project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

# import os

# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.core.asgi import get_asgi_application
# import base.routing

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nextstudy.settings')
# django_asgi_app = get_asgi_application()

# application = ProtocolTypeRouter({
#     "http": django_asgi_app,
#     "websocket": URLRouter(
#         base.routing.websocket_urlpatterns
#     )
# })

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nextstudy.settings')

application = get_asgi_application()