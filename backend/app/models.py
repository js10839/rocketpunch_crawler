from pydantic import BaseModel, Field
from typing import List, Optional

class Job(BaseModel):
    회사명: str
    포지션: str
    설명: str
    링크: Optional[str] = None

class CommunityPost(BaseModel):
    author: str = Field(..., max_length=30)
    content: str
    timestamp: Optional[str]

class EmailRequest(BaseModel):
    to_email: str
    subject: str
    body: str
    # Optional: 첨부파일 경로 지정