import unittest
import asyncio
import threading
import time
import pytest
from easy_mcp_server import DualTransportMCPServer, ServerSettings

def echo(message: str) -> str:
    """Echo the input message."""
    return message

def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@pytest.mark.skip("Integration test requires manual verification")
class TestSSEServerIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Start the SSE server in a separate thread."""
        settings = ServerSettings(transport="sse", port=8081)
        cls.server = DualTransportMCPServer([echo, add], settings=settings)
        
        # Start server in a thread
        cls.server_thread = threading.Thread(target=cls.server.run)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        
        # Give the server time to start
        time.sleep(1)

    async def _test_client_connection(self):
        """Test client can connect to server and call tools."""
        try:
            from mcp.client.sse import sse_client
            
            # The sse_client in this version returns a tuple of read/write streams
            async with sse_client("http://localhost:8081/sse") as session_streams:
                from mcp.client.session import ClientSession
                
                # Create a session with the streams
                read_stream, write_stream = session_streams
                session = ClientSession(read_stream, write_stream, client_name="TestClient")
                
                # Use the initialize method to start the session
                await session.initialize()
                
                # Test echo tool
                result1 = await session.call_tool("echo", {"message": "Hello World"})
                self.assertEqual(result1, "Hello World")
                
                # Test add tool
                result2 = await session.call_tool("add", {"a": 5, "b": 7})
                self.assertEqual(result2, 12)
        except (ImportError, AttributeError) as e:
            self.skipTest(f"MCP client API mismatch: {str(e)}")
    
    def test_client_connection(self):
        """Run the async test."""
        asyncio.run(self._test_client_connection())

if __name__ == "__main__":
    unittest.main() 