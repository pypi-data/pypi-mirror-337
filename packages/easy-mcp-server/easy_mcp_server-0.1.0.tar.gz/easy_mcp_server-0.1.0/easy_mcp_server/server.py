from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from .settings import ServerSettings
from pydantic import BaseModel, Field, field_validator
from typing import Callable, Any, List
import click

class ToolSpec(BaseModel):
    """Specification for a valid MCP tool function."""
    func: Callable[..., Any] = Field(..., description="The tool function to validate")
    @field_validator("func")
    @classmethod
    def validate_function(cls, func):
        """Ensure the function has a docstring and return type annotation."""
        if not callable(func):
            raise ValueError("Tool must be a callable function")
        if not getattr(func, "__doc__", None):
            raise ValueError(f"Tool {func.__name__} must have a docstring")
        if not hasattr(func, "__annotations__") or "return" not in func.__annotations__:
            raise ValueError(f"Tool {func.__name__} must have a return type annotation")
        return func

class DualTransportMCPServer:
    """A class to create and run an MCP server with stdio or SSE transport."""
    def __init__(self, tools: List[Callable[..., Any]], settings: ServerSettings = ServerSettings()):
        """
        Initialize the MCP server with tools and settings.
        Args:
            tools: List of functions to register as MCP tools. Each must have a docstring and return type.
            settings: Pydantic model with transport and port settings (defaults to stdio, port 8000)
        """
        self.settings = settings
        self.app = FastAPI() if settings.transport == "sse" else None
        self.transport_obj = SseServerTransport(endpoint="/sse/") if settings.transport == "sse" else None
        self.server_name = "DynamicSSEServer" if settings.transport == "sse" else "DynamicStdioServer"
        self.mcp = FastMCP(self.server_name, transport=self.transport_obj)
        # Validate and register tools using Pydantic
        self._validate_and_register_tools(tools)

    def _validate_and_register_tools(self, tools: List[Callable[..., Any]]) -> None:
        """Validate and register tools using Pydantic."""
        for tool in tools:
            # Validate with Pydantic
            validated_tool = ToolSpec(func=tool)
            # Register the validated function
            self.mcp.tool()(validated_tool.func)

    def run(self):
        """Run the server based on the configured settings."""
        click.echo(f"Starting MCP server '{self.server_name}' in {self.settings.transport} mode...")
        if self.settings.transport == "sse":
            self.app.mount("/", self.mcp.sse_app())
            self.app.get("/health")(lambda: {"status": "ok"})
            import uvicorn
            uvicorn.run(self.app, host="0.0.0.0", port=self.settings.port)
        else:
            self.mcp.run()