import pytest
from src.sanitizer.pii_engine import sanitize_payload

def test_sanitize_api_keys():
    text = "Here is my key AKIAIOSFODNN7EXAMPLE and OpenAI sk-proj-9999999999999999 and GitHub ghp_1234567890abcdefghijklmnopqrstuvwxyz"
    sanitized = sanitize_payload(text)
    assert "AKIAIOSFODNN7EXAMPLE" not in sanitized
    assert "sk-proj-" not in sanitized
    assert "ghp_" not in sanitized
    assert "[REDACTED: API_KEY]" in sanitized

def test_sanitize_aadhaar_number():
    text = "User Aadhaar is 3675 8392 0192 and alternate 3675-8392-0192"
    sanitized = sanitize_payload(text)
    assert "3675 8392 0192" not in sanitized
    assert "3675-8392-0192" not in sanitized
    assert "[REDACTED: AADHAAR_NUMBER]" in sanitized

def test_sanitize_pan_number():
    text = "Taxpayer PAN is ABCDE1234F for user Harsh"
    sanitized = sanitize_payload(text)
    assert "ABCDE1234F" not in sanitized
    assert "[REDACTED: PAN_NUMBER]" in sanitized

def test_sanitize_credit_card():
    text = "Card number 4532 0151 8293 4810 expires 12/28"
    sanitized = sanitize_payload(text)
    assert "4532 0151 8293 4810" not in sanitized
    assert "[REDACTED: CREDIT_CARD]" in sanitized

def test_sanitize_password_secret():
    payload = {"user": "admin", "password": "SuperSecretPassword123!", "token": "Bearer xyz"}
    sanitized = sanitize_payload(payload)
    assert sanitized["password"] == "[REDACTED: SECRET]"
    assert sanitized["user"] == "admin"

def test_sanitize_nested_dict_json():
    payload = {
        "status": "success",
        "data": {
            "user_info": {
                "pan": "XYZPA9876Q",
                "aadhaar": "9876 5432 1098"
            }
        }
    }
    sanitized = sanitize_payload(payload)
    assert sanitized["data"]["user_info"]["pan"] == "[REDACTED: PAN_NUMBER]"
    assert sanitized["data"]["user_info"]["aadhaar"] == "[REDACTED: AADHAAR_NUMBER]"

def test_sanitize_dict_key_pii():
    payload = {"AKIAIOSFODNN7EXAMPLE": "leaked_key_as_dict_key"}
    sanitized = sanitize_payload(payload)
    assert "[REDACTED: API_KEY]" in sanitized
    assert "AKIAIOSFODNN7EXAMPLE" not in sanitized

def test_sanitize_deeply_nested_mixed_payload():
    payload = {
        "level1": [
            {
                "level2": (
                    {
                        "level3": {
                            "keys": ["AKIAIOSFODNN7EXAMPLE", "clean_value"],
                            "pan_list": ("ABCDE1234F", "safe")
                        }
                    },
                )
            }
        ]
    }
    sanitized = sanitize_payload(payload)
    assert sanitized["level1"][0]["level2"][0]["level3"]["keys"][0] == "[REDACTED: API_KEY]"
    assert sanitized["level1"][0]["level2"][0]["level3"]["pan_list"][0] == "[REDACTED: PAN_NUMBER]"

def test_sanitize_mcp_content_blocks():
    payload = {
        "result": {
            "content": [
                {
                    "type": "text",
                    "text": "AWS Key leaked: AKIAIOSFODNN7EXAMPLE and PAN: ABCDE1234F"
                }
            ]
        }
    }
    sanitized = sanitize_payload(payload)
    content_text = sanitized["result"]["content"][0]["text"]
    assert "AKIAIOSFODNN7EXAMPLE" not in content_text
    assert "ABCDE1234F" not in content_text
    assert "[REDACTED: API_KEY]" in content_text
    assert "[REDACTED: PAN_NUMBER]" in content_text
