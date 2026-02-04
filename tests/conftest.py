import shutil
import threading
import time
from pathlib import Path
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
    """Start the REST API server before Dash app tests.

     Makes a copy of the database before the server starts, and to replace
     the original at the end of the tests.
     NB this is not a recommended approach, this will be covered when the REST API is tested
    """

    # Create a copy of the database
    root = Path(__file__).parent.parent
    _orig_db = root.joinpath("src", "data", "paralympics.db")
    _backup_db = _orig_db.with_suffix(_orig_db.suffix + ".orig")

    if not _orig_db.exists():
        raise RuntimeError(f"Original DB not found: {_orig_db}")

    # backup original
    shutil.copy2(_orig_db, _backup_db)

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

    # Teardown: restore original DB
    if _backup_db.exists():
        shutil.copy2(_backup_db, _orig_db)
        try:
            _backup_db.unlink()
        except Exception:
            pass


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
