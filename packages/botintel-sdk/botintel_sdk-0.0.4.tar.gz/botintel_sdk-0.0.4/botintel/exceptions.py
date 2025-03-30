class BotIntelError(Exception):
    """Base exception class for BotIntel SDK"""
    pass

class AuthenticationError(BotIntelError):
    """Invalid API key exception"""
    pass

class InsufficientBalanceError(BotIntelError):
    """Insufficient balance exception"""
    pass

class APIError(BotIntelError):
    """Generic API error exception"""
    pass

class ImageGenerationError(BotIntelError):
    """Exception related to image generation errors"""
    pass