import requests
from . import exceptions
from .models import ImageGeneration

class ImageClient:
    def __init__(self, api_key: str, base_url: str = "https://bix-api.onrender.com/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User -Agent": "BotIntel-Python-SDK/1.0"
        })

    def generations(self):
        return ImageGenerationHandler(self)

class ImageGenerationHandler:
    def __init__(self, client: ImageClient):
        self.client = client

    def create(self, model: str, prompt: str, resolution: str = "1024x1024", **kwargs):
        if model not in ["imagen-1", "imagen-2"]:  # Add valid models as needed
            raise ValueError("Invalid model provided.")
        
        url = f"{self.client.base_url}/images/generations"
        data = {
            "model": model,
            "prompt": prompt,
            "resolution": resolution,
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

        # Initialize ImageGeneration with the response data
        response_data = response.json()
        return ImageGeneration(url=response_data.get("url"))  # Adjust based on actual response structure