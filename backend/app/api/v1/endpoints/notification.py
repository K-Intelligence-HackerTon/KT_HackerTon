"""
알림 API 엔드포인트
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.ai_recommendation import AIRecommendation
from app.services.notification_service import NotificationService, NotificationChannel, NotificationPriority

router = APIRouter()
notification_service = NotificationService()

@router.post("/send/{recommendation_id}")
async def send_notification(
    recommendation_id: str,
    channels: List[str],
    priority: str = "high",
    db: Session = Depends(get_db)
):
    """알림 전송"""
    try:
        recommendation = db.query(AIRecommendation).filter(
            AIRecommendation.recommendation_id == recommendation_id
        ).first()
        
        if not recommendation:
            raise HTTPException(status_code=404, detail="권고안을 찾을 수 없습니다")
        
        notification_channels = [NotificationChannel(ch) for ch in channels]
        notification_priority = NotificationPriority(priority)
        
        result = await notification_service.send_notification(
            recommendation, notification_channels, notification_priority
        )
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"알림 전송 실패: {str(e)}")
