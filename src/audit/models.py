from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float
from src.core.database import Base

class AuditRecord(Base):
    __tablename__ = "audit_records"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String, index=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    agent_id = Column(String, index=True, nullable=False)
    method = Column(String, nullable=False)
    tool_name = Column(String, nullable=True)
    payload_hash = Column(String, nullable=False)
    risk_level = Column(String, nullable=False)
    decision = Column(String, nullable=False)
    latency_ms = Column(Float, nullable=False)
