from fastapi import APIRouter, HTTPException
from typing import List
from ..models import CommunityPost
from ..services.logger import load_posts, append_post

router = APIRouter()

@router.get("/", response_model=List[CommunityPost])
async def list_posts():
    return load_posts()

@router.post("/", response_model=CommunityPost)
async def create_post(post: CommunityPost):
    try:
        post.timestamp = append_post(post)
        return post
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))