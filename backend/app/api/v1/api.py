"""
API 라우터 설정
"""

from fastapi import APIRouter
from app.api.v1.endpoints import (
    sensor_data,
    ai_recommendation,
    approval,
    notification,
    dashboard
)

api_router = APIRouter()

# 센서 데이터 엔드포인트
api_router.include_router(
    sensor_data.router,
    prefix="/sensor-data",
    tags=["센서 데이터"]
)

# AI 권고안 엔드포인트
api_router.include_router(
    ai_recommendation.router,
    prefix="/ai-recommendations",
    tags=["AI 권고안"]
)

# 승인 프로세스 엔드포인트
api_router.include_router(
    approval.router,
    prefix="/approval",
    tags=["승인 프로세스"]
)

# 알림 엔드포인트
api_router.include_router(
    notification.router,
    prefix="/notifications",
    tags=["알림"]
)

# 대시보드 엔드포인트
api_router.include_router(
    dashboard.router,
    prefix="/dashboard",
    tags=["대시보드"]
)
