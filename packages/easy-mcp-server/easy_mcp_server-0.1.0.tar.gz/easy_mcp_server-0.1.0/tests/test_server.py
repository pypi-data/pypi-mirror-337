import unittest
from unittest.mock import patch, MagicMock, ANY
from easy_mcp_server import DualTransportMCPServer, ServerSettings
from pydantic import ValidationError

class TestDualTransportMCPServer(unittest.TestCase):
    def setUp(self):
        # Define test tools as instance methods
        def test_tool_1(input_str: str) -> str:
            """A test tool that returns the input string."""
            return input_str

        def test_tool_2(a: int, b: int) -> int:
            """A test tool that adds two numbers."""
            return a + b
        
        def invalid_tool(x):
            # No docstring
            return x

        def invalid_tool_2(x):
            """Has docstring but missing return annotation."""
            pass
            
        self.test_tool_1 = test_tool_1
        self.test_tool_2 = test_tool_2
        self.invalid_tool = invalid_tool
        self.invalid_tool_2 = invalid_tool_2
    
    def test_valid_tools_registration(self):
        """Test valid tools are registered correctly."""
        server = DualTransportMCPServer([self.test_tool_1, self.test_tool_2])
        # We can't directly check the number of tools, so let's check the FastMCP instance exists
        self.assertIsNotNone(server.mcp)
    
    def test_invalid_tool_no_docstring(self):
        """Test tool without docstring raises error."""
        with self.assertRaises(ValidationError):
            DualTransportMCPServer([self.invalid_tool])
    
    def test_invalid_tool_no_return_type(self):
        """Test tool without return type annotation raises error."""
        with self.assertRaises(ValidationError):
            DualTransportMCPServer([self.invalid_tool_2])
    
    @patch('uvicorn.run')
    def test_run_sse_mode(self, mock_run):
        """Test running server in SSE mode."""
        settings = ServerSettings(transport="sse", port=8080)
        server = DualTransportMCPServer([self.test_tool_1], settings=settings)
        server.run()
        # Verify uvicorn.run was called
        mock_run.assert_called_once()
    
    @patch('mcp.server.fastmcp.FastMCP.run')
    def test_run_stdio_mode(self, mock_run):
        """Test running server in stdio mode."""
        settings = ServerSettings(transport="stdio")
        server = DualTransportMCPServer([self.test_tool_1], settings=settings)
        server.run()
        # Verify FastMCP.run was called
        mock_run.assert_called_once()

if __name__ == "__main__":
    unittest.main() 