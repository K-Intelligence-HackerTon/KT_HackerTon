"""
대시보드 API 엔드포인트
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.models.sensor_data import SensorData
from app.models.ai_recommendation import AIRecommendation

router = APIRouter()

@router.get("/stats")
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """대시보드 통계 조회"""
    try:
        # 활성 화재 수
        active_fires = db.query(SensorData).filter(
            SensorData.fire_detected == True
        ).count()
        
        # 활성 센서 수
        active_sensors = db.query(SensorData).filter(
            SensorData.data_quality > 0.8
        ).count()
        
        # AI 권고안 수
        total_recommendations = db.query(AIRecommendation).count()
        
        # 승인 완료 수
        approved_recommendations = db.query(AIRecommendation).filter(
            AIRecommendation.status == "approved"
        ).count()
        
        # 기관별 권고안 수
        agency_stats = {}
        for agency in ["fire_department", "forest_service", "local_government"]:
            count = db.query(AIRecommendation).filter(
                AIRecommendation.agency_type == agency
            ).count()
            agency_stats[agency] = count
        
        # 우선순위별 권고안 수
        priority_stats = {}
        for priority in ["low", "medium", "high", "critical"]:
            count = db.query(AIRecommendation).filter(
                AIRecommendation.priority_level == priority
            ).count()
            priority_stats[priority] = count
        
        return {
            "active_fires": active_fires,
            "active_sensors": active_sensors,
            "total_recommendations": total_recommendations,
            "approved_recommendations": approved_recommendations,
            "agency_stats": agency_stats,
            "priority_stats": priority_stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"통계 조회 실패: {str(e)}")

@router.get("/recent-alerts")
async def get_recent_alerts(db: Session = Depends(get_db)):
    """최근 알림 조회"""
    try:
        # 최근 화재 탐지 데이터
        recent_fires = db.query(SensorData).filter(
            SensorData.fire_detected == True
        ).order_by(SensorData.created_at.desc()).limit(10).all()
        
        alerts = []
        for fire in recent_fires:
            alerts.append({
                "id": fire.id,
                "type": "fire",
                "title": "화재 탐지 알림",
                "message": f"{fire.location_name or '산불 현장'}에서 화재가 탐지되었습니다.",
                "time": fire.created_at.strftime("%H:%M:%S"),
                "level": "high",
                "location": fire.location_name or "산불 현장",
                "confidence": fire.fire_confidence or 0
            })
        
        return alerts
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"최근 알림 조회 실패: {str(e)}")
