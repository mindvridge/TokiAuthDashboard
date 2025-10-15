# 🚀 Streamlit Cloud 배포 - 완벽 가이드

## ✅ 완료된 작업
- [x] 코드 작성 완료
- [x] Git 저장소 초기화
- [x] GitHub에 푸시 완료 ✅
  - Repository: https://github.com/mindvridge/TokiAuthDashboard

## 🌐 Streamlit Cloud 배포 (5분)

### Step 1: Streamlit Community Cloud 접속

**브라우저에서 접속:**
```
https://share.streamlit.io/
```

또는
```
https://streamlit.io/cloud
```

---

### Step 2: GitHub로 로그인

1. **"Continue with GitHub"** 버튼 클릭

2. GitHub 계정으로 로그인
   - 계정: `mindvridge`

3. **Authorize Streamlit** (권한 승인)
   - Streamlit이 GitHub 저장소에 접근할 수 있도록 허용
   - "Authorize streamlit" 클릭

---

### Step 3: 새 앱 배포

1. **"New app"** 버튼 클릭 (우측 상단)

2. **Deploy an app** 화면에서 입력:

   **Repository, branch, and file**
   ```
   Repository: mindvridge/TokiAuthDashboard
   Branch: main
   Main file path: app.py
   ```

   **App URL (Optional - 선택사항)**
   ```
   Custom subdomain: toki-auth-dashboard
   ```
   → 최종 URL: `https://toki-auth-dashboard.streamlit.app`

3. **Advanced settings** (선택사항 - 그냥 넘어가도 됨)
   - Python version: 3.11 (자동 감지됨)

4. **"Deploy!"** 버튼 클릭 🚀

---

### Step 4: 배포 진행 확인

**화면에 표시되는 내용:**

```
🔄 Installing packages...
   - streamlit
   - requests
   - pandas
   - plotly
   - ... (약 30초 소요)

🔄 Starting app...
   - Loading app.py
   - Initializing components
   - ... (약 10초 소요)

✅ Your app is live!
```

**배포 완료!** 🎉

---

### Step 5: Secrets 설정 (필수!)

배포가 완료되면:

1. **앱 화면 우측 하단** 또는 **왼쪽 상단 햄버거 메뉴 (☰)** 클릭

2. **"Settings"** 선택

3. **왼쪽 메뉴에서 "Secrets"** 선택

4. **Edit secrets** 클릭

5. **다음 내용 입력**:
   ```toml
   API_BASE_URL = "https://toki-auth-964943834069.asia-northeast3.run.app"
   ```

6. **"Save"** 버튼 클릭

7. **앱 자동 재시작** (10초 소요)

---

## 🎊 배포 완료!

### 대시보드 URL
```
https://toki-auth-dashboard.streamlit.app
```

또는 자동 생성된 URL:
```
https://tokiauthdashboard-[random].streamlit.app
```

---

## 🔐 대시보드 로그인

### 방법 1: API 문서에서 토큰 받기

1. **Toki Auth API 문서 접속**:
   ```
   https://toki-auth-964943834069.asia-northeast3.run.app/docs
   ```

2. **카카오 로그인 테스트**:
   - `POST /api/v1/auth/kakao/callback` 찾기
   - "Try it out" 클릭
   - Request body:
     ```json
     {
       "access_token": "실제_카카오_액세스_토큰"
     }
     ```
   - "Execute" 클릭

3. **응답에서 토큰 복사**:
   ```json
   {
     "access_token": "eyJhbGc...",  ← 복사
     "refresh_token": "eyJhbGc...", ← 복사
     "token_type": "bearer",
     "expires_in": 3600
   }
   ```

### 방법 2: 대시보드에서 로그인

1. **배포된 대시보드 접속**

2. **사이드바에서 로그인**:
   - "JWT 토큰 직접 입력" 선택
   - Access Token 붙여넣기
   - Refresh Token 붙여넣기
   - "로그인" 버튼 클릭

3. **✅ 로그인 성공!**

---

## 📊 사용 가능한 기능

### 대시보드 홈 (app.py)
- 📈 주요 통계 지표
- 🥧 OAuth 제공자 분포 차트
- 📉 일별 가입자 추이 그래프
- 👥 최근 가입 사용자 목록

### 사용자 관리
- 전체 사용자 목록
- 검색 및 필터링
- 사용자 상세 정보
- CSV 다운로드

### 통계
- 활성/비활성 사용자 차트
- 일별 가입자 분석
- OAuth 제공자 통계

### OAuth 계정
- 연동 계정 목록
- 제공자별 필터링

### 설정
- 계정 정보
- API 연결 상태
- 로그아웃

---

## 🔄 코드 업데이트 방법

코드를 수정한 후:

```powershell
cd C:\TokiAuthDashboard

git add .
git commit -m "Update dashboard"
git push

# Streamlit Cloud가 자동으로 감지하고 재배포!
```

---

## 📋 배포 체크리스트

- [x] GitHub 저장소 생성
- [x] 코드 푸시 완료
- [ ] Streamlit Cloud 로그인 (https://share.streamlit.io/)
- [ ] 새 앱 배포
- [ ] Secrets 설정 (API_BASE_URL)
- [ ] 대시보드 접속 테스트
- [ ] JWT 토큰으로 로그인
- [ ] 기능 테스트

---

**이제 https://share.streamlit.io/ 에서 배포를 진행하시면 됩니다!**

