import numpy as np
import openvino as ov
import time

# 결론: 내가 따로 드라이버 안깔아도 잘 되긴 한다.

from optimum.intel import OVModelForSequenceClassification
from transformers import AutoTokenizer
from openvino import Core

# 1. 모델 로드 + 변환
model_id = "distilbert-base-uncased"

model = OVModelForSequenceClassification.from_pretrained(
    model_id,
    export=True
)

# 2. NPU로 컴파일
model.compile(device="NPU")

# 3. tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_id)

# 4. 입력
inputs = tokenizer("Hello world!", return_tensors="pt")

# 5. 실행
outputs = model(**inputs)

# 6. 🔥 핵심: 실제 실행 디바이스 확인
print("Execution device:", model.model.get_property("EXECUTION_DEVICES"))