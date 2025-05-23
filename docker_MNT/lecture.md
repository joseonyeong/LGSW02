# ruby 관련 파일
- 파일명 : hello.rb

# 컨테이너 실행
```bash
# pwd는 현재경로
# 현재 경로 모든 file 복제해서 my-work에 넣음
$ docker container run --name ruby --rm --interactive --tty --mount type=bind,source="$(pwd)",destination=/my-work ruby:3.3.4 bash
```

