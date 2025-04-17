# 베이스 이미지 지정하기
# FROM [--platform] <image>, ubuntu, python, mysql 입력 가능
FROM ubuntu:24.04

## 1layer 이미지
RUN apt-get update && \
    apt-get install -y vim mysql-client postgresql-client && \
    rm -rf /var/lib/apt/lists/*

CMD ["bash"]


## 3layer 이미지
# # 인덱스 파일 취득
# RUN apt-get update
# # 필요한 리눅스 패키지 설치
# RUN apt-get install -y vim
# # 인덱스 파일 삭제
# RUN rm -rf /var/lib/apt/lists/*

