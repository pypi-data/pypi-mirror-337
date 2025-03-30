# reicore_sdk/sdk.py
import requests

class ReiSdk:
    """
    Rei Agent SDK for interacting with the Rei Agent API.
    """

    def __init__(self, agent_key: str):
        """
        Initializes the ReiSdk with an API key.

        :param agent_key: The API key for authentication.
        """
        self.agent_key = agent_key
        self.base_url = "https://api.reisearch.box/rei"  # Replace with actual API URL

    def get_agent(self):
        """
        Retrieves details about the Rei Agent.

        :return: A dictionary containing agent details.
        """
        url = f"{self.base_url}/agents"
        headers = {"x-rei-agent-key": f"{self.agent_key}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()

    def chat_completions(self, payload: dict):
        """
        Sends a message to the Rei Agent and receives a chat completion.

        :param payload: The chat completion payload to send.
        :return: A dictionary containing the chat completion response.
        """
        url = f"{self.base_url}/agents/chat-completion"
        headers = {"x-rei-agent-key": f"{self.agent_key}"}
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()