"""
설정 관리 모듈
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    """애플리케이션 설정"""
    
    # 기본 설정
    APP_NAME: str = "산불 대응 AI Agent 시스템"
    VERSION: str = "2.0.0"
    DEBUG: bool = False
    
    # 서버 설정
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # 데이터베이스 설정
    DATABASE_URL: str = "postgresql://admin:password123@localhost:5432/forest_fire_ai"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    
    # Redis 설정
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_PASSWORD: Optional[str] = None
    
    # RabbitMQ 설정
    RABBITMQ_URL: str = "amqp://admin:password123@localhost:5672"
    RABBITMQ_QUEUE_PREFIX: str = "forest_fire"
    
    # AI 모델 설정
    AI_MODEL_NAME: str = "믿:음-2.0"
    AI_MODEL_PATH: str = "./models/mideum-2.0"
    AI_CONFIDENCE_THRESHOLD: float = 0.8
    AI_MAX_TOKENS: int = 2048
    AI_TEMPERATURE: float = 0.7
    
    # Vision AI 설정
    VISION_AI_ENDPOINT: str = "https://api.kt.com/gigai"
    VISION_AI_API_KEY: str = ""
    VISION_CONFIDENCE_THRESHOLD: float = 0.85
    
    # IoT 센서 설정
    IOT_SENSOR_ENDPOINT: str = "https://sensors.forest-fire.com"
    IOT_SENSOR_API_KEY: str = ""
    SENSOR_UPDATE_INTERVAL: int = 30  # 초
    
    # 기상청 API 설정
    WEATHER_API_ENDPOINT: str = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0"
    WEATHER_API_KEY: str = ""
    
    # 알림 설정
    NOTIFICATION_CHANNELS: List[str] = ["sms", "email", "push", "radio"]
    CAP_PROTOCOL_ENABLED: bool = True
    CAP_SERVER_URL: str = "https://cap.forest-fire.com"
    
    # 보안 설정
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    
    # 로깅 설정
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/forest_fire_ai.log"
    
    # 모니터링 설정
    PROMETHEUS_ENABLED: bool = True
    GRAFANA_ENABLED: bool = True
    METRICS_PORT: int = 9090
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# 전역 설정 인스턴스
settings = Settings()
