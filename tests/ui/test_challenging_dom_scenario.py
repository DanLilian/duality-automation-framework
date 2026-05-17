"""Scenario 2: Dynamic elements & data extraction."""
import pytest
from framework.utils.retry import retry_until, RetryExhausted
from framework.utils.persistence import save_scenario2_result


def test_challenging_dom_sum_and_persist(home_page, challenging_dom_page):
    """Navigate via UI; click each button twice (counted by Answer changes); sum and persist."""
    home_page.click_challenging_dom_link()
    challenging_dom_page.wait_for_loaded()

    history: list[dict] = []
    failed_buttons: list[str] = []
    total = 0
    crashed_with: Exception | None = None

    try:
        for variant in challenging_dom_page.BUTTON_VARIANTS:
            for click_index in (1, 2):
                try:
                    previous = challenging_dom_page.read_answer()

                    def attempt() -> int:
                        challenging_dom_page.click_button(variant)
                        return challenging_dom_page.read_answer()

                    new_value = retry_until(
                        action=attempt,
                        success=lambda v: v != previous,
                        max_attempts=4,
                        max_seconds=20.0,
                        action_name=f"click_{variant}_#{click_index}",
                    )
                    total += new_value
                    history.append({
                        "button": variant,
                        "click_index": click_index,
                        "answer": new_value,
                        "status": "success",
                    })
                except RetryExhausted as e:
                    failed_buttons.append(f"{variant}#{click_index}")
                    history.append({
                        "button": variant,
                        "click_index": click_index,
                        "answer": None,
                        "status": "failed",
                        "error": str(e),
                    })
    except Exception as e:
        # Catch unexpected crashes so persistence still runs.
        crashed_with = e
    finally:
        save_scenario2_result({
            "sum": total,
            "history": history,
            "failed_buttons": failed_buttons,
            "complete": len(failed_buttons) == 0 and crashed_with is None,
            "crashed_with": str(crashed_with) if crashed_with else None,
        })

    if crashed_with:
        raise crashed_with
    if failed_buttons:
        pytest.fail(f"Buttons failed after retry exhaustion: {failed_buttons}. Partial sum: {total}.")