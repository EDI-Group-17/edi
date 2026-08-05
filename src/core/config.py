import os
from pydantic import BaseModel

class Settings(BaseModel):
    PROJECT_NAME: str = "AgentShield Security Gateway"
    VERSION: str = "1.0.0"
    HITL_TIMEOUT_SECONDS: int = 60
    TARGET_MCP_URL: str = "http://testserver/mock-mcp"
    HIGH_RISK_TOOLS: set[str] = {
        "fs.write_file",
        "fs.delete_file",
        "github.delete_repo",
        "db.execute_sql",
        "shell.execute",
        "exec",
        "delete_database"
    }
    RESTRICTED_PATHS: set[str] = {
        "/etc/passwd",
        "/etc/shadow",
        ".env",
        ".git"
    }

settings = Settings()
