from typing import Type, Any
from dataclasses import dataclass


class _Sentinel:
    """
    foo: int | _Sentinel = UNSET 형태로 사용
    UNSET 객체: 프로젝트 전체에서 센티널은 이 센티널 객체만 써야 == 연산자로 같다고 나옴.
    None과 혼동될 일이 없는 경우는 그냥 None 사용
    is로 비교
    """
    __slots__ = ()  # 이 객체에는 s.x=10 등으로 속성을 추가할 수 없다.

    def __repr__(self) -> str:
        return "UNSET"


UNSET = _Sentinel()


@dataclass(slots=True)  # 아래의 type_ 등을 __slots__로 변환
class ParameterSpec:
    type_: Type | _Sentinel = UNSET
    default: Any | _Sentinel = UNSET
    description: str = "No description given."
    choices: list[Any] | None = None
    range: tuple[Any, Any] | None = None
