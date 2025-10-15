# Toki Auth Dashboard - 빠른 시작 가이드

## 🚀 로컬에서 실행하기

### 1. 패키지 설치
```powershell
# 가상 환경 생성 (선택사항)
python -m venv venv
.\venv\Scripts\Activate.ps1

# 패키지 설치
pip install -r requirements.txt
```

### 2. 환경 변수 설정
```powershell
# env.example 복사
Copy-Item env.example .env

# .env 파일 수정
# API_BASE_URL은 이미 올바르게 설정되어 있음
```

### 3. Streamlit 실행
```powershell
streamlit run app.py
```

브라우저가 자동으로 열립니다: http://localhost:8501

## 🔐 로그인 방법

### 방법 1: JWT 토큰 직접 입력 (권장)

1. **Toki Auth 서비스에서 로그인**
   - 카카오 또는 구글로 로그인
   - https://toki-auth-964943834069.asia-northeast3.run.app/docs

2. **JWT 토큰 복사**
   - `access_token`과 `refresh_token` 복사

3. **대시보드 사이드바에 입력**
   - 사이드바에서 "JWT 토큰 직접 입력" 선택
   - 토큰 붙여넣기
   - "로그인" 버튼 클릭

### 방법 2: API 테스트 (Postman 사용)

1. Postman에서 카카오 로그인:
   ```
   POST https://toki-auth-964943834069.asia-northeast3.run.app/api/v1/auth/kakao/callback
   Content-Type: application/json
   
   {
     "access_token": "카카오_액세스_토큰"
   }
   ```

2. 응답에서 받은 JWT 토큰 사용

## 📱 페이지 구성

- **🏠 대시보드 홈**: 주요 통계 및 차트
- **👥 사용자 관리**: 전체 사용자 목록 및 검색
- **📊 통계**: 일별 가입자 추이, OAuth 통계
- **🔗 OAuth 계정**: OAuth 연동 계정 관리
- **⚙️ 설정**: 계정 정보 및 API 설정

## 🧪 테스트

대시보드가 정상 작동하는지 확인:

1. 로그인 성공 확인
2. 대시보드 홈에서 통계 표시 확인
3. 사용자 목록 페이지 확인
4. 차트가 제대로 렌더링되는지 확인

## ⚠️ 문제 해결

### "API 연결 실패" 에러
- Toki Auth 서비스가 실행 중인지 확인
- API_BASE_URL이 올바른지 확인

### "인증이 필요합니다" 에러
- JWT 토큰이 만료되었을 수 있음
- 다시 로그인하여 새 토큰 받기

### 페이지가 로드되지 않음
- 브라우저 콘솔에서 에러 확인
- `streamlit run app.py --logger.level=debug`로 실행

## 📚 추가 문서

- **README.md**: 전체 프로젝트 개요
- **deploy.sh**: Cloud Run 배포 스크립트

