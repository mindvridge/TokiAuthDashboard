# Streamlit Community Cloud 배포 가이드 (완전 무료!)

## 🎯 Streamlit Community Cloud란?

Streamlit이 제공하는 **완전 무료 호스팅 서비스**입니다.
- 무료로 무제한 사용
- 자동 HTTPS
- GitHub 연동
- 간단한 설정

## 📋 사전 준비

### 1. GitHub 계정 생성
- https://github.com 에서 가입

### 2. GitHub 저장소 생성
```
저장소 이름: TokiAuthDashboard
공개 여부: Public (무료 플랜은 Public만 가능)
```

### 3. 코드 푸시
```powershell
cd C:\TokiAuthDashboard

# Git 초기화
git init

# GitHub 저장소와 연결
git remote add origin https://github.com/your-username/TokiAuthDashboard.git

# 파일 추가
git add .

# 커밋
git commit -m "Initial commit - Toki Auth Dashboard"

# 푸시
git push -u origin main
```

## 🚀 Streamlit Cloud 배포

### 1단계: Streamlit Community Cloud 접속
```
https://share.streamlit.io/
```

### 2단계: GitHub로 로그인
- "Continue with GitHub" 클릭
- GitHub 계정으로 로그인

### 3단계: 새 앱 배포
1. **"New app"** 버튼 클릭
2. 정보 입력:
   ```
   Repository: your-username/TokiAuthDashboard
   Branch: main
   Main file path: app.py
   ```
3. **"Deploy!"** 버튼 클릭

### 4단계: Secrets 설정 (중요!)
배포 후 Settings에서:

1. **"Advanced settings"** 클릭
2. **"Secrets"** 탭 선택
3. 다음 내용 입력:
   ```toml
   API_BASE_URL = "https://toki-auth-964943834069.asia-northeast3.run.app"
   ```
4. **"Save"** 클릭

### 5단계: 완료!
- 자동으로 URL 생성: `https://your-app-name.streamlit.app`
- 배포 완료까지 1-2분 소요

## 🔐 보안 설정

### 비밀 정보 보호

**중요**: JWT 토큰 등 민감한 정보는 코드에 포함하지 마세요!

**올바른 방법:**
1. Streamlit Secrets 사용
2. 사용자가 대시보드에서 직접 로그인
3. 세션에만 토큰 저장 (코드에는 저장 안 함)

### 접근 제한

Streamlit Community Cloud는 기본적으로 공개되므로:

**옵션 1: 코드에서 인증 구현**
```python
# 이미 구현되어 있음!
# utils/auth.py의 require_auth() 함수
```

**옵션 2: 비공개 URL 사용**
- Streamlit Cloud Settings에서 "Sharing" 설정
- URL을 공유하지 않으면 사실상 비공개

## ⚡ 자동 배포 설정

### GitHub에 푸시하면 자동 배포됨!
```powershell
# 코드 수정 후
git add .
git commit -m "Update dashboard"
git push

# Streamlit Cloud가 자동으로 감지하고 재배포
# 1-2분 후 변경사항 반영됨
```

## 📊 리소스 제한

Streamlit Community Cloud **무료 플랜**:
- ✅ 앱 개수: 무제한
- ✅ 리소스: 1GB RAM
- ✅ 저장소: Public GitHub만
- ✅ 트래픽: 제한 없음
- ✅ 동시 접속: 약 10-20명

**충분한 이유:**
- 관리자 대시보드는 동시 사용자가 적음
- 데이터 처리가 많지 않음
- API 호출이 주요 작업

## 🎯 단계별 실행

### 1. GitHub 저장소 준비
```powershell
cd C:\TokiAuthDashboard

git init
git add .
git commit -m "Initial commit"

# GitHub에서 저장소 생성 후
git remote add origin https://github.com/YOUR_USERNAME/TokiAuthDashboard.git
git push -u origin main
```

### 2. Streamlit Cloud 배포
1. https://share.streamlit.io/ 접속
2. GitHub로 로그인
3. "New app" 클릭
4. 저장소 선택 → Deploy!

### 3. Secrets 설정
```toml
API_BASE_URL = "https://toki-auth-964943834069.asia-northeast3.run.app"
```

### 4. 접속
`https://your-app-name.streamlit.app`

## 💡 팁

### 빠른 업데이트
```powershell
git add .
git commit -m "Update"
git push

# 자동으로 재배포됨!
```

### 로그 확인
- Streamlit Cloud 대시보드에서 "Manage app" → "Logs"

### 앱 재시작
- Streamlit Cloud 대시보드에서 "Reboot app"

---

**완전 무료로 프로덕션급 대시보드 호스팅!** 🎉

