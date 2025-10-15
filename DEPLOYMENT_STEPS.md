# 🚀 Streamlit Cloud 배포 - 실행 단계

## ✅ 현재 완료된 작업
- [x] Git 저장소 초기화
- [x] 모든 파일 커밋 완료
- [x] 코드 준비 완료

## 📋 다음 실행할 명령어

### 1. GitHub 저장소 생성
브라우저에서 https://github.com/new 접속 후 저장소 생성

### 2. Git Remote 추가 및 Push
```powershell
# YOUR_USERNAME을 본인의 GitHub 사용자명으로 변경!
git remote add origin https://github.com/YOUR_USERNAME/TokiAuthDashboard.git
git branch -M main
git push -u origin main
```

### 3. Streamlit Cloud 배포
1. https://share.streamlit.io/ 접속
2. "Continue with GitHub" 클릭
3. "New app" 클릭
4. 설정:
   ```
   Repository: YOUR_USERNAME/TokiAuthDashboard
   Branch: main
   Main file path: app.py
   ```
5. "Deploy!" 클릭

### 4. Secrets 설정
앱 배포 후 Settings → Secrets에 추가:
```toml
API_BASE_URL = "https://toki-auth-964943834069.asia-northeast3.run.app"
```

### 5. 로그인 테스트
1. 배포된 대시보드 접속
2. 사이드바에서 로그인
3. Toki Auth에서 받은 JWT 토큰 입력

## 🔑 JWT 토큰 받는 방법

### API 문서 사용:
https://toki-auth-964943834069.asia-northeast3.run.app/docs

1. "/api/v1/auth/kakao/callback" 또는 "/api/v1/auth/google/callback" 선택
2. "Try it out" 클릭
3. 카카오/구글 액세스 토큰 입력
4. Execute
5. 응답에서 access_token과 refresh_token 복사

## 📌 중요 정보

### GitHub 저장소 URL 형식
```
https://github.com/YOUR_USERNAME/TokiAuthDashboard
```

### Streamlit 배포 URL 형식
```
https://tokiauthdashboard-YOUR_USERNAME.streamlit.app
```
또는
```
https://YOUR_APP_NAME.streamlit.app
```

## 🆘 문제 해결

### GitHub 인증 오류
- Personal Access Token 필요
- https://github.com/settings/tokens 에서 생성
- 권한: `repo` 전체 선택

### Streamlit Cloud 배포 실패
- requirements.txt 확인
- Python 버전 호환성 확인
- Logs에서 에러 메시지 확인

---

**GitHub 저장소를 생성하신 후, 명령어를 실행해주세요!**

