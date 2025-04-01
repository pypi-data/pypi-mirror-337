"""
Tests for the PicaClient class.
"""

import unittest
from unittest.mock import patch, MagicMock
from pica_ai import PicaClient
from pica_ai.models import Connection

class TestPicaClient(unittest.TestCase):
    """Test cases for the PicaClient class."""
    
    @patch('pica_ai.client.requests')
    def test_get_connections(self, mock_requests):
        """Test that get_connections returns a list of connections."""

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "rows": [
                {
                    "_id": "conn1",
                    "key": "connection-key-1",
                    "platform": "gmail",
                    "active": True
                },
                {
                    "_id": "conn2",
                    "key": "connection-key-2",
                    "platform": "slack",
                    "active": True
                }
            ]
        }
        mock_response.status_code = 200
        mock_requests.get.return_value = mock_response
        
        client = PicaClient(secret="test-secret")
        client._initialized = True
        client.connections = [
            Connection(_id="conn1", key="connection-key-1", platform="gmail", active=True),
            Connection(_id="conn2", key="connection-key-2", platform="slack", active=True)
        ]
        
        connections = client.get_connections()
        
        self.assertEqual(len(connections), 2)
        self.assertEqual(connections[0].platform, "gmail")
        self.assertEqual(connections[1].platform, "slack")
    
    @patch('pica_ai.client.requests')
    def test_generate_system_prompt(self, mock_requests):
        """Test that generate_system_prompt returns a string."""

        client = PicaClient(secret="test-secret")
        client._initialized = True  # Skip initialization
        client._system_prompt = "Test system prompt"
        
        prompt = client.generate_system_prompt()
        
        self.assertIsInstance(prompt, str)
        self.assertEqual(prompt, "Test system prompt")
        
        user_prompt = "User system prompt"
        prompt = client.generate_system_prompt(user_prompt)
        
        self.assertIn(user_prompt, prompt)
        self.assertIn("Test system prompt", prompt)

if __name__ == '__main__':
    unittest.main() 