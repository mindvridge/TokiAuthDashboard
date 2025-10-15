# Cloud Run 배포 가이드 (무료 티어 활용)

## 💰 Cloud Run 무료 티어

Google Cloud Run은 **매월 무료 할당량**을 제공합니다:

- ✅ **요청**: 월 2백만 건 무료
- ✅ **CPU**: 월 180,000 vCPU-초
- ✅ **메모리**: 월 360,000 GiB-초
- ✅ **네트워크**: 월 1GB 송신 무료

**대시보드는 내부용이므로 무료 티어로 충분합니다!**

## 🚀 배포 방법

### PowerShell 스크립트 사용 (권장)

```powershell
cd C:\TokiAuthDashboard

# 1. Docker 이미지 빌드 (Cloud Build 사용)
gcloud builds submit --tag gcr.io/keyboardai-473202/toki-auth-dashboard

# 2. Cloud Run 배포
gcloud run deploy toki-auth-dashboard `
  --image gcr.io/keyboardai-473202/toki-auth-dashboard:latest `
  --region asia-northeast3 `
  --platform managed `
  --memory 512Mi `
  --cpu 1 `
  --max-instances 3 `
  --min-instances 0 `
  --timeout 300 `
  --no-allow-unauthenticated `
  --set-env-vars "API_BASE_URL=https://toki-auth-964943834069.asia-northeast3.run.app"
```

### 접근 권한 설정

**관리자에게만 접근 권한 부여:**
```powershell
# 본인 이메일로 변경
gcloud run services add-iam-policy-binding toki-auth-dashboard `
  --region asia-northeast3 `
  --member="user:your-email@gmail.com" `
  --role="roles/run.invoker"

# 팀원 추가
gcloud run services add-iam-policy-binding toki-auth-dashboard `
  --region asia-northeast3 `
  --member="user:teammate@gmail.com" `
  --role="roles/run.invoker"
```

## 💰 비용 절감 팁

### 1. 최소 인스턴스 0으로 설정
```powershell
--min-instances 0
```
- 사용하지 않을 때 자동으로 종료
- 비용 $0
- 콜드 스타트: 5-10초 (괜찮음)

### 2. 최대 인스턴스 제한
```powershell
--max-instances 3
```
- 관리자 대시보드는 동시 사용자가 적음
- 3개면 충분

### 3. 타임아웃 설정
```powershell
--timeout 300  # 5분
```
- 장시간 유휴 시 자동 종료

### 4. 리소스 최적화
```powershell
--memory 512Mi  # 512MB면 충분
--cpu 1         # 1 vCPU
```

## 📊 예상 비용 (관리자 대시보드)

### 사용 패턴
- 접속: 하루 10회
- 세션 시간: 평균 5분
- 월 접속: 약 300회

### 계산
```
월 요청: 300회 × 10 API calls = 3,000회
CPU 시간: 300회 × 5분 × 1 vCPU = 1,500분 = 90,000 vCPU-초
메모리: 300회 × 5분 × 0.5GB = 750분 = 22.5 GiB-초

무료 한도:
- 요청: 2,000,000회 (3,000회 사용, 0.15%)
- CPU: 180,000 vCPU-초 (90,000초 사용, 50%)
- 메모리: 360,000 GiB-초 (22.5초 사용, 0.006%)

결론: 완전 무료! 🎉
```

## 🔒 보안 강화 옵션

### 옵션 1: Cloud Run 인증 (권장)
```powershell
--no-allow-unauthenticated
```
- Google 계정으로만 접근 가능
- IAM 정책으로 특정 사용자만 허용
- 추가 비용: $0

### 옵션 2: VPN 연동
```powershell
# VPC 네트워크 설정
--vpc-connector=your-vpc-connector
```
- 회사 VPN에서만 접근
- 추가 비용: 약 $10/월

### 옵션 3: Identity-Aware Proxy (IAP)
- Google 계정 + 추가 인증
- 추가 비용: $0

## 🆚 Streamlit Cloud vs Cloud Run

| 항목 | Streamlit Cloud | Cloud Run |
|------|----------------|-----------|
| **가격** | 무료 | 무료 (한도 내) |
| **설정 난이도** | ⭐ 매우 쉬움 | ⭐⭐ 쉬움 |
| **배포 속도** | GitHub push → 자동 | 수동 명령어 |
| **접근 제어** | URL 공유 제한 | IAM 정책 |
| **커스터마이징** | 제한적 | 완전 제어 |
| **리소스** | 1GB RAM | 커스터마이징 |

---

## 🎯 최종 추천

### **무료로 시작: Streamlit Community Cloud**

**이유:**
1. ✅ 완전 무료
2. ✅ 가장 간단 (GitHub push만 하면 됨)
3. ✅ 충분한 성능
4. ✅ 자동 배포

**단점을 감수할 수 있다면:**
- Public GitHub 저장소 필요
- 민감한 정보는 Secrets로 관리

---

### **더 나은 보안: Cloud Run (무료 티어)**

**이유:**
1. ✅ 무료 (예상 사용량으로 무료 티어 내)
2. ✅ IAM 기반 접근 제어
3. ✅ Private GitHub 가능
4. ✅ GCP 생태계 통합

**단점:**
- 설정이 약간 더 복잡

---

## 🚀 즉시 실행 가능한 배포 명령어

### 방법 1: Streamlit Cloud (추천!)

**3분 안에 배포:**

```powershell
cd C:\TokiAuthDashboard

# 1. GitHub 저장소 생성 (GitHub.com에서)
# 2. Git 초기화 및 푸시
git init
git add .
git commit -m "Toki Auth Dashboard"
git remote add origin https://github.com/YOUR_USERNAME/TokiAuthDashboard.git
git push -u origin main

# 3. Streamlit Cloud 접속
# https://share.streamlit.io/
# - "New app" 클릭
# - 저장소 선택
# - Deploy!

# 4. Secrets 설정 (앱 Settings에서)
# API_BASE_URL = "https://toki-auth-964943834069.asia-northeast3.run.app"
```

**완료!** 🎉
- URL: `https://your-app.streamlit.app`
- 비용: $0

---

### 방법 2: Cloud Run (무료 티어)

**5분 안에 배포:**

```powershell
cd C:\TokiAuthDashboard

# 1. Docker 이미지 빌드
gcloud builds submit --tag gcr.io/keyboardai-473202/toki-auth-dashboard

# 2. 배포
gcloud run deploy toki-auth-dashboard `
  --image gcr.io/keyboardai-473202/toki-auth-dashboard:latest `
  --region asia-northeast3 `
  --platform managed `
  --memory 512Mi `
  --cpu 1 `
  --max-instances 3 `
  --min-instances 0 `
  --no-allow-unauthenticated `
  --set-env-vars "API_BASE_URL=https://toki-auth-964943834069.asia-northeast3.run.app"

# 3. 접근 권한 부여
gcloud run services add-iam-policy-binding toki-auth-dashboard `
  --region asia-northeast3 `
  --member="user:your-email@gmail.com" `
  --role="roles/run.invoker"
```

**완료!** 🎉
- URL: `https://toki-auth-dashboard-[hash].run.app`
- 예상 비용: $0 (무료 티어 내)

## 🔥 초저비용 대안들

### Render (Free Tier)
```
- 무료: 750시간/월
- 자동 슬립: 15분 비활성 시
- URL: https://your-app.onrender.com
```

### Railway (Hobby Plan)
```
- $5/월
- 자동 배포
- URL: https://your-app.up.railway.app
```

### Heroku (Eco Dyno)
```
- $5/월
- 간편한 CLI
- URL: https://your-app.herokuapp.com
```

## 💡 최종 결론

**관리자 대시보드는 사용량이 적으므로:**

1. **Streamlit Community Cloud** (무료) - 첫 시작 추천! ⭐⭐⭐⭐⭐
2. **Cloud Run** (무료 티어) - 더 나은 보안 필요 시 ⭐⭐⭐⭐
3. 로컬 실행 - 개인 사용

**제 추천: Streamlit Community Cloud로 시작하세요!**
- 완전 무료
- 가장 간단
- 충분한 성능
- 나중에 Cloud Run으로 마이그레이션 가능

배포 방법을 선택하시면 단계별로 도와드리겠습니다! 🚀

