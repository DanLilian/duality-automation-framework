# Duality automation framework

A Python + Playwright UI automation framework built for the Duality Student Automation Developer take-home assignment.

## Technologies
- Python 3.13
- Playwright (sync API, Chromium only)
- pytest + pytest-playwright + pytest-html
- uv (package and Python version management)
- ruff (lint + format)

## Repository hierarchy
```
duality-automation-framework/
├── src/framework/
│   ├── config/         # BASE_URL and other settings, read from env vars
│   ├── pages/          # Page Object Model classes (BasePage + concrete pages)
│   └── utils/          # Reusable helpers: retry, persistence
├── tests/
│   ├── conftest.py     # Root conftest (currently empty by design)
│   ├── ui/             # UI tests with shared UI fixtures in conftest.py
│   └── api/            # Reserved for future REST API tests
├── output/
│   ├── reports/        # pytest-html report + failure screenshots
│   └── data/           # Scenario 2 persisted JSON results
├── pyproject.toml      # uv + pytest + ruff config in one file
└── .github/workflows/  # CI pipeline (see CI section below)
```
## Setup
Prerequisites: any OS, no Python required (uv will install it).

1. **Install uv** (one-time, if not already installed):
    - macOS/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
    - Windows: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

2. **Clone and install dependencies:**
    - git clone <repo-url>
    - cd duality-automation-framework
    - uv sync
    - uv run playwright install chromium
`uv sync` reads `.python-version` and `pyproject.toml`, downloads Python 3.13 if missing, creates `.venv/`, and installs every dependency from `uv.lock` for reproducibility.

## Test run Guideline

### Run everything, headless (default)
uv run pytest

### Run with a visible browser (useful for the live interview demo)
uv run pytest --headed

### Run a single scenario
uv run pytest tests/ui/test_notification_scenario.py --headed
uv run pytest tests/ui/test_challenging_dom_scenario.py --headed

The HTML report writes to `output/reports/report.html` after every run. Failure screenshots go to same directory.

## Output Location

- **Test report**: `output/reports/report.html` (self-contained, open in any browser)
- **Failure screenshots**: `output/reports/<test_name>_failure.png` (only on failure)
- **Scenario 2 persisted data**: `output/data/scenario2_result.json`

Test Scenario 2 JSON includes the running sum, per-click history with status, any failed buttons, and a `complete` flag indicating whether all clicks succeeded.

## Architectural Decisions:

### Page Object Model

Every page on the site that is tested has a corresponding Python class inheriting from `BasePage`. `BasePage` exposes three shared methods — `navigate()`, `wait_for_loaded()`, and `take_screenshot()` — and the pages override `wait_for_loaded` to declare what "ready for use" means for them.

Locators live inside page objects. Tests never reference DOM selectors directly. If the application's CSS changes, only the page object updates; tests are untouched.

### Locator strategy

`get_by_role` first, falling back to text or stable IDs when role-based selectors don't apply. I picked role-based selectors because they query the accessibility tree and stay stable across CSS rewrites. The Scenario 2 Answer reader is the one place I had to fall back further: the value is drawn onto a `<canvas>` via Javascript, so there's no DOM text. I read it from the inline `<script>` tag's source.

### Retry placement: in the test, not the page object

Both scenarios needed retries. I did not put retry logic inside the page object methods. A different test might want to check that the banner is unreliable rather than retry past it. Putting retry inside the page object would couple every caller to one policy. The `retry_until` helper is generic.

### Scenario 2: halt vs. continue on retry exhaustion

When a button fails its 4-retry budget, the test logs the failure and continues to the next button rather than halting on the first failure.

My Reasoning for this is that I prefer one test run that tells me about all three buttons over three runs that each tell me about one. The cost is partial data — but I handled that by recording per-button success/failure in the persisted JSON with a `complete` flag, and the test still fails loudly at the end if any button hit retry exhaustion, The result is still correct (failure).

### Data store: JSON, and the 10K-parallel-tests answer

I chose a flat JSON file at `output/data/scenario2_result.json`. Reasons:
- Zero infrastructure cost.
- The reviewer running the framework can open the file in any text editor.
- Output structure is human-readable.

Although I understand that at 10,000 parallel tests, JSON breaks.**

At that scale, I'd probably switch to Postgres or SQLite

The framework's persistence layer is one function (`save_scenario2_result` in `utils/persistence.py`). Swapping JSON for any of the above is a one-function rewrite, not a framework rewrite. That separation is by design.

### Fixture hierarchy

Fixtures live in `tests/ui/conftest.py`, not `tests/conftest.py`. UI fixtures (page objects, browser context, screenshot-on-failure) shouldn't load when running API tests. Today this distinction is invisible because all tests are UI; when API tests are added under `tests/api/`, they won't pull in browser infrastructure they don't need. Pytest's conftest hierarchy composes automatically.

The `home_page` fixture both constructs the page object and calls `.navigate()` before yielding, so tests get a loaded page without boilerplate. The other page-object fixtures only construct — navigation happens *inside* the test via `home_page.click_<x>_link()`, because the assignment requires UI navigation rather than deep-linking.

### Test independence

Tests run in alphabetical filename order — Challenging DOM before Notification. That's not the assignment's narrative order. My tests are independent and should stay that way. If the report needed grouping by scenario number for presentation, pytest markers would handle that without affecting execution order.

## Mocks / Workarounds

- **Canvas Answer reading**: The Answer on `/challenging_dom` is rendered onto a `<canvas>` element via JavaScript and has no DOM text representation. Rather than OCR'ing the canvas pixels, I read the inline `<script>` tag's source code and extract the number from its `strokeText('Answer: NNNNN', ...)` call. This is documented in `ChallengingDomPage.read_answer` and works because the page's script is regenerated server-side per page request, so the value in the script source matches the rendered value.

- **No other mocks.** All retries, click logic, and assertions run against the real `the-internet.herokuapp.com` site.

## CI/CD

A GitHub Actions workflow lives at `.github/workflows/ci.yml`. It runs on push and pull request: installs uv, syncs deps, installs Chromium, runs the test suite headless, and uploads `output/reports/` and `output/data/` as build artifacts. The job is scaffolded with the same `uv sync` flow used locally, so what runs in CI is what runs on the developer machine.

## Known limitations and would be Next steps

If I had more time:
- **Allure reporting**: Better failure analytics, history trends, severity tagging. Cut for the take-home because Allure adds a Java dependency and a separate CLI; pytest-html is a single self-contained file that works on a clean reviewer machine with zero extra setup.
- **Playwright trace files on failure**: One config line away. Traces give you a step-by-step time-travel debugger for failed tests. Higher value than HTML reports for UI debugging.
- **API test layer**: The folder exists at `tests/api/` and the conftest hierarchy is ready. Adding REST tests would mean writing fixtures for an HTTP client (`httpx`) in `tests/api/conftest.py` and writing the tests. Zero framework changes needed.
- **Cross-browser**: Currently Chromium only. `pytest-playwright` supports Firefox and WebKit via a CLI flag; install times triple, so cut for now.
- **Parallel execution**: `pytest-xdist` plugin would parallelize tests across workers. At two tests it's overkill; at hundreds, essential.
- **Visual regression**: Playwright's `expect(page).to_have_screenshot()` for pixel-diff testing against baselines. Useful once the suite covers visual layouts.

## Why specific choices

This section consolidates the architectural calls and the trade-offs I considered:

- **uv over poetry/pip**: much faster install, single tool replaces venv/pip/pyenv. Cost: newer, smaller community. Mitigation: `pyproject.toml` is portable, switching to poetry is a few hours of work if uv hits limits I can't work around.
- **Sync Playwright over async**: Lower cognitive overhead. Async only matters when you need to drive many browsers concurrently in one process, which isn't this assignment.
- **Class-attribute `PATH` per page**: The URL path is a property of the class, not of an instance. Class-level signals "this is fixed across all instances," and allows `NotificationPage.PATH` reference without instantiation.
- **`os.getenv` with default for `BASE_URL`**: Sensible local default, env var override for staging/production. 12-Factor principle: separate config from code.
- **Self-contained HTML report**: Single file, opens anywhere with no asset dependencies. Important for the live interview review.