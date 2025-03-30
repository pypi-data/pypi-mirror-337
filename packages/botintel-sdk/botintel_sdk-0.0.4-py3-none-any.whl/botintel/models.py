from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Message:
    role: str
    content: str

@dataclass
class Choice:
    message: Message
    finish_reason: str

@dataclass
class Usage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

@dataclass
class ChatCompletion:
    id: str
    object: str
    created: int
    model: str
    choices: List[Choice]
    usage: Usage
    
    def __str__(self):
        return self.choices[0].message.content if self.choices else ""

@dataclass
class ImageGeneration:
    url: Optional[str]  # URL of the generated image
    # Add other fields as necessary