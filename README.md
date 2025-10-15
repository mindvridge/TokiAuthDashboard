# Toki Auth Dashboard

Toki Auth Service의 관리자 대시보드입니다. 사용자 정보 조회, 통계 확인 등의 관리 기능을 제공합니다.

## 🎯 주요 기능

- **📊 대시보드 홈**: 주요 통계 및 지표 한눈에 보기
- **👥 사용자 관리**: 전체 사용자 목록 조회 및 검색
- **📈 통계**: 일별 가입자 추이, OAuth 제공자별 통계
- **🔗 OAuth 계정**: OAuth 연동 계정 관리
- **⚙️ 설정**: 계정 정보 및 API 연결 설정

## 🚀 로컬 실행

### 1. 패키지 설치
```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정
`.env.example`을 복사하여 `.env` 파일 생성:
```bash
cp .env.example .env
```

또는 Streamlit Secrets 사용:
```bash
mkdir .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

실제 값으로 수정:
```toml
API_BASE_URL = "https://toki-auth-964943834069.asia-northeast3.run.app"
```

### 3. 실행
```bash
streamlit run app.py
```

브라우저에서 자동으로 http://localhost:8501 열림

## 🔐 로그인 방법

### 방법 1: JWT 토큰 직접 입력 (권장)

1. Toki Auth 서비스에서 카카오/구글로 로그인
2. 받은 JWT access_token과 refresh_token 복사
3. 대시보드 사이드바에서 토큰 입력

### 방법 2: OAuth 로그인

1. 사이드바에서 "카카오 로그인" 또는 "구글 로그인" 클릭
2. 로그인 완료 후 토큰 복사
3. 토큰을 사이드바에 입력

## ☁️ Cloud Run 배포

### Docker 이미지 빌드 및 배포

```bash
# 프로젝트 ID 설정
PROJECT_ID="keyboardai-473202"
SERVICE_NAME="toki-auth-dashboard"
REGION="asia-northeast3"

# Docker 이미지 빌드
gcloud builds submit --tag gcr.io/${PROJECT_ID}/${SERVICE_NAME}

# Cloud Run 배포
gcloud run deploy ${SERVICE_NAME} \
  --image gcr.io/${PROJECT_ID}/${SERVICE_NAME}:latest \
  --region ${REGION} \
  --platform managed \
  --memory 512Mi \
  --cpu 1 \
  --set-env-vars "API_BASE_URL=https://toki-auth-964943834069.asia-northeast3.run.app"
```

### 인증 설정 (중요!)

대시보드는 관리자만 접근해야 하므로:

```bash
# 인증 필요하도록 설정
gcloud run deploy ${SERVICE_NAME} \
  --region ${REGION} \
  --no-allow-unauthenticated
```

접근 권한 부여:
```bash
# 특정 사용자에게 권한 부여
gcloud run services add-iam-policy-binding ${SERVICE_NAME} \
  --region ${REGION} \
  --member="user:your-email@gmail.com" \
  --role="roles/run.invoker"
```

## 📂 프로젝트 구조

```
TokiAuthDashboard/
├── app.py                      # 메인 페이지 (대시보드 홈)
├── requirements.txt
├── Dockerfile
├── README.md
├── .gitignore
├── components/
│   ├── __init__.py
│   └── sidebar.py             # 사이드바 (로그인/네비게이션)
├── utils/
│   ├── __init__.py
│   └── auth.py                # 인증 유틸리티
├── pages/
│   ├── 1_👥_Users.py          # 사용자 목록
│   ├── 2_📊_Statistics.py     # 통계
│   ├── 3_🔗_OAuth.py          # OAuth 계정
│   └── 4_⚙️_Settings.py       # 설정
└── .streamlit/
    ├── config.toml
    └── secrets.toml.example
```

## 🔗 연결 구조

```
Toki Auth Dashboard (Streamlit)
        ↓ REST API 호출
Toki Auth Service (FastAPI)
        ↓ 데이터 조회
PostgreSQL / SQLite
```

## 📡 사용하는 API 엔드포인트

- `GET /api/v1/auth/me` - 현재 사용자 정보
- `GET /api/v1/admin/users` - 사용자 목록
- `GET /api/v1/admin/users/{id}` - 사용자 상세
- `GET /api/v1/admin/stats` - 전체 통계
- `GET /api/v1/admin/stats/daily` - 일별 통계
- `GET /api/v1/admin/stats/providers` - 제공자별 통계
- `GET /api/v1/admin/oauth-accounts` - OAuth 계정 목록

## 🛠 개발

### 로컬 개발 환경
```bash
# 가상 환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt

# 개발 모드 실행
streamlit run app.py --server.runOnSave=true
```

## 📄 라이선스

MIT License

