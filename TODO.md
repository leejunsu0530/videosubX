
## TODO
- 전사 base 만들기
- whisper나 kotoba, 양자화 등은 hf에서도 되니까 pwcpp에서 온전히 사용 못하면 이쪽으로
- diarize 모델과 vad 각각 구현

## whisper 관련 메모
TODO:
1. whisper의 NPU 지원 테스트. 이게 안되면 뒤에 과정 필요없이 whisper.cpp나 faster-whisper로.
> **시도해봤는데 안돼서 xpu 넣고 해보고, 나오는 성능과 저울질해서 whisperx나 pwcpp int8 멀티스레딩과 비교할듯**
2. 벤치마킹으로 tiny, base, ..., turbo 실 수치 확인. 가장 적합한 모델을 골라야 함
3. 코토바 데이터로 whisper 파인튜닝
4. 중오: diarize npu지원 확인

일단 hf의 whisper를 기본으로 해서 제작. 가능한 최적화:
- ctranslate2
- optimum(ct2와 양립 불가)
- onnx
- 양자화
- 파인튜닝(kotoba를 사용해서? https://ysg2997.tistory.com/53 참고)

> distill-whisper는 영어만 지원함

> 엔비디아가 되면 그냥 다른 cuda 지원 구현들을 쓰면 되고, hf에서 날것 그대로 쓰는 건 optimum의 ov 지원을 위해서다.

npu에서 whisper 지원 x면 pipe 따로 만들지 말고 whisperx에서 내가 학습시킨 코토바 넣고 사용. 더 성능을 높일 수 없으면 저 파이프라인이 최선이니까. faster-whisper의 whispermodel을 상속한 whisperx의 모델 클래스는 경로로 지정이 가능함.

## 전사 관련
- [ ] Base에서 asr, vad, 화자분리, 강제정렬을 별도 클래스로 만들고 Base를 파이프라인으로 만들어서 조립
- [ ] asr은 whisperx, hf(+intel optimum), faster-whisper, whisper.cpp 지원
- [ ] 파인튜닝, 양자화 지원

### 번역 관련
- [ ] hf 기반 번역기 지원
- [ ] 파인튜닝, 양자화 지원
- [ ] 구글, deepl, marianMT, NLLB, MBart 등 다양한 번역기 지원

### 이미지 처리 관련
- [ ] paddleocr 기반 이미지/영상 자막 생성 지원

### 기타
- [ ] cuda 지원
- [ ] pypi 지원

## yt-dlp 관련
- [x] 플레이리스트를 개별 영상 파일들로 쪼개기
- [x] pp에 인자 전달 방법 및 기본 시점 정의하는 방법 찾기
- [ ] cli to api 몽키패치 해결    
- [ ] optparse로 ytdlp의 인자 설명 추가
- [ ] 커스텀 pp, 필터 추가
    - [ ] 챕터별 썸네일 pp
    - [ ] 자동자막 생성 pp
    - [ ] 챕터 자동 생성 pp 및 사용자 지정 챕터 삽입 pp
- [ ] 더 빠른 info 다운로드(멀티스레딩)
- [ ] 다운로드 중 유튜브 차단이 걸리면 해당 프로세스를 종료하고 다른 프로세스에서 이어감
- [ ] exe 파일로 사용할 경우에 라이브러리 업데이트가 안되니까, 외부 ytdlp 경로와 연결 가능하게 하기
- [ ] 버전 확인 및 업데이트 스크립트
- [ ] 외부 경로 쪽 관리 스크립트

