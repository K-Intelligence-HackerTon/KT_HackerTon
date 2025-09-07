"""
승인 프로세스 API 엔드포인트
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.ai_recommendation import AIRecommendation, RecommendationApproval

router = APIRouter()

@router.post("/{recommendation_id}/approve")
async def approve_recommendation(
    recommendation_id: str,
    approval_data: RecommendationApproval,
    db: Session = Depends(get_db)
):
    """권고안 승인/거부"""
    try:
        recommendation = db.query(AIRecommendation).filter(
            AIRecommendation.recommendation_id == recommendation_id
        ).first()
        
        if not recommendation:
            raise HTTPException(status_code=404, detail="권고안을 찾을 수 없습니다")
        
        if approval_data.approved:
            recommendation.status = "approved"
            recommendation.approved_by = approval_data.approved_by
        else:
            recommendation.status = "rejected"
            recommendation.rejection_reason = approval_data.rejection_reason
        
        db.commit()
        
        return {
            "message": "승인 처리 완료",
            "recommendation_id": recommendation_id,
            "status": recommendation.status
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"승인 처리 실패: {str(e)}")

@router.get("/pending", response_model=List[AIRecommendation])
async def get_pending_recommendations(
    db: Session = Depends(get_db)
):
    """대기 중인 권고안 목록 조회"""
    try:
        recommendations = db.query(AIRecommendation).filter(
            AIRecommendation.status == "pending"
        ).all()
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"대기 중인 권고안 조회 실패: {str(e)}")
