# 잠신네컷
2023 잠신제 출품작 & 10월 이벤트

2023년 잠신제 출품을 위해 시작한 프로젝트이며, 10월 중간고사 후 중앙현관에서 잠신네컷 행사를 진행하였다.

## 주요 모듈
- Django (웹서버)
- OpenCV2 (카메라 연결)
- Pillow (사진 합성)
- PyAutoGUI (인쇄 매크로)
- requests (클라이언트-프린터, 파일서버 연결)
- websocket (프린터 웹소캣)
- qrcode (QR코드 생성)
- webbrowser (사진 파일 열기)

## 코드 흐름
### 클라이언트 (사진 부스)
사진 부스의 노트북에서 실행되는 사실상의 메인 앱! `clientapp`

1. 인원수 선택 (start)
* 클라이언트 `/startpage`: 사용자가 인원수 선택 후 '시작하기' 버튼 클릭
* 새로운 Cut 모델 생성
* 이전 촬영에서 사용된 자원 모두 정리

2. 배경 선택 (bg)
* 클라이언트 `/background`: 사용자가 배경 클릭
* 카메라 스레드 `consumers.cam_while()` 시작
  * 이때부터 연결된 카메라의 실시간 화면을 받아와서 `/ws/cam` 주소로 base64/png 형식으로 계속 쏴줌
  * 동시에 프레임들을 별개의 리스트에 저장해서, 나중에 동영상 스레드에서 영상 제작에 사용하도록 모아둠
  * 카메라 관련 코드는 `utils/webcam.py`에 있음. `opencv` 모듈 사용.
* 영상 공유코드 스레드 `consumers.manage_code()` 시작
  * `https://jamsin.tk/pre_code`로 요청 보내서, 파일 공유코드만 미리 받아오기
  * 받아온 공유코드는 Cut에 저장
  * jamsin.tk와 통신 관련 기능은 `utils/send_video.py`에 있음
* 만약 settings.json에서 `chroma=false`라면 이 단계 스킵

3. 촬영 (cam)
* 클라이언트 `/cam`
  * `/ws/cam`에서 사진 받아와서 실시간으로 표시.
  * 10초 카운트 후, 서버로 `cap` 메세지 보내고 찰칵소리 재생. 서버에서 사진 처리 후 `resume` 메세지 받으면 다시 10초 카운트 시작.
  * 6장 다 찍었으면 서버로 `end` 메세지 보내고, 다시 서버에서 `end` 메세지 돌아오면 다음 단계로 이동.
* 카메라 스레드는 상시 돌아가는 중
  * 클라이언트에서 `cap` 메세지 받으면 잠깐 카메라 기능이 멈춤 (의도한게 아니라 기술적 딜레이인데, 클라이언트에서 화면 멈추는건 은근 나쁘지 않았음)
  * 현재 프레임을 Cut에 저장하고, 보정 작업 시행.
    * 크로마키 배경때문에 사진이 너무 초록초록해져서, 사진에서 초록 비율 10% 감소
    * 밝기를 전체적으로 10% 올림 (보정 빡세게 걸어준다고 좋아했음)
    * settings.json에서 크로마키 설정되어 있으면 크로마키 효과 적용. 아래의 조건 중 하나 이상 만족하는 픽셀을 지움.
      * 하나의 픽셀은 빛의 3원색인 `Red`, `Green`,`Blue`로 표현됨. 각 변수는 0~255 사이의 값을 가짐.
      * 조건 1. `Green-Red > 25` 이고 `Green-Blue > 25` : 초록색 배경 감지
      * 조건 2. `Green >= 250`이고 `Green-Red > 25` : 조명 때문에 밝기가 밝아지면 흰색에 가까워질 때가 있는데, 이러면 G와 R/B의 차이가 작아지는 경향이 있음. 따라서 Green이 250 이상인 경우 조명 때문에 밝아진걸로 보고, `Green-Red>25`로 '원래 하얀' 픽셀이 아님을 감지.
      * 조건 3. `Green >= 150`이고 `Green-Red > 100` : 커다란 선글라스 소품을 사용하는 경우, 선글라스에 가려진 배경은 오히려 검은색에 가까워짐. 따라서 위와 같은 이유로 Green이 150 이상인 경우 선글라스 때문에 어두워진걸로 보고, `Green-Red>100`으로 '원래 어두운' 픽셀이 아님을 감지.
    * 보정 코드는 `utils/chroma.py`에 있음. `pillow` 모듈 사용.
    * 보정 결과물을 Cut에 저장하고, 클라이언트로 `resume` 메세지 전송 후 카메라 기능 계속.
  * 클라이언트에서 `end` 메세지 받으면 동영상 스레드 시작 후 `end` 메세지 다시 보내고, 카메라 스레드 종료
    * 동영상 스레드 `consumers.manage_video()`
    * 카메라 스레드에서 저장해둔 프레임들을 영상으로 조합하여, 이름이 '잠신네컷.mp4'인 동영상을 제작
    * 영상 제작 후 프레임을 비우고, `https://jamsin.tk/post_file`에 영상을 업로드함. 공유코드는 아까 배경 선택에서 이미 받아둠.
    * 영상 제작 코드는 `utils/make_video.py`에 있음. `opencv` 모듈 사용.
    * 영상 업로드 코드는 `utils/send_video.py`에 있음.

4. 프레임 선택 (frame)
* 클라이언트 `/framechoose`: 사용자가 프레임 선택
* 카메라 스레드 종료

5. 로딩 (load)
* 클라이언트 `/loading`
  * 로딩이 너무 오래걸려서 만들어진 화면. 전날 새벽에 급하게 부랴부랴 만든 애니메이션이 일품!
  * `/ws/loading` 연결해서 진행상황 실시간으로 표시하다가, 100% 되면 다음 단계로 이동.
* 로딩 스레드 `consumers.manage_loading()` 시작
  * 사진 6장 모두 준비될 때까지 대기
  * 사진 6장 + 프레임 = 1개의 사진으로 합성 (result.png)
    * 각 사진을 배경 프레임의 칸에 맞는 비율로 잘라서 부착
    * 동영상 QR코드 생성해서 오른쪽 하단에 배치
  * 프린터 서버로 사진 전송
  * 위 단계들 진행하면서 계속 각 단계별 안내 문구 클라이언트로 발송 (`consumers.loading_update`)
  * 사진 합성 코드는 `utils/combine_photo.py`에 있음. `pillow` 모듈 사용.
  * QR코드 제작은 `utils/qr.py`에 있음. `qrcode` 모듈 사용.

6. 마무리 (end)
* 클라이언트 `/end`: 완성된 사진 화면에 표시, 돌아가기 누르면 처음으로 이동
* 완성된 사진 찾아서 base64/png로 전송

### 클라이언트-프린터 서버
클라이언트에서 온 사진을 프린터로 보내주는, 중간 다리 역할을 해주는 서버! `printapp`

* 사진 수신 (`/send_print`)
  * 클라이언트에서 받은 사진을 그대로 프린터로 전송

### 프린터
프린터에 연결된 노트북에서 실행될 코드 `print_websocket.py`

* `settings.json`에서 설정된 주소인 클라이언트-프린트 서버에 `/ws/print`로 웹소캣 연결
* 웹소캣 데이터가 들어올 때마다 작업목록 리스트에 쌓아두고, 별개의 스레드에서 하나씩 순차적으로 실행
  * 받은 사진(base64/png)을 'print.png' 파일로 저장
  * print.png 파일 열어서, 인쇄 매크로 실행. (인쇄 매크로는 Windows 10/11의 '사진' 앱을 기준으로 설정됨)
  * Ctrl+P -> 사진 장수 입력 -> 출력 -> 창 닫기
* 웹소캣 통신은 `websocket` 모듈 사용.
* 프린트 매크로 코드는 `utils/printer.py`에 있음. `pyautogui` 및 `webbrowser` 모듈 사용.

## 개선할 점
잠신네컷을 잠신제 직전까지 만들다가 실패하고, 10월 이벤트도 중간고사 바로 다음날 이었던지라... 만들면서, 혹은 이벤트 진행하면서 시간이 있었으면 개선할 수 있었을텐데 하면서 아쉬웠던 점들을 여기에 적어둡니다

* 렉
  * 원래 우리학교 학생용 노트북 사양이 안좋기도 하고... 그래서 렉이 좀 많이 걸림. 알다시피 부스에서 실시간으로 OutOfMemoryError 뜬 적도 있고.
  * 공유코드를 pre_code와 post_file로 나눠두는 이유는, 영상 제작이 너무 오래걸림ㅜㅜ 현장에서 약 2분정도 걸리는듯. 그래서 QR코드가 먼저 만들어질 수 있도록 공유코드만 미리 받아두고, 영상은 나중에 합성되는 대로 업로드하도록 짜여짐.
  * 영상 스레드같이 오래걸리는 스레드들은 아예 프로세스(Process)로 분리해도 좋을듯. 파이썬의 `multithreading`은 병렬 연산을 지원하지 않음 (스레드가 아님!) Process로 해야 듀얼코어 사용할꺼임 아마.
  * [ ] 아니면 영상 만드는거를 한번에 하지 말고, 각 frame 받아올때마다 video.write() 한번씩 실행해도 나쁘지 않을듯. 오 이게 더 좋겠다.
  * [ ] 특히 pillow나 opencv, 또는 base64 쓰는 과정에서 일단 작동되게 하려고 비효율적으로 짠 코드들이 꽤 있을거임. 포멧을 변경한다던지 등으로 이런 비효율성 없애면 성능 향상 가능할듯.
* 인터넷
  * 영상 업로드하는 시간도 꽤 걸림. 영상이 약 50MB정도 되는데, 중앙현관 senWiFi_Free 드럽게 느림. 그래서 중간부터는 핸드폰으로 핫스팟 켜서 씀.
  * [ ] 영상 화질을 약간 낮추는 것도 방법일듯? 하루필름도 화질 꽤 낮더라. 근데 이러면 화질 바꾸는 연산이 추가되니까 로딩시간이 더 걸릴수도오...
  * 특히 학교 인터넷에서는 서버를 열었을 때 외부에서 접속이 불가능해서, 프린터 서버를 Azure로 외부에 따로 만들 수밖에 없었음. (내부 아이피로 접속하려고 해도 자주 끊김)
* [ ] 지금 카메라로 찍히는 사진은 16:9인데, 배경 프레임의 각 사진 칸 비율하고 안맞아서 가로 양옆이 짤림. 이거 비율 조정해야함!!
* [ ] startpage에서 인원수 입력 안하고 바로 시작하기 누르면 장고 에러 화면 뜸. 시작하기 눌렀을 때 숫자 입력된거 맞는지 js로 한번 확인하고 넘어가면 좋을듯.
* [ ] 10초 카운트가 잘 보이지 않는다는 의견 있었음. HTML에서 더 잘 보이게 바꾸면 좋을듯.
* [ ] 프린터(`print_websocket.py`)에서 혹시 인쇄 안된 사진 있으면 바로 찾아서 뽑아줄 수 있도록, 'print.png'가 아니라 공유코드를 파일이름으로 각각 다르게 저장해놔도 좋을듯.
* [ ] 크로마키를 굳이 사진 찍을때마다 바로 처리하는 이유는, 원래는 다 찍고 난 다음에 프레임에 미리 합성해서 클라이언트에 보여주려 했었음. 시간 관계상 넣지는 못한 기능인데, 중간에 잠깐 로딩 화면 만들어서 해도 좋을듯!
* [ ] jamsin.tk에서 공유코드가 도착하지 않았는데 넘어가서, 영상 없이 프린트해주는 경우가 있었음. 공유코드 스레드에서 `Cut.video_code가` `None`인지로 확인하지 말고, 기본값 999999인지를 확인해야함. 코드 도착하지 않았을 경우에 어떻게 할지도 대비해야 할듯. (처음부터 다시 시작?)
* [ ] 코드를 잘 찾아보면 '잠신네컷.mp4'나 'jamsin.tk'와 같은, 코드에 섞여있는 설정값들이 있을거임. 이런 변동적인 값들은 setting.json에서 직접 정할 수 있도록 하기... 쉽게 변할 수 있는 설정값들이 코드에 직접 입력되어있는건 좋지 않음 ([참고: Config Files](https://youtu.be/jaX9zrC7y4Y))
* [ ] `views.end()`에서 Status를 LOAD로 하도록 오타 나있는듯. END로 바꿔주기.
* [ ] 애니메이션 개선해도 좋을듯! 중간고사 끝나고 이벤트 전날 새벽에 겨우 만든거라... ㄹㅇ UI만 이뻐도 사용자 만족도 떡상함
* [ ] `main/settings.py`에서 `settings.json`의 `type`에 따라 `INSTALLED_APPS` 변경하도록 하기. 둘다 로드하는건 좀 비효율적인듯. 추가로 세 영역의 코드가 지금 뚜렷하게 나뉘어있지 않은데, 구분 좀 해둬도 좋을듯.
* [ ] 마지막에 준우가 프레임 약간 수정해서 보내준거 있는데, 그거 테스트 안해봄 ㅋㅋ큐ㅠㅠㅠ 커밋은 올려두었으니 운용 전 테스트 한번 해보기!
* 사진에서 초록 비율 10% 낮추는거, settings.json에서 `chroma=false`라면 안해도 될듯.
* 클라이언트로 화면 보내는거를 base64/png로 하는것보다, 동영상 스트림 하나 만들어도 좋을듯. 사진 보내는건 넘 비효율적... 근데 지금도 충분히 잘 되긴함ㅎ
* 크로마키 조건 2,3에서 G-R만 봐도 되는건지 모르겠음. G-B는 확인 안해봐도 되나..? 사소한 거지만 시간나면 함 테스트해보삼!

### 자료 출처
* 우주 사진: https://www.instagram.com/p/CxOmGSRs3d-/
* 엘리멘탈: https://theqoo.net/movie/2846249863
* 분홍 하늘: https://jib.transportkuu.com/2020/11/23/%ED%95%98%EB%8A%98-%EA%B3%A0%ED%99%94%EC%A7%88-%EC%BB%B4%ED%93%A8%ED%84%B0-%EB%B0%B0%EA%B2%BD-%ED%99%94%EB%A9%B4/
* 셔터 소리: https://pgtd.tistory.com/283

## 필요 품목
- 사진 부스
  - 카메라 (과학교육부 대여)
  - 노트북 (과학교육부 대여)
  - 조명 (과학교육부 대여)
  - 파티션 (인문사회부 대여)
  - 크로마키 or 배경지 (메이커실 보관)
  - 캡쳐보드(HDMI in to USB out) (메이커실 or 과학교육부)
  - 젠더(HDMI in to Mini HDMI out) (과학교육부 대여, 카메라랑 같이 있음)
- 인화 부스
  - 노트북 1대 (과학교육부 대여)
  - 프린터(G2060) (창의체험부 대여 - 2023 잠신제 로델라 예산으로 구매)
  - 광택용지(GP-508) (구매 필요 - 메이커실에 20장정도 있음)
  - 사진 보관용 비닐(OPP봉투 비접착식, 11x15cm) (구매 필요 - 메이커실에 조금 있음)
  - 잉크(GI-990BK/C/M/Y) (프린터 박스에 같이 들어있음)
- 기타
  - 클라이언트-프린터 연결 서버 (Azure)
  - jamsin.tk에서 pre_code 및 post_file 기능 활성화

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

클라이언트-프린터 연결 서버의 경우:
```json
{
  "type": "client"
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

클라이언트-프린터 연결 서버의 경우:
```commandline
python manage.py runserver 0.0.0.0:8000
```

프린터의 경우:
```commandline
python print_websocket.py
```
