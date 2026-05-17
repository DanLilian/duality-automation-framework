"""Scenario 1: Handling non-deterministic UI states."""
from framework.utils.retry import retry_until


def test_notification_banner_eventually_shows_success(home_page, notification_page):
    """Navigate to notification page via UI, retry click+read until banner says success.

    The banner shows success or failure randomly on each click. We retry the
    click+read action with a budget of 4 attempts or 20 seconds (whichever
    fires first). If exhausted, retry_until raises RetryExhausted with rich
    diagnostic context - attempt count, elapsed time, last observed text.
    """
    home_page.click_notification_messages_link()
    notification_page.wait_for_loaded()

    def attempt() -> str:
        notification_page.click_link()
        return notification_page.read_banner_text()

    retry_until(
        action=attempt,
        success=lambda text: "Action successful" in text,
        max_attempts=4,
        max_seconds=20.0,
        action_name="click_link_and_verify_banner",
    )