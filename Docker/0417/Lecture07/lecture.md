# 호스트머신에서 로그 출력 설정 파일 만들기
# 설정 파일을 이미지에 복사
# 컨테이너가 실행되면 컨테이너 내부에서 복사한 파일에서 로그 출력

# 도커 이미지 빌드
```bash
docker image build --tag my-sql:log .
```
