# 디버깅으로 따라가볼까
from whisperx import load_model
model = load_model('tiny', 'cpu', 
                   compute_type='int8', 
                   
                   )

model.