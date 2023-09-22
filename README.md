# 인생네컷
2023 잠신제 출품작

## To-do
- [X] 사진 합치기
- [ ] 화면 흐름 말끔하게 다듬기
- [ ] jamsin.tk에 영상? 이미지? 올리고 QR코드 생성해서 이미지에 부착 (QR이 먼저냐 이미지가 먼저냐..?)
- [ ] utils 처리는 스레드 분리해서 웹소캣으로 통신
- [ ] 영상 저장
- [ ] 마지막 안내 문구 수정 (나가서 프린트, 머리띠 반납, jamsin.tk에서 다운로드)
- [ ] 카메라 시작한 다음에 켜지게 해도 될듯
- [ ] 사진 고르기
- [ ] 프린터 부분 제작
- [ ] static => models 포함 전반적인 refactor

## 주요 모듈
- Django (웹서버)
- OpenCV2 (카메라 연결)
- Pillow (사진 합성)
- PyAutoGUI (인쇄 매크로)

## 개발환경 설정

0. Python, vscode, git 설치

설치 안되어있는 것들만 설치하면 됩니다
* Python: https://www.python.org/downloads/
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

5. 서버 실행
```commandline
python manage.py runserver
```
