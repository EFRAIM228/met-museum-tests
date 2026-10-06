import logging
import os
import pytest
import requests

BASE_URL = "https://collectionapi.metmuseum.org/public/collection/v1"

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/test_run.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

@pytest.fixture(scope="session")
def base_url():
    return BASE_URL

@pytest.fixture
def session():
    s = requests.Session()
    return s

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call":
        logging.info(f"Test: {item.name} | Outcome: {rep.outcome}")
