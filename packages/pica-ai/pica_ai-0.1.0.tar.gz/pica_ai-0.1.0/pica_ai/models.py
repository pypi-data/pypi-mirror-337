"""
Data models for the Pica API client.
"""

from typing import Dict, List, Any, Optional, Union, Literal
from pydantic import BaseModel, Field, ConfigDict

class PicaClientOptions(BaseModel):
    """Configuration options for the Pica client."""
    server_url: str = Field(
        default="https://api.picaos.com",
        description="Custom server URL to use instead of the default"
    )
    connectors: List[str] = Field(
        default_factory=list,
        description="List of connector keys to filter by. Use [\"*\"] to initialize all connections."
    )
    identity: Optional[str] = Field(
        default=None,
        description="Filter connections by specific identity ID"
    )
    identity_type: Optional[Literal["user", "team", "organization"]] = Field(
        default=None,
        description="Filter connections by identity type (user, team, or organization)"
    )
    authkit: bool = Field(
        default=False,
        description="Whether to use the AuthKit integration which enables the promptToConnectPlatform tool"
    )
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

class Connection(BaseModel):
    """A Pica connection."""
    _id: str
    key: str
    platform: str
    active: bool = True
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

class ConnectionDefinition(BaseModel):
    """A Pica connection definition."""
    _id: str
    platform: str
    frontend: Any
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

class AvailableAction(BaseModel):
    """An available action on a platform."""
    _id: str 
    title: str
    tags: List[str] = []
    path: Optional[str] = None
    knowledge: Optional[Any] = None
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

class BaseResponse(BaseModel):
    """Base class for API responses."""
    success: bool
    title: Optional[str] = None
    message: Optional[str] = None
    raw: Optional[Any] = None
    content: Optional[str] = None
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

class ActionsResponse(BaseResponse):
    """Response for available actions."""
    data: List[Dict[str, Any]] = []
    platform: Optional[str] = None 