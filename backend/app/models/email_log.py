from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base


class EmailLog(Base):
    __tablename__ = "EmailLogs"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("Applications.id"), nullable=False)
    recipient_email = Column(String(120), nullable=False)
    subject = Column(String(255), nullable=False)
    message_body = Column(Text, nullable=False)
    sent_at = Column(DateTime, server_default=func.getdate())
    sent_by = Column(Integer, ForeignKey("Users.id"), nullable=False)