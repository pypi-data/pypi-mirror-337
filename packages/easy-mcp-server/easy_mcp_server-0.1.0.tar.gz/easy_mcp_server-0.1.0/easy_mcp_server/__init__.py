
# easy_mcp_server/__init__.py
from .server import DualTransportMCPServer
from .settings import ServerSettings

__version__ = "0.1.0"
__all__ = ["DualTransportMCPServer", "ServerSettings"]