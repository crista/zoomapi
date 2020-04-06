"""Zoom.us REST API Python Client -- Chat Messages component"""

from zoomapi.util import Throttled
from zoomapi.components import base

class ChatChannelsComponentV2(base.BaseComponent):
    """Component dealing with all chat channels related matters"""

    @Throttled
    def list(self, **kwargs):
        return self.get_request("/chat/users/me/channels")

