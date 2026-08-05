from typing import Any, Dict
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

mock_mcp_app = FastAPI(title="Mock MCP Target Server")

@mock_mcp_app.post("/mock-mcp")
async def handle_mock_mcp(payload: Dict[str, Any]):
    req_id = payload.get("id")
    method = payload.get("method")
    
    if method == "resources/read":
        return JSONResponse(status_code=status.HTTP_200_OK, content={
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "contents": [{"uri": "file:///docs/readme.txt", "text": "Mock target server content"}]
            }
        })
    elif method == "tools/call":
        params = payload.get("params", {})
        tool_name = params.get("name")
        if tool_name == "get_user_info":
            return JSONResponse(status_code=status.HTTP_200_OK, content={
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "user": "Harsh",
                    "aws_key": "AKIAIOSFODNN7EXAMPLE",
                    "aadhaar": "3675 8392 0192",
                    "pan": "ABCDE1234F"
                }
            })

        return JSONResponse(status_code=status.HTTP_200_OK, content={
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "content": [{"type": "text", "text": f"Executed mock tool {tool_name}"}]
            }
        })
        
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        "jsonrpc": "2.0",
        "id": req_id,
        "result": {"status": "mock_success"}
    })
