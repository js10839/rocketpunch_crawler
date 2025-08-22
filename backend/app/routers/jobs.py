from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from ..services.job_crawler import crawl_jobs
from ..models import Job

router = APIRouter()

@router.get("/", response_model=List[Job])
async def get_jobs(
    keyword: Optional[str] = Query(None),
    seniority: str = Query(None)
):
    try:
        raw = crawl_jobs(keyword, seniority)
        return [Job(**r) for r in raw]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))