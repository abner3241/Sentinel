import pytest
from utils.retry import retry

def test_retry_success():
    @retry(max_attempts=2)
    def f():
        return 1
    assert f() == 1
