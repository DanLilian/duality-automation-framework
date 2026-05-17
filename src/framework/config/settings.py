"""Framework configuration.

Values are read from environment variables with sensible defaults, following
12-Factor App principles - the same code runs against local, staging, or
production by changing one env var.
"""
import os

BASE_URL: str = os.getenv("BASE_URL", "https://the-internet.herokuapp.com")