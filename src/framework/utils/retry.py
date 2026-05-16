"""Generic retry helper with attempt and time budgets."""
import time
from typing import Callable, TypeVar

T = TypeVar("T")


class RetryExhausted(Exception):
    """Raised when retry budget is exhausted without meeting the success predicate."""

    def __init__(
        self,
        action_name: str,
        attempts: int,
        max_attempts: int,
        elapsed: float,
        max_seconds: float,
        last_value: object,
    ) -> None:
        self.action_name = action_name
        self.attempts = attempts
        self.max_attempts = max_attempts
        self.elapsed = elapsed
        self.max_seconds = max_seconds
        self.last_value = last_value
        super().__init__(
            f"'{action_name}' failed after {attempts}/{max_attempts} attempts "
            f"in {elapsed:.2f}s of {max_seconds}s budget. "
            f"Last observed value: {last_value!r}"
        )


def retry_until(
    action: Callable[[], T],
    success: Callable[[T], bool],
    max_attempts: int,
    max_seconds: float,
    action_name: str = "action",
) -> T:
    """Call `action` repeatedly until `success(result)` is True.

    Stops when either max_attempts or max_seconds is reached. Raises RetryExhausted
    if neither attempt hits success. Both limits are evaluated after each attempt;
    whichever expires first ends the loop.
    """
    start = time.monotonic()
    attempts = 0
    last_value: object = None

    while attempts < max_attempts and (time.monotonic() - start) < max_seconds:
        attempts += 1
        result = action()
        last_value = result
        if success(result):
            return result

    raise RetryExhausted(
        action_name=action_name,
        attempts=attempts,
        max_attempts=max_attempts,
        elapsed=time.monotonic() - start,
        max_seconds=max_seconds,
        last_value=last_value,
    )