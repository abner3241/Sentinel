import time

class CircuitBreaker:
    """Circuit breaker para prevenir chamadas excessivas."""

    def __init__(self, max_failures=5, reset_timeout=60):
        self.max_failures = max_failures
        self.reset_timeout = reset_timeout
        self.failures = 0
        self.last_failure = None

    def call(self, func, *args, **kwargs):
        # TODO: implementar lógica de circuit breaker
        return func(*args, **kwargs)
