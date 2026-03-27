# 아래는 가상환경 코드
Write-Host "[Command]: py -3.13 -m venv .venv" -BackgroundColor White -ForegroundColor Blue
py -3.13 -m venv .venv
Write-Host "[Command]: .venv/scripts/activate" -BackgroundColor White -ForegroundColor Blue
.venv/scripts/activate
Write-Host "[Command]: python.exe -m pip install --upgrade pip uv" -BackgroundColor White -ForegroundColor Blue
python.exe -m pip install --upgrade pip uv
Write-Host "[Command]: python -m uv pip install -U -e .[intel]" -BackgroundColor White -ForegroundColor Blue
python -m uv pip install -U -e .[intel]