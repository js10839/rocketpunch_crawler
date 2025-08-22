from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import jobs, community, email
import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()
origins = os.getenv("ALLOWED_ORIGINS", "").split(",")

app = FastAPI(title="Job Tracker API")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
app.include_router(community.router, prefix="/community", tags=["community"])
app.include_router(email.router, prefix="/email", tags=["email"])