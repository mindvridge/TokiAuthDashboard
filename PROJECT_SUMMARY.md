# Toki Auth Dashboard - 프로젝트 요약

## 📌 프로젝트 개요

**Toki Auth Dashboard**는 Toki Auth Service의 관리자 대시보드입니다. Streamlit으로 구축되었으며, REST API를 통해 사용자 정보와 통계를 조회합니다.

## 🏗 아키텍처

```
┌─────────────────────────────────────┐
│  Toki Auth Dashboard (Streamlit)    │
│  - 사용자 관리                       │
│  - 통계 및 차트                      │
│  - OAuth 계정 관리                   │
└──────────────┬──────────────────────┘
               │ REST API (JWT 인증)
               ▼
┌─────────────────────────────────────┐
│  Toki Auth Service (FastAPI)        │
│  - Admin API 제공                    │
│  - JWT 토큰 검증                     │
└──────────────┬──────────────────────┘
               │ Database Query
               ▼
┌─────────────────────────────────────┐
│  PostgreSQL / SQLite                │
│  - 사용자 데이터                     │
│  - OAuth 연동 정보                   │
└─────────────────────────────────────┘
```

## 📂 프로젝트 구조

```
TokiAuthDashboard/
├── app.py                      # 메인 페이지 (대시보드 홈)
├── requirements.txt            # Python 패키지
├── Dockerfile                  # Docker 이미지 빌드
├── deploy.sh                   # 배포 스크립트
├── env.example                 # 환경 변수 예시
├── .gitignore                  # Git 제외 파일
│
├── components/                 # UI 컴포넌트
│   ├── __init__.py
│   └── sidebar.py              # 로그인 및 네비게이션
│
├── utils/                      # 유틸리티
│   ├── __init__.py
│   └── auth.py                # 인증 및 API 호출
│
├── pages/                      # 멀티페이지
│   ├── 1_👥_Users.py          # 사용자 목록
│   ├── 2_📊_Statistics.py     # 통계
│   ├── 3_🔗_OAuth.py          # OAuth 계정
│   └── 4_⚙️_Settings.py       # 설정
│
├── .streamlit/                 # Streamlit 설정
│   ├── config.toml
│   └── secrets.toml.example
│
├── README.md                   # 프로젝트 문서
├── QUICKSTART.md               # 빠른 시작 가이드
└── PROJECT_SUMMARY.md          # 이 파일
```

## 🔑 주요 기능

### 1. 대시보드 홈
- 주요 통계 지표 (전체/활성 사용자, 오늘 가입자 등)
- OAuth 제공자별 분포 차트 (파이차트, 바차트)
- 최근 30일 가입자 추이 그래프
- 최근 가입 사용자 목록

### 2. 사용자 관리
- 전체 사용자 목록 조회
- 이메일/이름 검색
- 활성화 상태 필터링
- 페이지네이션
- 사용자 상세 정보 조회
- CSV 내보내기

### 3. 통계
- 활성/비활성 사용자 파이차트
- 활성 사용자 비율 게이지
- OAuth 제공자별 통계
- 일별 가입자 추이 (커스터마이징 가능)
- 누적 가입자 그래프

### 4. OAuth 계정 관리
- OAuth 연동 계정 목록
- 제공자별 필터링
- 연동 계정 통계
- CSV 내보내기

### 5. 설정
- 계정 정보 표시
- API 연결 상태 확인
- 토큰 정보 및 유효성 확인
- 로그아웃

## 🔐 인증 방식

### JWT 토큰 기반 인증

1. **사용자가 Toki Auth Service에서 로그인**
   - 카카오 또는 구글 OAuth 사용
   - JWT 토큰 발급받음

2. **대시보드에서 토큰 입력**
   - 사이드바에서 access_token과 refresh_token 입력
   - 세션에 저장

3. **API 요청 시 토큰 자동 포함**
   - 모든 API 요청에 `Authorization: Bearer {token}` 헤더 추가
   - 401 에러 시 자동 로그아웃

## 📡 사용하는 API 엔드포인트

### 인증 API
- `GET /api/v1/auth/me` - 현재 사용자 정보 (토큰 검증)

### 관리자 API
- `GET /api/v1/admin/users` - 사용자 목록
- `GET /api/v1/admin/users/{id}` - 사용자 상세
- `GET /api/v1/admin/stats` - 전체 통계
- `GET /api/v1/admin/stats/daily` - 일별 통계
- `GET /api/v1/admin/stats/providers` - 제공자별 통계
- `GET /api/v1/admin/oauth-accounts` - OAuth 계정 목록
- `GET /api/v1/admin/health` - 헬스 체크

## 🛠 기술 스택

- **Streamlit 1.29.0**: 웹 프레임워크
- **Plotly**: 인터랙티브 차트
- **Pandas**: 데이터 처리
- **Requests**: HTTP 클라이언트

## ☁️ 배포 정보

### 배포 대상
- **플랫폼**: Google Cloud Run
- **프로젝트**: keyboardai-473202
- **서비스명**: toki-auth-dashboard
- **리전**: asia-northeast3 (서울)

### 배포 방법
```powershell
# Docker 빌드 및 배포
gcloud builds submit --tag gcr.io/keyboardai-473202/toki-auth-dashboard

# Cloud Run 배포
gcloud run deploy toki-auth-dashboard \
  --image gcr.io/keyboardai-473202/toki-auth-dashboard:latest \
  --region asia-northeast3 \
  --platform managed \
  --memory 512Mi \
  --cpu 1 \
  --no-allow-unauthenticated \
  --set-env-vars "API_BASE_URL=https://toki-auth-964943834069.asia-northeast3.run.app"
```

### 보안 설정
```powershell
# 특정 사용자에게만 접근 권한 부여
gcloud run services add-iam-policy-binding toki-auth-dashboard \
  --region asia-northeast3 \
  --member="user:your-email@gmail.com" \
  --role="roles/run.invoker"
```

## 🎯 주요 차이점: Toki Auth vs Dashboard

| 항목 | Toki Auth Service | Toki Auth Dashboard |
|------|------------------|---------------------|
| **목적** | 인증 서비스 | 관리자 대시보드 |
| **프레임워크** | FastAPI | Streamlit |
| **접근 권한** | 공개 (안드로이드 앱) | 제한 (관리자만) |
| **주요 기능** | OAuth 로그인, JWT 발급 | 사용자 조회, 통계 |
| **데이터 접근** | 직접 DB 접근 | REST API 호출 |
| **배포 방식** | `--allow-unauthenticated` | `--no-allow-unauthenticated` |

## 📊 주요 화면

### 대시보드 홈
- 주요 지표 카드 (4개)
- OAuth 제공자 파이차트
- 일별 가입자 라인차트
- 최근 가입자 테이블

### 사용자 관리
- 검색 및 필터
- 페이지네이션
- 사용자 상세 정보
- CSV 다운로드

### 통계
- 활성/비활성 파이차트
- 활성률 게이지
- 제공자별 바차트
- 일별 추이 라인/영역 차트

## 🔧 커스터마이징

### 차트 색상 변경
```python
# app.py에서 color_discrete_map 수정
color_discrete_map={
    "카카오": "#FEE500",  # 노란색
    "구글": "#4285F4"     # 파란색
}
```

### 통계 기간 변경
```python
# pages/2_📊_Statistics.py
days_range = st.slider("조회 기간 (일)", 7, 90, 30)
```

## 💡 유용한 명령어

```powershell
# 로컬 실행
streamlit run app.py

# 포트 변경
streamlit run app.py --server.port 8502

# 디버그 모드
streamlit run app.py --logger.level=debug

# 자동 새로고침 활성화
streamlit run app.py --server.runOnSave=true
```

## 📝 개발 팁

1. **세션 상태 초기화**: 사이드바에서 "Clear cache" 클릭
2. **API 응답 확인**: 브라우저 개발자 도구 → Network 탭
3. **에러 추적**: Streamlit 로그 확인

---

**Toki Auth Dashboard** - 간편하고 직관적인 사용자 관리 솔루션

