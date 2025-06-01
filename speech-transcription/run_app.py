import subprocess
import sys
import webbrowser
import time
import socket
import requests
from pathlib import Path

def check_port_available(port: int) -> bool:
    """Check if a port is available"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            return True
        except socket.error:
            return False

def find_available_port(start_port: int = 8000, max_attempts: int = 10) -> int:
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        if check_port_available(port):
            return port
    raise Exception(f"No available ports found in range {start_port}-{start_port + max_attempts}")

def install_dependencies():
    """Install required packages"""
    packages = [
        'fastapi',
        'uvicorn[standard]',
        'python-multipart',  # Required for file uploads
        'torch',
        'torchaudio',
        'transformers',
        'librosa',
        'numpy',
        'requests'
    ]
   
    print("📦 Installing dependencies...")
    for package in packages:
        print(f"Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")
            return False
   
    print("✅ All dependencies installed!")
    return True

def check_dependencies():
    """Check if packages are installed"""
    required_packages = [
        'fastapi', 'uvicorn', 'torch', 'torchaudio', 
        'transformers', 'librosa', 'numpy', 'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing dependencies: {', '.join(missing_packages)}")
        return False
    else:
        print("✅ All dependencies found!")
        return True

def wait_for_server(url: str, timeout: int = 30) -> bool:
    """Wait for the server to be ready"""
    print("⏳ Waiting for server to start...")
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"{url}/health", timeout=5)
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)
    
    return False

def run_app():
    """Run the FastAPI app"""
    print("🚀 Starting Audio Transcription API...")
    
    # Check if main.py exists
    if not Path("main.py").exists():
        print("❌ main.py not found in current directory!")
        print("Please make sure main.py is in the same folder as this launcher.")
        return
    
    try:
        # Find available port
        port = find_available_port(8000)
        print(f"🔌 Using port: {port}")
        
        # Start FastAPI with uvicorn
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "main:app",
            "--host", "0.0.0.0",
            "--port", str(port),
            "--reload"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
        )
        
        # Wait for server to be ready
        server_url = f"http://localhost:{port}"
        
        if wait_for_server(server_url):
            print(f"✅ Server is ready!")
            
            # Open browser
            try:
                webbrowser.open(server_url)
                print(f"🌐 Browser opened at: {server_url}")
            except Exception as e:
                print(f"⚠️ Could not open browser automatically: {e}")
                print(f"Please open manually: {server_url}")
            
            print(f"📖 API Documentation: {server_url}/docs")
            print(f"🔍 Interactive API: {server_url}/redoc")
            print("⏹️ Press Ctrl+C to stop the server")
            
            # Wait for user to stop
            try:
                while process.poll() is None:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Stopping server...")
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    print("⚠️ Force killing server...")
                    process.kill()
                print("👋 Server stopped!")
        else:
            print("❌ Server failed to start within timeout period")
            stdout, stderr = process.communicate()
            if stderr:
                print(f"Error details: {stderr}")
            process.terminate()
            
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def show_usage_info():
    """Show information about how to use the API"""
    print("\n📋 USAGE INFORMATION")
    print("=" * 50)
    print("🌐 Web Interface: http://localhost:PORT")
    print("📖 API Docs: http://localhost:PORT/docs")
    print("🔍 ReDoc: http://localhost:PORT/redoc")
    print("\n🎯 Main Endpoints:")
    print("  GET  /health      - Check server status")
    print("  POST /transcribe  - Upload audio file for transcription")
    print("  GET  /models/info - Get model information")
    print("\n📁 Supported Audio Formats:")
    print("  WAV, MP3, FLAC, M4A, OGG")

def main():
    print("🎙️ AUDIO TRANSCRIPTION API LAUNCHER")
    print("=" * 50)
   
    # Check dependencies
    if not check_dependencies():
        choice = input("📦 Install missing packages? (y/n): ").strip().lower()
        if choice == 'y':
            if not install_dependencies():
                print("❌ Installation failed! Cannot proceed.")
                return
        else:
            print("❌ Cannot run without dependencies!")
            return
    
    # Show usage info
    show_usage_info()
    
    # Ask user if they want to continue
    choice = input("\n🚀 Start the API server? (y/n): ").strip().lower()
    if choice != 'y':
        print("👋 Goodbye!")
        return
   
    # Run app
    run_app()

if __name__ == "__main__":
    main()