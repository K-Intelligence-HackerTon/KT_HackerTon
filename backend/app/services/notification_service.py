"""
알림 서비스 모듈
다중 채널 전송 시스템 (SMS, 이메일, 푸시, 무전 등)
"""

import asyncio
import logging
import httpx
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.core.config import settings
from app.models.ai_recommendation import AIRecommendation, AgencyType

logger = logging.getLogger(__name__)

class NotificationChannel(str, Enum):
    """알림 채널 열거형"""
    SMS = "sms"
    EMAIL = "email"
    PUSH = "push"
    RADIO = "radio"
    CAP = "cap"  # Common Alerting Protocol
    WEBHOOK = "webhook"

class NotificationPriority(str, Enum):
    """알림 우선순위"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class NotificationService:
    """알림 서비스 클래스"""
    
    def __init__(self):
        self.channels = {
            NotificationChannel.SMS: self._send_sms,
            NotificationChannel.EMAIL: self._send_email,
            NotificationChannel.PUSH: self._send_push,
            NotificationChannel.RADIO: self._send_radio,
            NotificationChannel.CAP: self._send_cap,
            NotificationChannel.WEBHOOK: self._send_webhook
        }
    
    async def send_notification(
        self,
        recommendation: AIRecommendation,
        channels: List[NotificationChannel],
        priority: NotificationPriority = NotificationPriority.HIGH
    ) -> Dict[str, Any]:
        """
        권고안 알림 전송
        
        Args:
            recommendation: AI 권고안
            channels: 전송할 채널 리스트
            priority: 알림 우선순위
            
        Returns:
            전송 결과 딕셔너리
        """
        try:
            logger.info(f"📤 알림 전송 시작 - 권고안: {recommendation.recommendation_id}, 채널: {channels}")
            
            # CAP 메시지 생성
            cap_message = self._create_cap_message(recommendation, priority)
            
            # 각 채널별로 전송
            results = {}
            for channel in channels:
                try:
                    result = await self.channels[channel](recommendation, cap_message, priority)
                    results[channel.value] = {
                        "success": True,
                        "message": "전송 성공",
                        "timestamp": datetime.now().isoformat(),
                        "result": result
                    }
                except Exception as e:
                    logger.error(f"❌ {channel.value} 채널 전송 실패: {str(e)}")
                    results[channel.value] = {
                        "success": False,
                        "message": f"전송 실패: {str(e)}",
                        "timestamp": datetime.now().isoformat(),
                        "error": str(e)
                    }
            
            # 전송 결과 요약
            success_count = sum(1 for r in results.values() if r["success"])
            total_count = len(results)
            
            logger.info(f"✅ 알림 전송 완료 - 성공: {success_count}/{total_count}")
            
            return {
                "recommendation_id": recommendation.recommendation_id,
                "total_channels": total_count,
                "success_count": success_count,
                "failure_count": total_count - success_count,
                "results": results,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ 알림 전송 실패: {str(e)}")
            raise
    
    def _create_cap_message(
        self, 
        recommendation: AIRecommendation, 
        priority: NotificationPriority
    ) -> Dict[str, Any]:
        """CAP (Common Alerting Protocol) 메시지 생성"""
        try:
            # 우선순위에 따른 CAP 심각도 매핑
            severity_map = {
                NotificationPriority.LOW: "Minor",
                NotificationPriority.MEDIUM: "Moderate", 
                NotificationPriority.HIGH: "Severe",
                NotificationPriority.CRITICAL: "Extreme"
            }
            
            # 기관별 수신자 매핑
            agency_contacts = {
                AgencyType.FIRE_DEPARTMENT: {
                    "sms": ["010-1234-5678", "010-2345-6789"],
                    "email": ["fire@example.com", "emergency@fire.gov.kr"],
                    "radio": ["FIRE_CH_01", "FIRE_CH_02"]
                },
                AgencyType.FOREST_SERVICE: {
                    "sms": ["010-3456-7890", "010-4567-8901"],
                    "email": ["forest@example.com", "emergency@forest.gov.kr"],
                    "radio": ["FOREST_CH_01", "FOREST_CH_02"]
                },
                AgencyType.LOCAL_GOVERNMENT: {
                    "sms": ["010-5678-9012", "010-6789-0123"],
                    "email": ["local@example.com", "emergency@local.gov.kr"],
                    "radio": ["LOCAL_CH_01", "LOCAL_CH_02"]
                }
            }
            
            contacts = agency_contacts.get(recommendation.agency_type, {})
            
            cap_message = {
                "identifier": f"KOREA-FOREST-FIRE-{recommendation.recommendation_id}",
                "sender": "forest-fire-ai-agent@kt.com",
                "sent": datetime.now().isoformat() + "Z",
                "status": "Actual",
                "msgType": "Alert",
                "scope": "Public",
                "info": {
                    "language": "ko-KR",
                    "category": "Fire",
                    "event": "산불 대응 AI 권고안",
                    "urgency": priority.value.upper(),
                    "severity": severity_map[priority],
                    "certainty": "Observed",
                    "senderName": "산불 대응 AI Agent 시스템",
                    "headline": recommendation.title,
                    "description": recommendation.description or "",
                    "instruction": self._create_instruction_text(recommendation),
                    "area": {
                        "areaDesc": recommendation.location_name or "산불 현장",
                        "polygon": self._create_polygon(recommendation),
                        "circle": self._create_circle(recommendation)
                    },
                    "parameter": {
                        "AI_CONFIDENCE": str(recommendation.ai_confidence),
                        "PRIORITY_LEVEL": recommendation.priority_level.value,
                        "AGENCY_TYPE": recommendation.agency_type.value,
                        "AFFECTED_RADIUS": str(recommendation.affected_radius or 0),
                        "EXPECTED_COST": str(recommendation.expected_cost or 0)
                    },
                    "contact": contacts
                }
            }
            
            return cap_message
            
        except Exception as e:
            logger.error(f"CAP 메시지 생성 실패: {str(e)}")
            return {}
    
    def _create_instruction_text(self, recommendation: AIRecommendation) -> str:
        """지시사항 텍스트 생성"""
        instructions = []
        
        if recommendation.immediate_actions:
            instructions.append("즉시 조치사항:")
            for i, action in enumerate(recommendation.immediate_actions[:3], 1):
                instructions.append(f"{i}. {action.get('action', '')}")
        
        if recommendation.legal_basis:
            instructions.append("\n법적 근거:")
            for basis in recommendation.legal_basis[:2]:
                instructions.append(f"- {basis.get('law', '')} {basis.get('article', '')}")
        
        return "\n".join(instructions)
    
    def _create_polygon(self, recommendation: AIRecommendation) -> Optional[str]:
        """영향 지역 폴리곤 생성"""
        if not recommendation.affected_radius:
            return None
        
        # 간단한 원형 폴리곤 생성 (실제로는 더 정교한 계산 필요)
        radius_km = recommendation.affected_radius
        lat = recommendation.location_lat
        lng = recommendation.location_lng
        
        # 1km = 약 0.009도 (대략적)
        lat_offset = radius_km * 0.009
        lng_offset = radius_km * 0.009 / 1.1  # 경도는 위도에 비해 약간 작음
        
        polygon = f"{lat-lat_offset},{lng-lng_offset} {lat+lat_offset},{lng-lng_offset} {lat+lat_offset},{lng+lng_offset} {lat-lat_offset},{lng+lng_offset} {lat-lat_offset},{lng-lng_offset}"
        return polygon
    
    def _create_circle(self, recommendation: AIRecommendation) -> Optional[str]:
        """영향 지역 원형 생성"""
        if not recommendation.affected_radius:
            return None
        
        return f"{recommendation.location_lat},{recommendation.location_lng} {recommendation.affected_radius}"
    
    async def _send_sms(
        self, 
        recommendation: AIRecommendation, 
        cap_message: Dict[str, Any],
        priority: NotificationPriority
    ) -> Dict[str, Any]:
        """SMS 전송"""
        try:
            # SMS 내용 생성
            sms_content = self._create_sms_content(recommendation, cap_message)
            
            # 실제 SMS 서비스 API 호출 (예시)
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.sms-service.com/send",
                    json={
                        "to": cap_message["info"]["contact"].get("sms", []),
                        "message": sms_content,
                        "priority": priority.value
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    return {"status": "sent", "message_id": response.json().get("message_id")}
                else:
                    raise Exception(f"SMS 전송 실패: {response.status_code}")
                    
        except Exception as e:
            logger.error(f"SMS 전송 실패: {str(e)}")
            raise
    
    async def _send_email(
        self, 
        recommendation: AIRecommendation, 
        cap_message: Dict[str, Any],
        priority: NotificationPriority
    ) -> Dict[str, Any]:
        """이메일 전송"""
        try:
            # 이메일 내용 생성
            email_subject, email_body = self._create_email_content(recommendation, cap_message)
            
            # 이메일 전송 (실제로는 SMTP 서버 사용)
            msg = MIMEMultipart()
            msg['From'] = "forest-fire-ai@kt.com"
            msg['To'] = ", ".join(cap_message["info"]["contact"].get("email", []))
            msg['Subject'] = email_subject
            
            msg.attach(MIMEText(email_body, 'html', 'utf-8'))
            
            # SMTP 서버 설정 (실제 환경에서는 설정에서 가져옴)
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            smtp_username = "your-email@gmail.com"
            smtp_password = "your-password"
            
            # 실제 전송은 비동기로 처리하지 않음 (예시)
            # server = smtplib.SMTP(smtp_server, smtp_port)
            # server.starttls()
            # server.login(smtp_username, smtp_password)
            # server.send_message(msg)
            # server.quit()
            
            return {"status": "sent", "subject": email_subject}
            
        except Exception as e:
            logger.error(f"이메일 전송 실패: {str(e)}")
            raise
    
    async def _send_push(
        self, 
        recommendation: AIRecommendation, 
        cap_message: Dict[str, Any],
        priority: NotificationPriority
    ) -> Dict[str, Any]:
        """푸시 알림 전송"""
        try:
            # 푸시 알림 내용 생성
            push_data = self._create_push_content(recommendation, cap_message)
            
            # FCM 또는 다른 푸시 서비스 API 호출
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://fcm.googleapis.com/fcm/send",
                    headers={
                        "Authorization": f"key={settings.FCM_SERVER_KEY}",
                        "Content-Type": "application/json"
                    },
                    json=push_data,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    return {"status": "sent", "message_id": response.json().get("message_id")}
                else:
                    raise Exception(f"푸시 전송 실패: {response.status_code}")
                    
        except Exception as e:
            logger.error(f"푸시 전송 실패: {str(e)}")
            raise
    
    async def _send_radio(
        self, 
        recommendation: AIRecommendation, 
        cap_message: Dict[str, Any],
        priority: NotificationPriority
    ) -> Dict[str, Any]:
        """무전 전송"""
        try:
            # 무전 메시지 생성
            radio_message = self._create_radio_message(recommendation, cap_message)
            
            # 무전 시스템 API 호출
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.radio-system.com/broadcast",
                    json={
                        "channels": cap_message["info"]["contact"].get("radio", []),
                        "message": radio_message,
                        "priority": priority.value
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    return {"status": "broadcasted", "channels": cap_message["info"]["contact"].get("radio", [])}
                else:
                    raise Exception(f"무전 전송 실패: {response.status_code}")
                    
        except Exception as e:
            logger.error(f"무전 전송 실패: {str(e)}")
            raise
    
    async def _send_cap(
        self, 
        recommendation: AIRecommendation, 
        cap_message: Dict[str, Any],
        priority: NotificationPriority
    ) -> Dict[str, Any]:
        """CAP 프로토콜 전송"""
        try:
            # CAP 서버로 전송
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    settings.CAP_SERVER_URL,
                    json=cap_message,
                    headers={"Content-Type": "application/json"},
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    return {"status": "sent", "cap_id": response.json().get("cap_id")}
                else:
                    raise Exception(f"CAP 전송 실패: {response.status_code}")
                    
        except Exception as e:
            logger.error(f"CAP 전송 실패: {str(e)}")
            raise
    
    async def _send_webhook(
        self, 
        recommendation: AIRecommendation, 
        cap_message: Dict[str, Any],
        priority: NotificationPriority
    ) -> Dict[str, Any]:
        """웹훅 전송"""
        try:
            # 웹훅 URL 설정 (실제로는 설정에서 가져옴)
            webhook_urls = {
                AgencyType.FIRE_DEPARTMENT: "https://fire-dept.example.com/webhook",
                AgencyType.FOREST_SERVICE: "https://forest-service.example.com/webhook",
                AgencyType.LOCAL_GOVERNMENT: "https://local-gov.example.com/webhook"
            }
            
            webhook_url = webhook_urls.get(recommendation.agency_type)
            if not webhook_url:
                raise Exception(f"웹훅 URL을 찾을 수 없습니다: {recommendation.agency_type}")
            
            # 웹훅 전송
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    webhook_url,
                    json={
                        "recommendation": recommendation.dict(),
                        "cap_message": cap_message,
                        "priority": priority.value
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    return {"status": "sent", "webhook_url": webhook_url}
                else:
                    raise Exception(f"웹훅 전송 실패: {response.status_code}")
                    
        except Exception as e:
            logger.error(f"웹훅 전송 실패: {str(e)}")
            raise
    
    def _create_sms_content(self, recommendation: AIRecommendation, cap_message: Dict[str, Any]) -> str:
        """SMS 내용 생성"""
        return f"""
🔥 산불 대응 AI 권고안
{recommendation.title}

위치: {recommendation.location_name or '산불 현장'}
신뢰도: {recommendation.ai_confidence:.1f}%
우선순위: {recommendation.priority_level.value.upper()}

즉시 조치사항:
{self._create_instruction_text(recommendation)[:100]}...

자세한 내용은 대시보드에서 확인하세요.
        """.strip()
    
    def _create_email_content(self, recommendation: AIRecommendation, cap_message: Dict[str, Any]) -> tuple:
        """이메일 내용 생성"""
        subject = f"🔥 산불 대응 AI 권고안 - {recommendation.agency_type.value}"
        
        body = f"""
        <html>
        <body>
            <h2>🔥 산불 대응 AI 권고안</h2>
            <h3>{recommendation.title}</h3>
            
            <p><strong>위치:</strong> {recommendation.location_name or '산불 현장'}</p>
            <p><strong>신뢰도:</strong> {recommendation.ai_confidence:.1f}%</p>
            <p><strong>우선순위:</strong> {recommendation.priority_level.value.upper()}</p>
            <p><strong>영향 반경:</strong> {recommendation.affected_radius}km</p>
            
            <h4>즉시 조치사항:</h4>
            <ul>
        """
        
        if recommendation.immediate_actions:
            for action in recommendation.immediate_actions:
                body += f"<li>{action.get('action', '')} - {action.get('estimatedTime', '')}</li>"
        
        body += """
            </ul>
            
            <h4>법적 근거:</h4>
            <ul>
        """
        
        if recommendation.legal_basis:
            for basis in recommendation.legal_basis:
                body += f"<li>{basis.get('law', '')} {basis.get('article', '')} - {basis.get('content', '')}</li>"
        
        body += """
            </ul>
            
            <p>자세한 내용은 대시보드에서 확인하세요.</p>
        </body>
        </html>
        """
        
        return subject, body
    
    def _create_push_content(self, recommendation: AIRecommendation, cap_message: Dict[str, Any]) -> Dict[str, Any]:
        """푸시 알림 내용 생성"""
        return {
            "to": "/topics/forest-fire-alerts",
            "notification": {
                "title": f"🔥 {recommendation.agency_type.value} 권고안",
                "body": recommendation.title,
                "icon": "fire_icon",
                "sound": "default",
                "priority": "high"
            },
            "data": {
                "recommendation_id": recommendation.recommendation_id,
                "agency_type": recommendation.agency_type.value,
                "priority": recommendation.priority_level.value,
                "confidence": recommendation.ai_confidence
            }
        }
    
    def _create_radio_message(self, recommendation: AIRecommendation, cap_message: Dict[str, Any]) -> str:
        """무전 메시지 생성"""
        return f"""
        산불 대응 AI 권고안 수신
        기관: {recommendation.agency_type.value}
        위치: {recommendation.location_name or '산불 현장'}
        신뢰도: {recommendation.ai_confidence:.1f}%
        우선순위: {recommendation.priority_level.value.upper()}
        
        즉시 조치사항 확인 요청
        대시보드에서 상세 내용 확인
        """.strip()
