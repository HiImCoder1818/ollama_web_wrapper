import subprocess
import time
import socket
import sys

def is_port_open(port=5000):
    with socket.socket() as sock:
        try:
            sock.connect(('127.0.0.1', port))
            return True
        except:
            return False

flask_process = subprocess.Popen([sys.executable, "server.py"])


for _ in range(20):
    if is_port_open(5000):
        break
    time.sleep(0.5)
else:
    print("Flask server failed to start.")
    flask_process.terminate()
    flask_process.wait()
    sys.exit()

fluid_app_path = "app.app"
fluid_process = subprocess.Popen(["open", fluid_app_path])

try:
    while True:
        retcode = fluid_process.poll()
        if retcode is not None:
            print("Fluid app exited with code", retcode)
            # Gracefully terminate Flask server
            flask_process.terminate()
            try:
                flask_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("Flask server did not terminate, killing...")
                flask_process.kill()
                flask_process.wait()
            break
        else:
            print("Fluid app still running...")
        time.sleep(1)
except KeyboardInterrupt:
    print("Interrupted. Cleaning up...")
    fluid_process.terminate()
    flask_process.terminate()
    fluid_process.wait()
    flask_process.wait()
