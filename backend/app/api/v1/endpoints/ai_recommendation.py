"""
AI 권고안 API 엔드포인트
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.ai_recommendation import (
    AIRecommendation,
    AIRecommendationCreate,
    AIRecommendationResponse,
    RecommendationFilter,
    RecommendationApproval
)
from app.services.ai_service import AIService
from app.services.data_collection_service import DataCollectionService
from app.services.risk_analysis_service import RiskAnalysisService
from app.services.notification_service import NotificationService, NotificationChannel, NotificationPriority

router = APIRouter()

# 서비스 인스턴스
ai_service = AIService()
data_collection_service = DataCollectionService()
risk_analysis_service = RiskAnalysisService()
notification_service = NotificationService()

@router.post("/generate", response_model=List[AIRecommendationResponse])
async def generate_recommendations(
    location: dict,
    radius_km: float = 5.0,
    db: Session = Depends(get_db)
):
    """
    AI 권고안 생성
    
    Args:
        location: {"lat": float, "lng": float} 위치 정보
        radius_km: 데이터 수집 반경 (km)
        db: 데이터베이스 세션
        
    Returns:
        생성된 권고안 리스트
    """
    try:
        # 1. 데이터 수집
        sensor_data = await data_collection_service.collect_all_data(location, radius_km)
        
        # 2. 위험도 분석
        risk_analysis = await risk_analysis_service.analyze_fire_risk(sensor_data, location)
        
        # 3. AI 권고안 생성
        recommendations = await ai_service.generate_recommendations(
            sensor_data, 
            risk_analysis["overall_risk"], 
            location
        )
        
        # 4. 데이터베이스에 저장
        saved_recommendations = []
        for rec_data in recommendations:
            db_rec = AIRecommendation(**rec_data.dict())
            db.add(db_rec)
            db.commit()
            db.refresh(db_rec)
            saved_recommendations.append(db_rec)
        
        return saved_recommendations
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"권고안 생성 실패: {str(e)}")

@router.get("/", response_model=List[AIRecommendationResponse])
async def get_recommendations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    agency_type: Optional[str] = None,
    status: Optional[str] = None,
    priority_level: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    권고안 목록 조회
    
    Args:
        skip: 건너뛸 개수
        limit: 조회할 개수
        agency_type: 기관 타입 필터
        status: 상태 필터
        priority_level: 우선순위 필터
        db: 데이터베이스 세션
        
    Returns:
        권고안 리스트
    """
    try:
        query = db.query(AIRecommendation)
        
        if agency_type:
            query = query.filter(AIRecommendation.agency_type == agency_type)
        if status:
            query = query.filter(AIRecommendation.status == status)
        if priority_level:
            query = query.filter(AIRecommendation.priority_level == priority_level)
        
        recommendations = query.offset(skip).limit(limit).all()
        return recommendations
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"권고안 조회 실패: {str(e)}")

@router.get("/{recommendation_id}", response_model=AIRecommendationResponse)
async def get_recommendation(
    recommendation_id: str,
    db: Session = Depends(get_db)
):
    """
    특정 권고안 조회
    
    Args:
        recommendation_id: 권고안 ID
        db: 데이터베이스 세션
        
    Returns:
        권고안 상세 정보
    """
    try:
        recommendation = db.query(AIRecommendation).filter(
            AIRecommendation.recommendation_id == recommendation_id
        ).first()
        
        if not recommendation:
            raise HTTPException(status_code=404, detail="권고안을 찾을 수 없습니다")
        
        return recommendation
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"권고안 조회 실패: {str(e)}")

@router.post("/{recommendation_id}/approve")
async def approve_recommendation(
    recommendation_id: str,
    approval_data: RecommendationApproval,
    db: Session = Depends(get_db)
):
    """
    권고안 승인/거부
    
    Args:
        recommendation_id: 권고안 ID
        approval_data: 승인 정보
        db: 데이터베이스 세션
        
    Returns:
        승인 결과
    """
    try:
        recommendation = db.query(AIRecommendation).filter(
            AIRecommendation.recommendation_id == recommendation_id
        ).first()
        
        if not recommendation:
            raise HTTPException(status_code=404, detail="권고안을 찾을 수 없습니다")
        
        # 권고안 상태 업데이트
        if approval_data.approved:
            recommendation.status = "approved"
            recommendation.approved_by = approval_data.approved_by
            recommendation.approved_at = db.func.now()
        else:
            recommendation.status = "rejected"
            recommendation.rejection_reason = approval_data.rejection_reason
        
        db.commit()
        
        # 승인된 경우 알림 전송
        if approval_data.approved:
            channels = [NotificationChannel.SMS, NotificationChannel.EMAIL, NotificationChannel.CAP]
            priority = NotificationPriority.HIGH if recommendation.priority_level == "high" else NotificationPriority.MEDIUM
            
            await notification_service.send_notification(
                recommendation, channels, priority
            )
        
        return {
            "message": "승인 처리 완료",
            "recommendation_id": recommendation_id,
            "status": recommendation.status
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"승인 처리 실패: {str(e)}")

@router.post("/{recommendation_id}/send-notification")
async def send_notification(
    recommendation_id: str,
    channels: List[str],
    priority: str = "high",
    db: Session = Depends(get_db)
):
    """
    권고안 알림 전송
    
    Args:
        recommendation_id: 권고안 ID
        channels: 전송할 채널 리스트
        priority: 알림 우선순위
        db: 데이터베이스 세션
        
    Returns:
        전송 결과
    """
    try:
        recommendation = db.query(AIRecommendation).filter(
            AIRecommendation.recommendation_id == recommendation_id
        ).first()
        
        if not recommendation:
            raise HTTPException(status_code=404, detail="권고안을 찾을 수 없습니다")
        
        # 채널 변환
        notification_channels = [NotificationChannel(ch) for ch in channels]
        notification_priority = NotificationPriority(priority)
        
        # 알림 전송
        result = await notification_service.send_notification(
            recommendation, notification_channels, notification_priority
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"알림 전송 실패: {str(e)}")

@router.delete("/{recommendation_id}")
async def delete_recommendation(
    recommendation_id: str,
    db: Session = Depends(get_db)
):
    """
    권고안 삭제
    
    Args:
        recommendation_id: 권고안 ID
        db: 데이터베이스 세션
        
    Returns:
        삭제 결과
    """
    try:
        recommendation = db.query(AIRecommendation).filter(
            AIRecommendation.recommendation_id == recommendation_id
        ).first()
        
        if not recommendation:
            raise HTTPException(status_code=404, detail="권고안을 찾을 수 없습니다")
        
        db.delete(recommendation)
        db.commit()
        
        return {"message": "권고안이 삭제되었습니다"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"권고안 삭제 실패: {str(e)}")

@router.get("/stats/summary")
async def get_recommendation_stats(db: Session = Depends(get_db)):
    """
    권고안 통계 조회
    
    Args:
        db: 데이터베이스 세션
        
    Returns:
        권고안 통계
    """
    try:
        total_count = db.query(AIRecommendation).count()
        pending_count = db.query(AIRecommendation).filter(
            AIRecommendation.status == "pending"
        ).count()
        approved_count = db.query(AIRecommendation).filter(
            AIRecommendation.status == "approved"
        ).count()
        rejected_count = db.query(AIRecommendation).filter(
            AIRecommendation.status == "rejected"
        ).count()
        
        # 기관별 통계
        agency_stats = {}
        for agency in ["fire_department", "forest_service", "local_government"]:
            count = db.query(AIRecommendation).filter(
                AIRecommendation.agency_type == agency
            ).count()
            agency_stats[agency] = count
        
        # 우선순위별 통계
        priority_stats = {}
        for priority in ["low", "medium", "high", "critical"]:
            count = db.query(AIRecommendation).filter(
                AIRecommendation.priority_level == priority
            ).count()
            priority_stats[priority] = count
        
        return {
            "total_count": total_count,
            "status_counts": {
                "pending": pending_count,
                "approved": approved_count,
                "rejected": rejected_count
            },
            "agency_counts": agency_stats,
            "priority_counts": priority_stats
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"통계 조회 실패: {str(e)}")
