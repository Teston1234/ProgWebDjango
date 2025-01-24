from django.urls import re_path
from . import consumers
from .consumers import SalonConsumer
websocket_urlpatterns = [
    re_path(r'ws/salon/(?P<salon_id>\d+)/$', consumers.SalonConsumer.as_asgi()),


]
