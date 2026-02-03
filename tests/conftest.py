import threading
import time
from urllib.request import urlopen

import pytest
import uvicorn

from paralympics import create_app


def wait_for_http(url, timeout=5):
    start = time.time()
    while True:
        try:
            urlopen(url, timeout=1)
            return
        except Exception:
            if time.time() - start > timeout:
                raise RuntimeError(f"Server did not start in time: {url}")
            time.sleep(0.1)


@pytest.fixture(scope="session", autouse=True)
def api_server():
    """Start the REST API server before Dash app tests."""
    from data.api import app

    thread = threading.Thread(
        target=uvicorn.run,
        kwargs={
            "app": app,
            "host": "127.0.0.1",
            "port": 8000,
            "reload": False
        },
        daemon=True,
    )
    thread.start()

    wait_for_http("http://127.0.0.1:8000")

    yield


@pytest.fixture(scope="session")
def app_server():
    """Start a Flask app server for Playwright tests

     Uses the threading library.
     """
    from paralympics.config import TestingConfig
    from paralympics import create_app

    app = create_app(TestingConfig)

    thread = threading.Thread(
        target=app.run,
        kwargs={'host': '127.0.0.1', 'debug': False, 'use_reloader': False, 'port': 5000},
        daemon=True
    )
    thread.start()

    wait_for_http("http://127.0.0.1:5000")

    yield f"http://127.0.0.1:5000"


@pytest.fixture(scope='session')
def app():
    """Create a Flask app configured for testing"""
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "WTF_CSRF_ENABLED": False
        }
    )
    yield app


@pytest.fixture()
def client(app):
    """ Create a flask test client """
    yield app.test_client()
