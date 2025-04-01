"""
Pica API client for interacting with Pica OS.
"""

import json
import sys
from typing import Dict, List, Any, Optional, Union

import requests

from .models import (
    Connection, 
    ConnectionDefinition, 
    AvailableAction,
    ActionsResponse,
    PicaClientOptions
)
from .logger import get_logger, log_request_response
from .prompts import get_default_system_prompt, get_authkit_system_prompt, generate_full_system_prompt

logger = get_logger()

class PicaClient:
    """
    Client for interacting with the Pica API.
    """
    def __init__(self, secret: str, options: Optional[PicaClientOptions] = None):
        """
        Initialize the Pica client.
        
        Args:
            secret: The API secret for Pica.
            options: Optional configuration parameters.
                - server_url: Custom server URL to use instead of the default.
                - connectors: List of connector keys to filter by.
                - identity: Filter connections by specific identity ID.
                - identity_type: Filter connections by identity type (user, team, or organization).
                - authkit: Whether to use the AuthKit integration which enables the promptToConnectPlatform tool.
        """
        if not secret:
            logger.error("Pica API secret is required")
            print("ERROR: Pica API secret is required")
            sys.exit(1)
            
        self.secret = secret
        self.connections: List[Connection] = []
        self.connection_definitions: List[ConnectionDefinition] = []
        
        # Use default options if none provided
        options = options or PicaClientOptions()
        
        self.base_url = options.server_url
        logger.info(f"Initializing Pica client with base URL: {self.base_url}")
        
        self.get_connection_url = f"{self.base_url}/v1/vault/connections"
        self.available_actions_url = f"{self.base_url}/v1/knowledge"
        self.get_connection_definitions_url = f"{self.base_url}/v1/public/connection-definitions?limit=500"
        
        self._initialized = False
        self._connectors_filter = options.connectors
        if self._connectors_filter:
            logger.debug(f"Filtering connections by keys: {self._connectors_filter}")
            
        self._identity_filter = options.identity
        self._identity_type_filter = options.identity_type
        if self._identity_filter or self._identity_type_filter:
            logger.debug(f"Filtering connections by identity: {self._identity_filter}, type: {self._identity_type_filter}")
        
        self._use_authkit = options.authkit
        if self._use_authkit:
            logger.debug("Using AuthKit settings")
            self._system_prompt = get_authkit_system_prompt("Loading connections...")
        else:
            self._system_prompt = get_default_system_prompt("Loading connections...")
    
    def _initialize(self) -> None:
        """Initialize the client by fetching connections and connection definitions."""
        if self._initialized:
            logger.debug("Client already initialized, skipping initialization")
            return
        
        logger.info("Initializing Pica client connections and definitions")
        
        if self._connectors_filter and "*" in self._connectors_filter:
            logger.debug("Initializing all available connections")
            self._initialize_connections()
            self._connectors_filter = []
        elif self._connectors_filter:
            logger.debug(f"Initializing specific connections: {self._connectors_filter}")
            self._initialize_connections()
        else:
            logger.debug("No connections to initialize")
            self.connections = []
        
        self._initialize_connection_definitions()
        
        filtered_connections = [conn for conn in self.connections if conn.active]
        logger.debug(f"Found {len(filtered_connections)} active connections")
        
        if self._connectors_filter:
            filtered_connections = [
                conn for conn in filtered_connections 
                if conn.key in self._connectors_filter
            ]
            logger.debug(f"After filtering, {len(filtered_connections)} connections remain")
        
        connections_info = (
            "\t* " + "\n\t* ".join([
                f"{conn.platform} - Key: {conn.key}" 
                for conn in filtered_connections
            ])
            if filtered_connections 
            else "No connections available"
        )
        
        available_platforms_info = "\n\t* ".join([
            f"{def_.platform} ({def_.frontend.get('spec', {}).get('title', 'No Title')})"
            for def_ in self.connection_definitions
        ])
        
        if self._use_authkit:
            self._system_prompt = get_authkit_system_prompt(
                connections_info, 
                available_platforms_info
            )
        else:
            self._system_prompt = get_default_system_prompt(
                connections_info, 
                available_platforms_info
            )

        self._initialized = True
        logger.info("Pica client initialization complete")
    
    def _initialize_connections(self) -> None:
        """Fetch connections from the API."""
        try:
            logger.debug("Fetching connections from API")
            headers = self._generate_headers()
            
            query_params: Dict[str, Union[str, int]] = {"limit": 300}
            
            if self._identity_filter:
                query_params["identity"] = self._identity_filter
                
            if self._identity_type_filter:
                query_params["identityType"] = self._identity_type_filter
            
            url = self.get_connection_url
            log_request_response("GET", url, request_data=query_params)
            
            response = requests.get(url, headers=headers, params=query_params)
            response.raise_for_status()
            
            data = response.json()

            log_request_response("GET", url, 
                                response_status=response.status_code, 
                                response_data={"total": len(data.get("rows", []))})
            
            self.connections = [Connection(**conn) for conn in data.get("rows", [])]
            logger.info(f"Successfully fetched {len(self.connections)} connections")
        except Exception as e:
            logger.error(f"Failed to initialize connections: {e}", exc_info=True)
            print(f"Failed to initialize connections: {e}")
            self.connections = []
    
    def _initialize_connection_definitions(self) -> None:
        """Fetch connection definitions from the API."""
        try:
            logger.debug("Fetching connection definitions from API")
            headers = self._generate_headers()
            
            log_request_response("GET", self.get_connection_definitions_url)
            response = requests.get(self.get_connection_definitions_url, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            log_request_response("GET", self.get_connection_definitions_url, 
                                response_status=response.status_code, 
                                response_data={"total": len(data.get("rows", []))})
            
            self.connection_definitions = [
                ConnectionDefinition(**def_) 
                for def_ in data.get("rows", [])
            ]
            logger.info(f"Successfully fetched {len(self.connection_definitions)} connection definitions")
        except Exception as e:
            logger.error(f"Failed to initialize connection definitions: {e}", exc_info=True)
            print(f"Failed to initialize connection definitions: {e}")
            self.connection_definitions = []
    
    def _generate_headers(self) -> Dict[str, str]:
        """Generate headers for API requests."""
        return {
            "Content-Type": "application/json",
            "x-pica-secret": self.secret,
        }
    
    def generate_system_prompt(self, user_system_prompt: Optional[str] = None) -> str:
        """
        Generate a system prompt for use with LLMs.
        
        Args:
            user_system_prompt: Optional custom system prompt to prepend.
            
        Returns:
            The complete system prompt including Pica connection information.
        """
        if not self._initialized:
            self._initialize()
        
        return generate_full_system_prompt(self._system_prompt, user_system_prompt)
    
    @property
    def system(self) -> str:
        """Get the current system prompt."""
        return self._system_prompt
    
    def _paginate_results(
        self, 
        url: str, 
        params: Optional[Dict[str, Any]] = None, 
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Paginate through API results.
        
        Args:
            url: The API endpoint URL.
            params: Query parameters to include in the request.
            limit: The number of results to fetch per page.
            
        Returns:
            A list of all results.
        """
        params = params or {}
        skip = 0
        all_results = []
        total = 0
        
        try:
            while True:
                current_params = {
                    **params,
                    "skip": skip,
                    "limit": limit
                }

                response = requests.get(
                    url, 
                    params=current_params, 
                    headers=self._generate_headers()
                )
                response.raise_for_status()
                data = response.json()
                
                rows = data.get("rows", [])
                total = data.get("total", 0)
                all_results.extend(rows)
                
                skip += limit
                if len(all_results) >= total:
                    break
                
            return all_results
        except Exception as e:
            logger.error(f"Error in pagination: {e}")
            raise
    
    def get_connections(self) -> List[Connection]:
        """
        Get all available connections.
        
        Returns:
            A list of available connections.
        """
        if not self._initialized:
            self._initialize()
        
        return self.connections
    
    def get_all_available_actions(self, platform: str) -> List[AvailableAction]:
        """
        Get all available actions for a platform.
        
        Args:
            platform: The platform to get actions for.
            
        Returns:
            A list of available actions.
        """
        try:
            params = {
                "supported": "true",
                "connectionPlatform": platform
            }
            
            actions_data = self._paginate_results(
                self.available_actions_url,
                params=params
            )
            
            return [AvailableAction(**action) for action in actions_data]
        except Exception as e:
            logger.error(f"Error fetching all available actions: {e}")
            raise ValueError("Failed to fetch all available actions")
    
    def get_available_actions(self, platform: str) -> ActionsResponse:
        """
        Get available actions for a platform.
        
        Args:
            platform: The platform to get actions for.
            
        Returns:
            A response containing the available actions.
        """
        try:
            logger.info(f"Fetching available actions for platform: {platform}")
            all_actions = self.get_all_available_actions(platform)
            
            simplified_actions = [
                {
                    "_id": action._id if hasattr(action, "_id") else "",
                    "title": action.title,
                    "tags": action.tags
                }
                for action in all_actions
            ]
            
            logger.info(f"Found {len(simplified_actions)} available actions for {platform}")
            return ActionsResponse(
                success=True,
                data=simplified_actions,
                platform=platform,
                content=f"Found {len(simplified_actions)} available actions for {platform}"
            )
        except Exception as e:
            logger.error(f"Error fetching available actions for {platform}: {e}")
            return ActionsResponse(
                success=False,
                title="Failed to get available actions",
                message=str(e),
                raw=str(e)
            ) 