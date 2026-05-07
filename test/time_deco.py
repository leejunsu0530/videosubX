"""
- 보통 __name__을 쓰나?
- f"{__name__}func_output"은 함수 자체 이름도 뜨게 하기
- 반복시에 첫번째 결과만 출력하게 하기
- 각 반복의 시간도 출력하게 하기
"""
from functools import wraps
from typing import Callable, ParamSpec, TypeVar
import time
import logging
from contextlib import redirect_stdout
from io import StringIO

P = ParamSpec("P")
T = TypeVar("T")

# 로거 설정 (필요시 level 조절: DEBUG, INFO, WARNING, ERROR)
logger = logging.getLogger(f"{__name__}")
logging.basicConfig(
    level=logging.INFO,
    format='[%(name)s] %(levelname)s: %(message)s'
)

# 함수 내부 print 출력용 로거
func_output_logger = logging.getLogger(f"{__name__}func_output")


def time_check(iterations: int = 1, show_output: bool = False):
    """
    반복 횟수를 지정할 수 있는 타이밍 데코레이터
    
    Args:
        iterations: 반복 횟수 (기본값: 1)
        show_output: 함수 내부 print 출력 표시 여부 (기본값: False)
    """
    def decorator(func: Callable[P, T]) -> Callable[P, list[T]]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> list[T]:
            logger.debug("%s 실행 시작 (반복: %d회)", func.__name__, iterations)
            start = time.perf_counter()
            
            # 함수의 stdout을 캡처해서 로거로 보내기
            results = []
            for i in range(iterations):
                output_buffer = StringIO()
                with redirect_stdout(output_buffer):
                    result = func(*args, **kwargs)
                    results.append(result)
                
                # show_output이 True일 때만, 첫 번째 반복에서만 출력
                if show_output and i == 0:
                    output = output_buffer.getvalue()
                    if output:
                        func_output_logger.info("[%s] %s (반복: %d회 중 첫 번째만 표시)", 
                                                 func.__name__, output.rstrip(), iterations)
            
            end = time.perf_counter()
            avg_time = (end - start) / iterations
            logger.info("%s 평균 실행 시간: %.6f초", func.__name__, avg_time)
            return results
        return wrapper
    return decorator


if __name__ == '__main__':
    @time_check(iterations=30, show_output=True)
    def test(n: int = 100_000):
        print("테스트 함수 내부 출력")
        return [i**2 for i in range(n)]

    test()
