import pytest
from src.risk.heuristics import evaluate_argument_heuristics

def test_heuristic_dangerous_command():
    args = {"cmd": "sudo apt-get update && chmod 777 /var/www"}
    detected, reason = evaluate_argument_heuristics(args)
    assert detected is True
    assert "HEURISTIC_DANGEROUS_COMMAND" in reason

def test_heuristic_system_directory_access():
    args = {"path": "/etc/nginx/nginx.conf", "mode": "write"}
    detected, reason = evaluate_argument_heuristics(args)
    assert detected is True
    assert "HEURISTIC_SYSTEM_DIRECTORY_ACCESS" in reason

def test_heuristic_safe_argument():
    args = {"path": "/home/user/docs/notes.txt", "query": "search keyword"}
    detected, reason = evaluate_argument_heuristics(args)
    assert detected is False
    assert reason == ""
