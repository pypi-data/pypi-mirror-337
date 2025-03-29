import unittest
from pydantic import ValidationError
from easy_mcp_server import ServerSettings

class TestServerSettings(unittest.TestCase):
    def test_default_settings(self):
        """Test default settings are created correctly."""
        settings = ServerSettings()
        self.assertEqual(settings.transport, "stdio")
        self.assertEqual(settings.port, 8000)
    
    def test_custom_settings(self):
        """Test custom settings are created correctly."""
        settings = ServerSettings(transport="sse", port=8080)
        self.assertEqual(settings.transport, "sse")
        self.assertEqual(settings.port, 8080)
    
    def test_invalid_transport(self):
        """Test validation error on invalid transport."""
        with self.assertRaises(ValidationError):
            ServerSettings(transport="invalid")
    
    def test_invalid_port(self):
        """Test validation error on invalid port."""
        with self.assertRaises(ValidationError):
            ServerSettings(port=70000)  # Port must be ≤ 65535
        with self.assertRaises(ValidationError):
            ServerSettings(port=0)  # Port must be ≥ 1

if __name__ == "__main__":
    unittest.main() 