# 베이스 이미지 지정하기
# FROM [--platform] <image>, ubuntu, python, mysql 입력 가능
FROM ubuntu:24.04

# runtime dependencies (용량 확보를 위해 설치 파일 삭제)

#### ---- 설치 확인 용도 ---- ####
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    vim \
    mysql-server \
    mysql-client \
    postgresql \
    postgresql-client \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*
