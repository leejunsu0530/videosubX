# translate-video

오디오를 전사하고, 이미지와 오디오의 텍스트를 번역하여 ass 자막파일로 만들거나 영상에 삽입하는 파이썬 라이브러리
A bundle of diverse features: whisper based transcription, translation, OCR, video download and manage
<!--여기 toc와 작동가능 환경 등 표시하는 스크립트 만들기-->
<!--i18n으로 자동번역 추가-->
## features

1. [WhisperX](https://github.com/m-bain/whisperX) 기반 오디오 전사
2. [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)을 통한 비디오 텍스트 검출 및 인식
3. HuggingFace Hub 및 api 기반 번역기를 통한 다국어 텍스트 번역
4. 생성, 번역 결과를 원본 비디오의 글자를 impaint하고 삽입하거나, .ass 형식의 자막 파일로 생성

## Installation

### External Dependencies
yt-dlp를 위해서 FFmpeg, FFprove, Deno를 설치해야 한다.
> **중요 이슈**: 현재(2026.03.05) 기준 최신 whisperx 버전은 3.8.1인데, 이 버전에선 torch를 2.8 버전으로 강제한다. pyannote에서 발생하는 의존성 문제를 해결하기 위해 ffmpeg는 DLL이 있는 full-shared로 설치해야 하며 해당 torch 버전에 맞게 torchcodec과 ffmpeg의 버전을 각각 0.7과 7로 고정해야 한다. torch와 torchcodec의 호환 버전의 경우는 [여기](https://www.gyan.dev/ffmpeg/builds/)를 참고.
      
#### FFmpeg & FFprove 설치
FFprove는 FFmpeg를 설치하면 같이 설치된다.
Windows에서는 아래의 명령어로 설치할 수 있다.

<details>
   <summary><s>기존 설치 방법</s></summary>
   
   ```powershell
   
    # on Windows using Chocolatey (https://chocolatey.org/)
    choco install ffmpeg
    # on Windows using Scoop (https://scoop.sh/)
    scoop install ffmpeg
   
   ```
   yt-dlp는 FFmpeg의 일부 버그를 수정한 [빌드](https://github.com/yt-dlp/FFmpeg-Builds#ffmpeg-static-auto-builds)를 제공한다. 해당 링크에서 다운받는 것이 더 원할한 동작을 지원할 수 있다.
</details>

full-shared 버전으로, 버전을 7.X로 고정해서 설치하는 방법:
```powershell
# windows 11 이상에서는 winget이 기본으로 설치되어 있다.
winget install "FFmpeg (Shared)" --version 7.1.1
```

위의 명령어에 실패하면 수동 설치를 할 수도 있다. [Windows builds from gyan.dev](https://www.gyan.dev/ffmpeg/builds/) 또는 [Windows builds by BtbN](https://github.com/BtbN/FFmpeg-Builds/releases)에 들어가서 압축 파일을 다운받아 원하는 폴더에 압축 해제하고 해당 폴더 내 bin 폴더를 시스템 환경변수의 Path에 설정하면 된다.

#### Deno 설치
Deno는 yt-dlp의 JS 관련 의존성인 [yt-dlp-ejs](https://github.com/yt-dlp/ejs)의 의존성으로, 링크에서 알 수 있듯이 Node, Bun, QuickJS로 대체 가능하지만 Deno가 추천된다.
[Deno 설치 안내](https://docs.deno.com/runtime/getting_started/installation/)에서 설치 방법을 알 수 있다. Windows의 경우에는 아래 명령어로 설치한다.

```powershell
# Using PowerShell (Windows):
irm https://deno.land/install.ps1 | iex

# Using Scoop:
scoop install deno

# Using Chocolatey:
choco install deno
```

추가 정보는 yt-dlp의 [Wiki](https://github.com/yt-dlp/yt-dlp/wiki/EJS)를 참조하라.
  

### Installing Dependency Library
다른 종속성 라이브러리는 이 라이브러리에서 자동으로 설치하지만 paddlepaddle과 torch는 최상의 결과를 위해서 수동 설치가 필요하다.

#### paddlepaddle 설치
[공식 사이트 설치 가이드](https://www.paddlepaddle.org.cn/en/install/quick?docurl=/documentation/docs/en/develop/install/pip/windows-pip_en.html)에서 자신의 환경에 맞게 설정하면 설치 명령어가 아래와 같이 나온다.

```powershell
python -m pip install paddlepaddle==3.2.2 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/
```    

#### torch 설치
자신에게 맞는 index url을 지정해서 설치하면 된다. 예를 들어, Intel GPU를 사용할 경우에는 아래 명령어를 사용하면 된다.
      
```powershell
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/xpu
```

### Installing translate-video

> 추후 pypi에서도 지원할 예정임

```powershell
python -m pip install git+https://github.com/leejunsu0530/translate-video
```

설치해야 할 의존성이 많아서 오래 걸리기 때문에 pip 대신 Rust 기반인 [uv](https://github.com/astral-sh/uv)를 사용하는 걸 추천한다.
```powershell
# python -m pip install uv
python -m uv pip install git+https://github.com/leejunsu0530/translate-video
```

업데이트는 다음과 같이 한다.
```powershell
python -m uv pip install -U git+https://github.com/leejunsu0530/translate-video
```

## Usage
1. pip로 설치해서 엔트리포인트로 vidsubx --arg...로 실행. 또는 vidsubx-gui로 실행
2. 제공하는 exe 설치관리자로 설치 및 기본폴더 생성
### python
### GUI(Gradio)

## TODO
- [ ] cli to api 몽키패치 해결
- [ ] yt dlp 인자 파싱, regex 해석 > help, 구문강조 구현
- torchcodec 오류 해결 

- [ ] paddleocr 기반 이미지/영상 자막 생성 지원
- [ ] 구글, deepl, marianMT, NLLB, MBart 등 다양한 번역기 지원
- [ ] cuda 지원
- [ ] pypi 지원
- [ ] Gradio 기반 GUI 지원
- [ ] faster-whisper, whisper.cpp 추가 지원
- [ ] 전사 부분에 인자 추가 지원
------
### yt-dlp 부분 TODO
- [ ] gradio 기반 gui
    - [ ] 챕터 수정용 gui
    - [ ] 다운로드 형식 선택기
    - [ ] 구간 선택기
    - [ ] 챕터 생성기
    - [ ] ffmpeg 계열 gui(메타데이터 수정 등)
- [ ] optparse로 ytdlp의 인자 설명 추가
- [ ] 다운받은 파일의 메타데이터 열람 및 수정
- [ ] 커스텀 pp, 필터 추가
    - [ ] 챕터별 썸네일 pp
    - [ ] 자동자막 생성 pp
    - [ ] 챕터 자동 생성 pp 및 사용자 지정 챕터 삽입 pp
    - [ ] 
- [ ] 챕터별 썸네일 pp, 자동자막 생성 pp 등 추가
- [ ] 자체 파일탐색기 - 조건을 통한 파일 탐색, 파일들의 폴더 관리, 엘범 등의 메타데이터 관리 
- [ ] 더 빠른 info 다운로드(멀티스레딩)
- [ ] 다운로드 중 유튜브 차단이 걸리면 해당 프로세스를 종료하고 다른 프로세스에서 이어감
- [ ] 플레이리스트를 개별 영상 파일들로 쪼개기
- [ ] pp에 인자 전달 방법 및 기본 시점 정의하는 방법 찾기

## License
이 프로젝트는 MIT 라이선스 하에 보호받고 있습니다. 자세한 정보는 LICENSE 파일을 참조하세요.

This project is licensed under the MIT License.
See the LICENSE file for details.

