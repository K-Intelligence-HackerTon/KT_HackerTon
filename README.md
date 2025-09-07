# 산불 대응 AI Agent 시스템 (믿:음 2.0 LLM)

## 📋 프로젝트 개요
산불 탐지부터 기관별 지시 전파까지의 전체 과정을 5단계로 체계화한 AI 기반 산불 대응 시스템입니다.

## 🏗️ 시스템 아키텍처

### 1단계: 데이터 수집 (센서 단)
- **Vision AI**: KT 기가아이즈 CCTV, 드론, 위성 영상 데이터 수집
- **IoT 센서**: 온도, 습도, 연기 농도 등 환경 데이터 수집

### 2단계: 위험도 산출 (백엔드)
- **데이터 융합**: 센서 데이터 결합 및 종합 신뢰도 지수 산출
- **확산 예측**: 기상 정보와 지형 데이터를 활용한 산불 확산 예측

### 3단계: AI 권고안 생성 (믿:음 LLM)
- **기관별 맞춤형 권고안**: 소방청, 산림청, 지자체별 대응 방안 생성
- **법령 기반 권고**: 관련 법령을 참조한 전문적 권고안 생성

### 4단계: 담당자 검토 및 승인 (UI/UX)
- **대시보드 표시**: 상위 기관 상황실에 권고안 표시
- **자동 승인**: 신뢰도가 높은 경우 조건부 자동 승인

### 5단계: 다중 채널 전송
- **CAP 기반 메시지**: 표준 Common Alerting Protocol 형식
- **다양한 채널**: 전용망, PS-LTE 무전, SMS 등

## 🛠️ 기술 스택
- **Backend**: Python (FastAPI), Node.js
- **AI/ML**: 믿:음 LLM, Vision AI, 데이터 융합
- **Frontend**: React.js, TypeScript
- **Database**: PostgreSQL, Redis
- **Message Queue**: RabbitMQ
- **Monitoring**: Prometheus, Grafana

## 📁 프로젝트 구조
```
forest-fire-ai-agent/
├── backend/                 # 백엔드 서비스
│   ├── data-collection/     # 데이터 수집 모듈
│   ├── risk-analysis/       # 위험도 분석 모듈
│   ├── ai-recommendation/   # AI 권고안 생성
│   ├── approval-system/     # 승인 시스템
│   └── notification/        # 알림 전송
├── frontend/                # 프론트엔드 대시보드
├── shared/                  # 공통 모듈
├── config/                  # 설정 파일
├── docs/                    # 문서
└── tests/                   # 테스트
```

## 🚀 시작하기
1. 의존성 설치: `pip install -r requirements.txt`
2. 데이터베이스 설정: `python scripts/setup_db.py`
3. 서비스 시작: `docker-compose up -d`
4. 대시보드 접속: `http://localhost:3000`

## 📞 연락처
- 개발팀: 
- 이메일: 32203919@dankook.ac.kr, kinglee4290@gmail.com