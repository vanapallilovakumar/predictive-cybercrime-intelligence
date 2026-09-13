import os
import signal
import subprocess
import sys
import time

from backend.config import settings


def launch() -> None:
    root = os.path.dirname(os.path.abspath(__file__))
    api_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.app:app", "--host", settings.FASTAPI_HOST, "--port", str(settings.FASTAPI_PORT)],
        cwd=root,
    )
    processes = [api_proc]
    try:
        time.sleep(2)
        streamlit_proc = subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", "frontend/app.py", "--server.port", str(settings.STREAMLIT_PORT), "--server.headless", "true"],
            cwd=root,
        )
        processes.append(streamlit_proc)
        print(f"Backend API: http://{settings.FASTAPI_HOST}:{settings.FASTAPI_PORT}")
        print(f"Swagger Docs: http://{settings.FASTAPI_HOST}:{settings.FASTAPI_PORT}/docs")
        print(f"Frontend: http://localhost:{settings.STREAMLIT_PORT}")
        while all(process.poll() is None for process in processes):
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping PRAHARI services...")
    finally:
        for process in reversed(processes):
            if process.poll() is None:
                process.terminate()
        for process in reversed(processes):
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()


if __name__ == "__main__":
    launch()
