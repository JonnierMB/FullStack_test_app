from fastapi import APIRouter, Request, HTTPException, Depends
from ..databases.db import create_challenge_quota
from ..databases.models import get_db
from sqlalchemy.orm import Session
from svix.webhooks import Webhook
import os
import json


router = APIRouter()

@router.post("/clerk")
async def handle_user_created(request: Request, db: Session = Depends(get_db)):
    Webhook_secret = os.getenv("CLERK_WEBHOOK_SECRET")
    if not Webhook_secret:
        raise HTTPException(status_code=500, detail="Webhook secret not configured")
    body = await request.body()
    payload = body.decode("utf-8")
    headers = dict(request.headers)

    try:
        wh = Webhook(Webhook_secret)
        wh.verify(payload, headers)
        data = json.loads(payload)
        if data.get("type") != "user.created":
            return {"status": "ignored", "reason": "not user.created event"}
        
        user_data = data.get("data", {})
        user_id = user_data.get("id")

        create_challenge_quota(db, user_id)

        return {"status": "success", "user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Webhook verification failed: {str(e)}")

