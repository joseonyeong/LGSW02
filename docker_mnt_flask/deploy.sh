#!/bin/bash

IMAGE_NAME="joseonyeong/my-flask-web"

# 1. 최신 태그 자동 추출 (old 제외)
# 1. 최신 태그 자동 추출
CURRENT_TAG=$(docker images ${IMAGE_NAME} --format "{{.Tag}} {{.CreatedAt}}" \
  | grep -v -E "^old|^latest" \
  | sort -rk2 | head -n1 | awk '{print $1}')

if [ -z "$CURRENT_TAG" ]; then
  echo "❌ ${IMAGE_NAME} 이미지가 존재하지 않습니다."
  exit 1
fi

echo "🧭 현재 최신 태그: ${CURRENT_TAG}"

# 2. 기존 태그 → old 태그로 백업
docker tag ${IMAGE_NAME}:${CURRENT_TAG} ${IMAGE_NAME}:old
echo "🔁 ${CURRENT_TAG} → old 태그 백업 완료"

# 3. 새 태그 입력
read -p "📦 새 버전(tag)을 입력하세요 (예: 1.0.1): " NEW_TAG

# 4. 새 태그 부여 및 푸시
docker tag ${IMAGE_NAME}:${CURRENT_TAG} ${IMAGE_NAME}:${NEW_TAG}
echo "🏷️ 새 태그 적용: ${IMAGE_NAME}:${NEW_TAG}"

docker push ${IMAGE_NAME}:${NEW_TAG}
echo "🚀 푸시 완료: ${IMAGE_NAME}:${NEW_TAG}"

# 5. 결과 요약
echo ""
echo "📌 태그 현황:"
docker images | grep $IMAGE_NAME | grep -E "old|${NEW_TAG}|${CURRENT_TAG}"

# 6. 컨테이너 이름 입력
read -p "🧱 새 컨테이너 이름을 입력하세요: " CONTAINER_NAME

# 7. 컨테이너 실행
echo ""
echo "🐳 컨테이너 실행 중..."
docker run --rm -it -p 5000:5000 \
  --name "$CONTAINER_NAME" \
  --mount type=bind,source="$(pwd)",destination=/app \
  -w /app \
  ${IMAGE_NAME}:${NEW_TAG}