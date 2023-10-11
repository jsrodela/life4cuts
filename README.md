# 인생네컷
2023 잠신제 출품작 & 10월 이벤트

## To-do
- [ ] 사진 고르기
- [X] 화면 흐름 말끔하게 다듬기
- [X] utils 처리는 스레드 분리해서 웹소캣으로 통신
- [X] 마지막 안내 문구 수정 (나가서 프린트, 머리띠 반납, jamsin.tk에서 다운로드)
- [X] 영상 압축하기 (프레임 크기 조정)
- [X] 사진 합치기
- [X] jamsin.tk에 영상? 이미지? 올리고 QR코드 생성해서 이미지에 부착 (영상 올리고 QR 부착해서 출력)
- [X] 영상 저장
- [X] 영상 저장 프로세스
- [X] 카메라 시작한 다음에 켜지게 해도 될듯
- [X] 프린터 부분 제작
- [X] static => models 포함 전반적인 refactor

## 주요 모듈
- Django (웹서버)
- OpenCV2 (카메라 연결)
- Pillow (사진 합성)
- PyAutoGUI (인쇄 매크로)
- requests (클라이언트-프린터, 파일서버 연결)
- Websocket (프린터 웹소캣)

### 자료 출처
* 우주 사진: https://www.instagram.com/p/CxOmGSRs3d-/
* 엘리멘탈: https://theqoo.net/movie/2846249863
* 분홍 하늘: https://jib.transportkuu.com/2020/11/23/%ED%95%98%EB%8A%98-%EA%B3%A0%ED%99%94%EC%A7%88-%EC%BB%B4%ED%93%A8%ED%84%B0-%EB%B0%B0%EA%B2%BD-%ED%99%94%EB%A9%B4/
* 셔터 소리: https://pgtd.tistory.com/283

## 개발환경 설정

0. Python, vscode, git 설치

설치 안되어있는 것들만 설치하면 됩니다
* Python (>=3.10): https://www.python.org/downloads/
* Visual Studio Code: https://code.visualstudio.com/
* Git: https://git-scm.com/download/win

> 아래 명령어들은 vscode에서 Ctrl+J를 누르면 나오는 터미널 창에 입력하면 됩니다.

1. git clone
```commandline
git clone https://github.com/jsrodela/life4cuts
cd life4cuts
```

2. 필요 프로그램 설치
> Redis: WebSocket(실시간 통신)에 사용되는 프로그램

[//]: # (> CrhromDriver: Chrome의 기반이 되는 Chromium의 드라이버)

* [Redis for Windows](https://github.com/tporadowski/redis/releases) .msi 다운로드 후 실행

[//]: # (* [ChromeDriver]&#40;https://sites.google.com/chromium.org/driver/downloads&#41; zip 압축 해제하여 chromedriver.exe 파일을 프로젝트 폴더에 넣기)

3. 가상환경 생성
> Pycharm에서는 대신 우측 아래의 `<No Interpreter>`를 눌러 가상 환경을 생성할 수 있습니다.
```commandline
python -m venv .venv
```

아래 명령어로 가상환경에 진입해준다. (터미널 껐다 킬 때마다 해야함. 이거 귀찮으면 pycharm 쓰는게 좋음)
```commandline
cmd
cd .venv/Scripts
activate.bat
```

4. 의존 모듈 설치
```commandline
pip install -r requirements.txt
```

5. DB 설정
```commandline
python manage.py migrate
```

6. settings.json 작성

클라이언트의 경우:
```json
{
  "type": "client",
  "chroma": true,
  "print_server": "http://example.com"
}
```

프린터의 경우:
```json
{
  "type": "printer",
  "print_server": "http://example.com"
}
```

7. 서버 실행

클라이언트의 경우:
```commandline
python manage.py runserver
```

프린터의 경우:
```commandline
python manage.py runserver 0.0.0.0:8000
```
