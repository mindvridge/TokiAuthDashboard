#!/bin/bash

# Toki Auth Dashboard 배포 스크립트

set -e

echo "========================================"
echo "Toki Auth Dashboard - Cloud Run 배포"
echo "========================================"

# 프로젝트 설정
PROJECT_ID="keyboardai-473202"
SERVICE_NAME="toki-auth-dashboard"
REGION="asia-northeast3"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo ""
echo "프로젝트 ID: ${PROJECT_ID}"
echo "서비스 이름: ${SERVICE_NAME}"
echo "리전: ${REGION}"

# GCP 프로젝트 설정
echo ""
echo "[1/4] GCP 프로젝트 설정 중..."
gcloud config set project ${PROJECT_ID}

# Docker 이미지 빌드
echo ""
echo "[2/4] Docker 이미지 빌드 중..."
gcloud builds submit --tag ${IMAGE_NAME}:latest

# Cloud Run에 배포
echo ""
echo "[3/4] Cloud Run에 배포 중..."
gcloud run deploy ${SERVICE_NAME} \
  --image ${IMAGE_NAME}:latest \
  --region ${REGION} \
  --platform managed \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 5 \
  --no-allow-unauthenticated \
  --set-env-vars "API_BASE_URL=https://toki-auth-964943834069.asia-northeast3.run.app"

# 서비스 URL 가져오기
echo ""
echo "[4/4] 배포 완료! 서비스 정보 확인 중..."
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} --region ${REGION} --format 'value(status.url)')

echo ""
echo "========================================"
echo "배포가 성공적으로 완료되었습니다!"
echo "========================================"
echo ""
echo "서비스 URL: ${SERVICE_URL}"
echo ""
echo "⚠️  중요: 이 서비스는 인증이 필요합니다."
echo "접근 권한을 부여하려면 다음 명령어를 실행하세요:"
echo ""
echo "gcloud run services add-iam-policy-binding ${SERVICE_NAME} \\"
echo "  --region ${REGION} \\"
echo "  --member=\"user:your-email@gmail.com\" \\"
echo "  --role=\"roles/run.invoker\""
echo ""

