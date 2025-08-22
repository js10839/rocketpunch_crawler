from fastapi import APIRouter, HTTPException
from ..models import EmailRequest
from ..services.emailer import send_email

router = APIRouter()

@router.post("/send")
async def send_email_endpoint(req: EmailRequest):
    try:
        send_email(req.to_email, req.subject, req.body)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))