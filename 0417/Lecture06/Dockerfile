## Python 이미지 기반 (slim 형식)
FROM python:3.10-slim

## 작업 디렉터리 설정
WORKDIR /app

## 패키지 목록 복사 (requirements.txt에 복사)
COPY requirements.txt .

## 패키지 설치
# 위에서 python image를 설정했기 때문에 pip install을 사용할 수 있음
# --no-cache-dir : 적절하게 캐시 삭제한다.
RUN pip install --no-cache-dir -r requirements.txt