# 인생네컷
2023 잠신제 출품작

## 주요 모듈
- Django (웹서버)
- OpenCV2 (카메라 연결)
- PySide6 (프린터 연결)

## 개발환경 설정

1. git clone
```commandline
git clone https://github.com/jsrodela/life4cuts
cd life4cuts
```

2. Redis 설치
> Redis: WebSocket(실시간 통신)에 사용되는 프로그램

[Redis for Windows](https://github.com/tporadowski/redis/releases) .msi 다운로드 후 실행

3. 가상환경 생성 및 모듈 설치
> Pycharm에서는 대신 우측 아래의 `<No Interpreter>`를 눌러 가상 환경을 생성할 수 있습니다.
```commandline
python -m venv .venv
pip install -r requirements.txt
```

4. 서버 실행
```commandline
python manage.py runserver
```
