import requests
from . import exceptions
from .models import ChatCompletion

class Client:
    def __init__(self, api_key: str, base_url: str = "https://bix-api.onrender.com/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User -Agent": "BotIntel-Python-SDK/1.0"
        })
    
    def chat(self):
        return ChatCompletionHandler(self)

import requests
from . import exceptions
from .models import ChatCompletion, Choice, Message, Usage

class Client:
    def __init__(self, api_key: str, base_url: str = "https://bix-api.onrender.com/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User -Agent": "BotIntel-Python-SDK/1.0"
        })
    
    def chat(self):
        return ChatCompletionHandler(self)

class ChatCompletionHandler:
    def __init__(self, client: Client):
        self.client = client
    
    def create(self, model: str, messages: list, temperature: float = 0.7, 
               max_tokens: int = 500, **kwargs):
        url = f"{self.client.base_url}/chat/completions"
        data = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            **kwargs
        }
        
        response = self.client.session.post(url, json=data)
        
        if response.status_code == 401:
            raise exceptions.AuthenticationError("Invalid API key")
        if response.status_code == 402:
            raise exceptions.InsufficientBalanceError("Insufficient balance")
        if response.status_code == 404:
            raise exceptions.APIError("Endpoint not found. Check the URL.")
        if not response.ok:
            raise exceptions.APIError(f"API Error: {response.text}")
        
        # Initialize ChatCompletion with the response data
        response_data = response.json()
        choices = [Choice(message=Message(**choice['message']), finish_reason=choice['finish_reason']) for choice in response_data['choices']]
        return ChatCompletion(
            id=response_data['id'],
            object=response_data['object'],
            created=response_data['created'],
            model=response_data['model'],
            choices=choices,
            usage=Usage(**response_data['usage'])
        )  # Ensure correct unpacking of response
