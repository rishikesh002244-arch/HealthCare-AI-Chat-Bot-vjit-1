import subprocess
import time
import webbrowser
import sys
import os

def run_app():
    print("🚀 Starting Premium HealthCare AI ChatBot...")
    
    # Check if we are in the right directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)

    # Clean up logs
    if os.path.exists("backend_error.log"):
        os.remove("backend_error.log")

    # 1. Start FastAPI Backend (Port 8000)
    print("📡 Starting Backend (FastAPI)...")
    # Redirect errors to a log file for debugging
    log_file = open("backend_error.log", "w")
    backend_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "api.index:app", "--host", "127.0.0.1", "--port", "8000"],
        stdout=subprocess.DEVNULL,
        stderr=log_file
    )

    # 2. Start Vite Frontend (Port 3000)
    print("🎨 Starting Frontend (Vite)...")
    frontend_dir = os.path.join(base_dir, "frontend")
    
    if not os.path.exists(os.path.join(frontend_dir, "node_modules")):
        print("📦 Installing frontend dependencies (this may take a minute)...")
        subprocess.run(["npm", "install"], cwd=frontend_dir, shell=True)

    frontend_proc = subprocess.Popen(
        ["npm", "run", "dev", "--", "--port", "3000"],
        cwd=frontend_dir,
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    print("⏳ Waiting for initialization...")
    time.sleep(6) 
    
    # Check if backend is still alive
    if backend_proc.poll() is not None:
        print("❌ Backend failed to start. Check backend_error.log")
        frontend_proc.terminate()
        return

    url = "http://localhost:3000"
    print(f"✅ Application is running at: {url}")
    webbrowser.open(url)
    
    print("\nPress Ctrl+C to stop the application.")
    
    try:
        while True:
            if backend_proc.poll() is not None:
                print("⚠️ Backend stopped unexpectedly. Check backend_error.log")
                break
            if frontend_proc.poll() is not None:
                print("⚠️ Frontend stopped unexpectedly.")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        backend_proc.terminate()
        frontend_proc.terminate()
        log_file.close()
        print("Done.")

if __name__ == "__main__":
    run_app()
