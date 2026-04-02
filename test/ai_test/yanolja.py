import json
import torch
from transformers import AutoTokenizer
from optimum.intel import OVModelForCausalLM
from optimum.intel import OVQuantizer
from pathlib import Path
from time import time

time_start = time()
# No OpenVINO files were found for yanolja/YanoljaNEXT-Rosetta-4B-2511,
# setting `export=True` to convert the model to the OpenVINO IR.
# Don't forget to save the resulting model with `.save_pretrained()`
model_id = "yanolja/YanoljaNEXT-Rosetta-4B-2511"
model_path = Path(__file__).resolve().parent / ".ov_models" / model_id.split("/", 1)[-1].lower()

if model_path.exists():
    model = OVModelForCausalLM.from_pretrained(
        str(model_path),
        # device = "NPU",
    )
else:
    model = OVModelForCausalLM.from_pretrained(model_id, export=True)
    model.save_pretrained(str(model_path))
tokenizer = AutoTokenizer.from_pretrained(str(model_path))

model.to("NPU")
time_load = time()

target_language = "Korean"
context = {
    "context": "Simple introduction about a tech company.",
    "tone": "Informative and helpful",
    "glossary": {
        "Yanolja NEXT": "야놀자넥스트",
        "travel industry": "여행 산업",
    }
}

system = [f"Translate the user's text to {target_language}."]
for key, value in context.items():
    key_pascal = key.capitalize()
    if isinstance(value, dict):
        system.append(f"{key_pascal}:")
        for f, t in value.items():
            system.append(f"- {f} -> {t}")
    else:
        system.append(f"{key_pascal}: {value}")

system.append("Output format: JSON")
system.append(
    "Provide the final translation immediately without any other text.")

source = {
    "company_name": "Yanolja NEXT",
    "description": "Yanolja NEXT is a company that provides cutting-edge "
    "technology for the global travel industry.",
}

messages = [
    {"role": "system", "content": "\n".join(system)},
    {"role": "user", "content": json.dumps(source, ensure_ascii=False)},
]

prompt = tokenizer.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True)
print(prompt)
# <bos><start_of_turn>instruction
# Translate the user's text to Korean.
# Context: Simple introduction about a tech company.
# Tone: Informative and helpful
# Glossary:
# - Yanolja NEXT -> 야놀자넥스트
# - travel industry -> 여행 산업
# Output format: JSON
# Provide the final translation immediately without any other text.<end_of_turn>
# <start_of_turn>source
# {"company_name": "Yanolja NEXT", "description": "Yanolja NEXT is a company that provides cutting-edge technology for the global travel industry."}<end_of_turn>
# <start_of_turn>translation

inputs = tokenizer(prompt, return_tensors="pt").to("cpu")
input_length = inputs["input_ids"].shape[1]

with torch.inference_mode():
    outputs = model.generate(
        **inputs,
        max_new_tokens=64,
        use_cache=True,
    )

generated_tokens = outputs[0][input_length:]
translation = tokenizer.decode(generated_tokens, skip_special_tokens=True)

print(json.dumps(json.loads(translation), indent=2, ensure_ascii=False))
# {
#   "company_name": "야놀자넥스트",
#   "description": "야놀자넥스트는 글로벌 여행 산업에 최첨단 기술을 제공하는 회사입니다."
# }
time_finish = time()
print(f"Time to load model: {time_load - time_start:.2f} seconds\n"
      f"Time to generate translation: {time_finish - time_load:.2f} seconds\n"
      f" (total: {time_finish - time_start:.2f} seconds)")