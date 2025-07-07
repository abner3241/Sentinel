import time
import logging
from functools import wraps

def retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0, exceptions: tuple = (Exception,)):
# [AUTO-FIXED]     Decorator to retry a function on failure.
# [AUTO-FIXED]     :param max_attempts: maximum number of attempts
# [AUTO-FIXED]     :param delay: initial delay between attempts in seconds
# [AUTO-FIXED]     :param backoff: multiplier for delay each retry
# [AUTO-FIXED]     :param exceptions: exceptions to catch
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts, current_delay = 0, delay
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    logging.warning(f"Retrying {func.__name__}: attempt {attempts}/{max_attempts} failed with error: {e}")
                    if attempts == max_attempts:
                        logging.error(f"All retry attempts failed for {func.__name__}")
                        raise
                    time.sleep(current_delay)
                    current_delay *= backoff
            # Fallback: call function one last time
            return func(*args, **kwargs)
        return wrapper
    return decorator
