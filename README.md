# 산불 대응 AI Agent 시스템 (믿:음 2.0 LLM)

## 📋 프로젝트 개요
산불 탐지부터 기관별 지시 전파까지의 전체 과정을 5단계로 체계화한 AI 기반 산불 대응 시스템입니다. 믿:음 2.0 LLM을 활용하여 실시간 모니터링, AI 권고안 생성, 승인 프로세스를 통합한 지능형 산불 대응 플랫폼입니다.

## 🏗️ 시스템 아키텍처

### 1단계: 데이터 수집 (센서 단)
- **Vision AI**: KT 기가아이즈 CCTV, 드론, 위성 영상 데이터 수집
- **IoT 센서**: 온도, 습도, 연기 농도, 풍속, 대기질 등 환경 데이터 수집
- **실시간 모니터링**: 용문산, 청편산 등 주요 산악 지역 CCTV 모니터링

### 2단계: 위험도 산출 (백엔드)
- **데이터 융합**: 센서 데이터 결합 및 종합 신뢰도 지수 산출
- **확산 예측**: 기상 정보와 지형 데이터를 활용한 산불 확산 예측
- **실시간 분석**: 5초마다 센서 데이터 업데이트 및 위험도 재계산

### 3단계: AI 권고안 생성 (믿:음 LLM)
- **기관별 맞춤형 권고안**: 소방청, 산림청, 지자체별 대응 방안 생성
- **법령 기반 권고**: 소방기본법, 재난 및 안전관리기본법 등 관련 법령 참조
- **상세한 권고 내용**: 즉시 조치사항, 법적 근거, 예상 비용/효과, 필요 자원 등

### 4단계: 담당자 검토 및 승인 (UI/UX)
- **대시보드 표시**: 상위 기관 상황실에 권고안 표시
- **실시간 알림**: 화재 감지 시 즉시 알림 및 신뢰도 표시
- **승인 프로세스**: 권고안 검토, 승인/거부, 코멘트 작성

### 5단계: 다중 채널 전송
- **CAP 기반 메시지**: 표준 Common Alerting Protocol 형식
- **다양한 채널**: 전용망, PS-LTE 무전, SMS 등
- **실시간 전파**: 승인된 권고안의 즉시 전파

## 🛠️ 기술 스택

### Backend
- **Python**: FastAPI 기반 RESTful API
- **AI/ML**: 믿:음 2.0 LLM (K-intelligence/Midm-2.0-Base-Instruct)
- **Vision AI**: 실시간 이미지 분석 및 화재 탐지
- **Database**: PostgreSQL (메인), Redis (캐시)
- **Message Queue**: RabbitMQ
- **Container**: Docker, Docker Compose

### Frontend
- **React.js**: TypeScript 기반 현대적 UI
- **Routing**: React Router DOM
- **Styling**: CSS3, 그라데이션, 글래스모피즘 효과
- **Real-time**: 실시간 데이터 시뮬레이션

### Infrastructure
- **Monitoring**: Prometheus, Grafana
- **LLM Serving**: vLLM (vllm/vllm-openai:latest)
- **GPU Support**: NVIDIA GPU 가속
- **Deployment**: Docker Compose

## 📁 프로젝트 구조
```
forest-fire-ai-agent/
├── backend/                    # 백엔드 서비스
│   ├── app/
│   │   ├── api/v1/endpoints/   # API 엔드포인트
│   │   ├── core/               # 핵심 설정 (DB, 로깅, 설정)
│   │   ├── models/             # 데이터 모델
│   │   └── services/           # 비즈니스 로직
│   │       ├── midm_llm_service.py    # 믿:음 LLM 서비스
│   │       ├── ai_service.py          # AI 권고안 생성
│   │       ├── vision_ai_service.py   # Vision AI 처리
│   │       └── risk_analysis_service.py # 위험도 분석
│   ├── requirements.txt        # Python 의존성
│   └── Dockerfile             # 백엔드 컨테이너
├── frontend/                   # 프론트엔드 대시보드
│   ├── public/
│   │   ├── images/            # 로컬 이미지 파일
│   │   │   ├── 용문산.png
│   │   │   └── 청편산.png
│   │   └── index.html
│   ├── src/
│   │   ├── components/Layout/  # 레이아웃 컴포넌트
│   │   ├── pages/             # 페이지 컴포넌트
│   │   │   ├── Dashboard/      # 대시보드
│   │   │   ├── AIRecommendation/ # AI 권고안
│   │   │   ├── Approval/       # 승인 프로세스
│   │   │   └── LogAudit/       # 로그 및 감사
│   │   └── App.tsx
│   ├── package.json           # Node.js 의존성
│   └── Dockerfile             # 프론트엔드 컨테이너
├── tests/                      # 테스트
│   ├── test_ai_service.py
│   ├── test_risk_analysis.py
│   └── test_midm_integration.py
├── scripts/                    # 유틸리티 스크립트
│   ├── setup_db.py
│   ├── start_services.py
│   └── deploy.py
├── docker-compose.yml          # 서비스 오케스트레이션
├── env.example                # 환경변수 예시
└── README.md                  # 프로젝트 문서
```

## 🚀 시작하기

### 1. 프로젝트 클론
```bash
git clone <repository-url>
cd forest-fire-ai-agent
```

### 2. 프론트엔드 실행 (MVP 데모)
```bash
cd frontend
npm install
npm start
```
- 브라우저에서 `http://localhost:3000` 접속

### 3. 전체 시스템 실행 (Docker)
```bash
# 환경변수 설정
cp env.example .env

# 서비스 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f
```

### 4. 믿:음 LLM 서버 설정
```bash
# 학교 서버에서 vLLM 실행
docker run --gpus all -p 8001:8000 \
  -e MODEL_NAME=K-intelligence/Midm-2.0-Base-Instruct \
  vllm/vllm-openai:latest \
  --model K-intelligence/Midm-2.0-Base-Instruct \
  --host 0.0.0.0 --port 8000
```

## 🎯 주요 기능

### 📊 실시간 대시보드
- **화재 알림**: 실시간 화재 감지 및 신뢰도 표시
- **센서 데이터**: 온도, 습도, 연기 농도, 풍속, 대기질 모니터링
- **CCTV 모니터링**: 용문산, 청편산 등 주요 지역 실시간 영상
- **지도 모니터링**: 위성 지도 기반 화재 위치 표시

### 🤖 AI 권고안 생성
- **믿:음 2.0 LLM**: 기관별 맞춤형 권고안 자동 생성
- **법령 기반**: 소방기본법, 재난관리법 등 관련 법령 참조
- **상세 분석**: 즉시 조치사항, 예상 비용/효과, 필요 자원 제시

### ✅ 승인 프로세스
- **권고안 검토**: 상세 내용 검토 및 승인/거부
- **이력 관리**: 승인 이력 및 코멘트 관리
- **실시간 업데이트**: 권고안 상태 실시간 반영

### 📋 로그 및 감사
- **활동 기록**: 시스템 사용자 활동 로그
- **시스템 메트릭**: 성능 및 상태 모니터링
- **감사 추적**: 모든 작업의 추적 가능성

## 🔧 환경 설정

### 환경변수 (.env)
```env
# 데이터베이스
DATABASE_URL=postgresql://user:password@localhost:5432/forest_fire_db
REDIS_URL=redis://localhost:6379

# 믿:음 LLM
MIDM_LLM_ENDPOINT=http://your-school-server:8001
MIDM_LLM_MODEL=K-intelligence/Midm-2.0-Base-Instruct
MIDM_LLM_TIMEOUT=60
MIDM_LLM_MAX_TOKENS=2048
MIDM_LLM_TEMPERATURE=0.7

# API 설정
API_V1_STR=/api/v1
SECRET_KEY=your-secret-key
```

## 📞 연락처
- **개발팀**: 단국대학교 컴퓨터공학과
- **이메일**: 32203919@dankook.ac.kr, kinglee4290@gmail.com
- **프로젝트**: 산불 대응 AI Agent 시스템 (믿:음 2.0 LLM 기반)