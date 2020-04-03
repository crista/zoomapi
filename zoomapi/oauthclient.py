"""Zoom.us REST API Python Client"""

from zoomapi import components, util
from zoomapi.client import ZoomClient

class OAuthZoomClient(ZoomClient):
    """Zoom.us REST API Python Client"""

    """Base URL for Zoom API"""

    def __init__(
        self, client_id, client_secret, port, redirect_url, browser_path, data_type="json", timeout=15
    ):
        """Create a new Zoom client

        :param client_id: The Zooom.us client id for this OAuth bot
        :param client_secret: The Zoom.us client secret for this OAuth bot
        :param data_type: The expected return data type. Either 'json' or 'xml'
        :param timeout: The time out to use for API requests
        """
        super(OAuthZoomClient, self).__init__(api_key=client_id, api_secret=client_secret, timeout=timeout)

        # Add the specific config details
        self.config["client_id"] = client_id
        self.config["client_secret"] = client_secret
        self.config["port"] = port
        self.config["redirect_url"] = redirect_url
        self.config["browser_path"] = browser_path
        self.config["token"] = util.get_oauth_token(client_id, client_secret, port, redirect_url, browser_path)

        self.components["chat_channels"] = components.chat_channels.ChatChannelsComponentV2
        self.components["chat_messages"] = components.chat_messages.ChatMessagesComponentV2

        # Instantiate the components
        for key in self.components.keys():
            self.components[key] = self.components[key](
                base_uri=self.BASE_URI, config=self.config
            )

    def refresh_token(self):
        self.config["token"] = util.get_oauth_token(self.config["client_id"], self.config["client_secret"], self.config["port"], self.config["redirect_url"], self.config["browser_path"])


    @property
    def redirect_url(self):
        """The Zoom.us OAuth redirect_url"""
        return self.config.get("redirect_url")

    @redirect_url.setter
    def redirect_url(self, value):
        """Set the redirect_url"""
        self.config["redirect_url"] = value
        self.refresh_token()

    @property
    def chat_messages(self):
        """Get the chat messages component"""
        return self.components.get("chat_messages")

    @property
    def chat_channels(self):
        """Get the chat messages component"""
        return self.components.get("chat_channels")
