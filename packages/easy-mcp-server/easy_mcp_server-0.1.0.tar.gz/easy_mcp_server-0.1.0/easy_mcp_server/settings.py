from pydantic import BaseModel, Field

class ServerSettings(BaseModel):
    transport: str = Field(default="stdio", pattern="^(stdio|sse)$", description="Transport mode: 'stdio' or 'sse'")
    port: int = Field(default=8000, ge=1, le=65535, description="Port for SSE mode")