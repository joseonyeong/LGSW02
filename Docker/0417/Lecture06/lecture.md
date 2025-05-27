ENV TZ=Asia/Seoul <==> SET time_zoone == 'Asia/Seoul'

## 호스트 머신의 파일을 복사해서 이미지 or 컨테이너 내부로 전달
- 명령어 예시 : hostfile.txt .
- 명령어 예시 : hostfile.txt /var/log/
    -> 파일 경로 이해가 필요

- requirements.txt 라이브러리는 도커파일 안에서 설치한다.

# 파이썬 이미지 생성
```bash
docker image build --tag my-python:install .
```

# 파이썬 컨테이너 생성 후 , bash
- 버전 확인
```bash
docker container run --name pytest -it my-python:install bash
```
```python
root@8d73b482409e:/# pwd
/
root@8d73b482409e:/# python3
Python 3.10.17 (main, Apr  9 2025, 18:21:43) [GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import pandas as pd
>>> pd.__version__
'2.2.3'
>>> import seaborn as sns
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ModuleNotFoundError: No module named 'seaborn'
```