from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ThreadUser(BaseModel):
    """Simplified user information."""
    id: int
    name: str
    course_role: Optional[str] = None


class ThreadComment(BaseModel):
    """Simplified comment model with only essential fields."""
    id: int
    user_id: int
    course_id: int
    thread_id: int
    parent_id: Optional[int] = None
    type: str
    document: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        extra = 'ignore'  # Ignore extra fields in the API response


class Thread(BaseModel):
    """Simplified thread model with only the fields you need."""
    id: int
    user_id: int
    course_id: int
    type: str
    title: str
    document: str
    category: str
    subcategory: str
    subsubcategory: str
    unique_view_count: int
    vote_count: int
    created_at: datetime
    updated_at: datetime
    user: Optional[ThreadUser] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert Thread to a dictionary"""
        return self.model_dump()

    class Config:
        extra = 'ignore'  # Ignore extra fields in the API response


class ThreadWithComments(Thread):
    """Thread with comments included."""
    comments: List[ThreadComment] = []
