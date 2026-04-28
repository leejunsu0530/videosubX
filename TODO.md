# TOC
- [TODO](#TODO)
- [전사 파이프라인](#전사-파이프라인)
    - [오디오 로딩](#오디오-로딩)
    - [VAD](#vad)
    - [배치 전사](#배치-전사)
    - [강제 정렬](#강제-정렬)
    - [화자 분리](#화자-분리)
- [whisper 모델 성능 개선](whisper-모델-성능-개선)
    - [가속 방법](#가속-방법)
    - [파인튜닝](#파인튜닝)
        - [어댑터(lora)](#어댑터lora)
        - [kotoba-whisper](#kotoba-whisper)
        - [distil-whisper](#distil-whisper)
    - [양자화](#양자화)
- [번역](#번역)
- [기타](#기타)

---

# TODO
- 

---
# 전사 파이프라인
- 전사 파이프라인 만들기: 메모리 고려한 로딩, VAD, 배치 전사, 강제 정렬, 화자 분리

## 오디오 로딩
- 메모리를 고려하는 로딩 필요. 너무 크면 터지니까.
- vad를 거친 후에야 문장이 잘리지 않게 할 수 있음.

## VAD

## 배치 전사
- 사용 고려 중인 엔진: hf, pwcpp, wx, faster, ~~insanely~~(이건 분석은 해보겠지만 그냥 hf 최적화인듯)

## 강제 정렬

## 화자 분리

---

# whisper 모델 성능 개선
- 일단 hf는 복잡해서 보류. 특히 optimum intel은. 

## 가속 방법
일단 NPU는 사용 실패.
- ctranslate2
- optimum(ct2와 양립 불가) -> intel or cuda 둘다 가능.
    - intel cpu 말고 xpu 사용 
- onnx
- ggml > pwcpp
- 양자화
- torch의 intel 또는 cuda
- ~~파인튜닝(kotoba를 사용해서? https://ysg2997.tistory.com/53 참고)~~ 사실 이건 가속은 아니지. 중첩되니까.
- accelerate (?)
- flash_attention_2 (?)

참고:

```python
# insanely-faster-whisper에 있는 허깅페이스의 코드.
    model_kwargs={"attn_implementation": "flash_attention_2"} if is_flash_attn_2_available() else {"attn_implementation": "sdpa"},
```

## 파인튜닝
1. kotoba를 어떻게든 가볍게 만듦
2. 어댑터를 적용함
3. 데이터셋을 사용하는 양자화로 각 체크포인트를 int8 양자화함
4. ct2 변환
**주의: 양자화는 lora 효과를 감소시킴. 특히 여러 겹일때는.**
작게 모델을 만들면 int8 필요 없을지도?

### 어댑터(LoRA)
일본어 모델에 구어체 어댑터, 특정 인물 어댑터 차례대로 적용

### kotoba-whisper
> 참고: https://github.com/kotoba-tech/kotoba-whisper

1. kotoba 더 최적화(더 잘라내기?)
2. 작은 모델(base, small)로 다시 학습
참고로 ct2 변환에 특정 파일들 만드는 명령어 없으면 터진다.

### distil-whisper
영어만 가능함. [hf hub](https://huggingface.co/distil-whisper) 참고.

## 양자화
ct2는 자체 양자화 된다.

---

# 번역
- mbart, marian, nllb, JapaneseBart 등으로 품질 테스트, 일본어 구어체 튜닝 + 특정 인물/도메인 튜닝. 
- marianMT는 새 언어쌍 만들려면 몇백~몇천만 문장 데이터셋이 필요하다 함.
- nllb 또는 mbart + lora fine-tuning + int8로 사용
- 구글, deepl, gpt 지원

---

# 기타

## 이미지 처리 관련
- [ ] paddleocr 기반 이미지/영상 자막 생성 지원

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


