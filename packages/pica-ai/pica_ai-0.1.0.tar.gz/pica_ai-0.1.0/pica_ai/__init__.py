"""
Pica-AI: Client for interacting with the Pica API.

This package provides tools for getting connections, actions, and system prompts for Pica.
"""

from .client import PicaClient
from .models import PicaClientOptions

__version__ = "0.1.0"
__all__ = ["PicaClient", "PicaClientOptions"] 