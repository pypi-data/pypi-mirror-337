"""
Logging utilities for the Pica API client.
"""

import logging
import sys
from typing import Any, Dict, Optional

def get_logger() -> logging.Logger:
    """
    Get a configured logger for the Pica client.
    
    Returns:
        A configured logger.
    """
    logger = logging.getLogger("pica-ai")
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

def log_request_response(
    method: str,
    url: str,
    request_data: Optional[Dict[str, Any]] = None,
    response_status: Optional[int] = None,
    response_data: Optional[Dict[str, Any]] = None,
    error: Optional[Exception] = None
) -> None:
    """
    Log API request and response details.
    
    Args:
        method: The HTTP method used.
        url: The URL of the request.
        request_data: Optional request data.
        response_status: Optional response status code.
        response_data: Optional response data.
        error: Optional exception if an error occurred.
    """
    logger = get_logger()
    if logger.level > logging.DEBUG:
        return
    
    # Mask sensitive data
    if request_data and isinstance(request_data, dict):
        # Make a copy to avoid modifying the original
        safe_request = request_data.copy() if hasattr(request_data, 'copy') else request_data
        
        # Mask sensitive fields
        if isinstance(safe_request, dict):
            for key in list(safe_request.keys()):
                if any(sensitive in key.lower() for sensitive in ["secret", "key", "token", "password", "auth"]):
                    safe_request[key] = "********"
                
                # Handle nested dictionaries
                if isinstance(safe_request[key], dict):
                    for nested_key in list(safe_request[key].keys()):
                        if any(sensitive in nested_key.lower() for sensitive in ["secret", "key", "token", "password", "auth"]):
                            safe_request[key][nested_key] = "********"
    else:
        safe_request = request_data
    
    log_parts = [
        f"API {method.upper()} {url}",
    ]
    
    if safe_request:
        log_parts.append(f"Request: {safe_request}")
    
    if response_status:
        log_parts.append(f"Response Status: {response_status}")
    
    if response_data:
        log_parts.append(f"Response Data: {response_data}")
    
    if error:
        log_parts.append(f"Error: {error}")
    
    logger.debug(" | ".join(log_parts)) 