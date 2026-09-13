import os
import signal
import subprocess
import sys
import time

from backend.config import settings


def launch() -> None:
    root = os.path.dirname(os.path.abspath(__file__))
    port = os.getenv("PORT", str(settings.STREAMLIT_PORT if settings.STREAMLIT_PORT != 8501 else 8080))
    api_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.app:app", "--host", settings.FASTAPI_HOST, "--port", str(settings.FASTAPI_PORT)],
        cwd=root,
    )
    processes = [api_proc]

    def _cleanup(signum=None, frame=None):
        print("\nStopping PRAHARI services...")
        for process in reversed(processes):
            if process.poll() is None:
                process.terminate()
        for process in reversed(processes):
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
        sys.exit(0)

    signal.signal(signal.SIGTERM, _cleanup)
    signal.signal(signal.SIGINT, _cleanup)

    try:
        time.sleep(2)
        streamlit_proc = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                "frontend/app.py",
                "--server.port",
                str(port),
                "--server.address",
                "0.0.0.0",
                "--server.headless",
                "true",
                "--browser.gatherUsageStats",
                "false",
            ],
            cwd=root,
        )
        processes.append(streamlit_proc)
        print(f"Backend API (Internal): http://{settings.FASTAPI_HOST}:{settings.FASTAPI_PORT}")
        print(f"Frontend Portal (Public): http://0.0.0.0:{port}")
        while all(process.poll() is None for process in processes):
            time.sleep(1)
    except KeyboardInterrupt:
        _cleanup()
    finally:
        _cleanup()


if __name__ == "__main__":
    launch()
