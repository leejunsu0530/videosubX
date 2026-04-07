"""내가 원래 pwcpp 클래스를 상속하고 거기서 모델만 바꿔서 재정의하면 
다른 내부 함수를 그대로 쓸 수 있지 않을까?"""

import _pywhispercpp as pwcpp
# import pywhispercpp


# print(pwcpp.__file__)
# >> C:\Users\leeju\Projects\videosubX\.venv\Lib\site-packages\_pywhispercpp.cp313-win_amd64.pyd

print(dir(pwcpp)) # 바인딩 된 함수들

# ctx = pwcpp.whisper_init_from_file('path/to/ggml/model')
