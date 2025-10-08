from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from models.auth import User  
from database import Base

class VoiceAgent(Base):
    __tablename__ = "voice_agents"

    id = Column(String, primary_key=True, index=True)  # ElevenLabs agent ID as string
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  
    name = Column(String, nullable=False)
    phone_number = Column(String, unique=True, nullable=True)
    system_prompt = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="voice_agents")
    knowledge_bases = relationship("KnowledgeBase", back_populates="voice_agent")

    __table_args__ = (
        UniqueConstraint('user_id', 'name', name='uq_user_agent_name'),
    )

    def __repr__(self):
        return f"<VoiceAgent id={self.id} name={self.name} phone={self.phone_number}>"


class KnowledgeBase(Base):
    __tablename__ = "knowledge_bases"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String, ForeignKey("voice_agents.id"), nullable=False)
    business_knowledge = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    voice_agent = relationship("VoiceAgent", back_populates="knowledge_bases")

    def __repr__(self):
        return f"<KnowledgeBase id={self.id} agent_id={self.agent_id}>"