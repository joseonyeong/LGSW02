# 파일구조
```bash
$ tree
.
├── app.py
├── lecture.md
└── templates
    └── index.html
```

# 컨테이너 실행
- ip: 127.0.0.1
- port: 5000
에서 실행

```bash
$ docker container run \
> --rm \
> -it \
> --publish 5000:5000 \
> --mount type=bind,source="$(pwd)",destination=/app \
> -w /app \
> python:3.10-slim \
> bash -c "pip install flask && python app.py"
```

# 도커파일
```bash
FROM python:3.10-slim

WORKDIR /app

RUN pip install flask

CMD ["python", "app.py"] 
```

# 이미지 생성
```bash
$ docker image build --tag joseonyeong/my-flask-web:1.0.0 /
```

## 컨테이너 실행
- 반드시 Dockfile에 기재한 WORKDIR와 동일한 destination 경로 설정
```bash
docker container run --rm -it -p 5000:5000 --mount type=bind,source="$(pwd)",destination=/app joseonyeong/my-flask-web:1.0.0
```