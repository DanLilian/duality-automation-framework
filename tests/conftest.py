"""Root conftest.

Currently empty by design. Fixtures shared across both UI and API test suites
would live here. Today all real fixtures are UI-only and live in
tests/ui/conftest.py - the conftest hierarchy means API tests don't load
browser fixtures they don't need.
"""