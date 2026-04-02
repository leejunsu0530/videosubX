# https://huggingface.co/docs/optimum-intel/en/openvino/optimization
# 이걸로 데이터 없이 양자화
from optimum.intel import OVModelForCausalLM, OVWeightQuantizationConfig
from pathlib import Path

save_dir = Path('.ov_models/quantized_tinyllama')

if not save_dir.exists():
    OVModelForCausalLM.from_pretrained(
        'TinyLlama/TinyLlama-1.1B-Chat-v1.0',
        quantization_config=OVWeightQuantizationConfig(bits=8)
    ).save_pretrained(str(save_dir))
else: # 모델 불러오기
    model = OVModelForCausalLM.from_pretrained(str(save_dir))
    
