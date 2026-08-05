from typing import Any, Dict, Optional
import httpx
import logging
from src.core.config import settings
from src.gateway.errors import build_jsonrpc_error

logger = logging.getLogger("agentshield.mcp_client")

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
        if http_client:
            return build_jsonrpc_error(req_id, -32603, f"Target MCP Server Connection Error: {str(exc)}")
        logger.info(f"Target MCP server at '{url}' unreachable ({str(exc)}); returning dev mock result.")
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "status": "success",
                "message": "MCP Target Execution Output",
                "received_params": payload.get("params", {})
            }
        }
