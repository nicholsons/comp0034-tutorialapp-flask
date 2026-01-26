"""
Helper to run both the REST API in FastAPI and the front end Flask app
This may not work on Windows
"""
import subprocess
import sys
import os

processes = []

def run_fastapi():
    p = subprocess.Popen([
        sys.executable, "-m", "uvicorn", "src.data.mock_api:app", "--reload", "--port", "8000"
    ])
    processes.append(p)

def run_flask():
    env = os.environ.copy()
    env["FLASK_APP"] = "paralympics"
    env["FLASK_RUN_PORT"] = "5000"
    env["FLASK_ENV"] = "development"
    env["FLASK_DEBUG"] = "1"
    p = subprocess.Popen([sys.executable, "-m", "flask", "run"], env=env)
    processes.append(p)

if __name__ == "__main__":
    try:
        run_fastapi()
        run_flask()
        print("Both apps are running. Press Ctrl+C to stop.")
        while True:
            pass
    except KeyboardInterrupt:
        print("\nStopping apps...")
        for p in processes:
            p.terminate()
        print("All apps stopped.")