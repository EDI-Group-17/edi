from typing import Any, Dict, Optional
import httpx
from src.core.config import settings
from src.gateway.errors import build_jsonrpc_error

async def forward_mcp_request(
    payload: Dict[str, Any],
    http_client: Optional[httpx.AsyncClient] = None,
    target_url: Optional[str] = None
) -> Dict[str, Any]:
    url = target_url or settings.TARGET_MCP_URL
    req_id = payload.get("id")

    try:
        if http_client:
            response = await http_client.post(url, json=payload, timeout=5.0)
        else:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, timeout=5.0)
                
        if response.status_code == 200:
            return response.json()
        return build_jsonrpc_error(req_id, -32603, f"Target MCP Server Error: HTTP {response.status_code}")
    except Exception as exc:
        return build_jsonrpc_error(req_id, -32603, f"Target MCP Server Connection Error: {str(exc)}")
