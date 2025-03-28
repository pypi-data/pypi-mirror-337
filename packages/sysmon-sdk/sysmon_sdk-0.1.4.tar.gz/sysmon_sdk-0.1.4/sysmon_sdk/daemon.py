import os
import sys
import time
import psutil
import socket
import threading
import signal
import logging

class SysMonDaemonUDS:
    def __init__(self, socket_path='/tmp/sysmon.sock', interval=5, log_file='/tmp/sysmon.log', pid_file='/tmp/sysmon.pid'):
        self.socket_path = socket_path
        self.interval = interval
        self.running = True
        self.log_file = log_file
        self.pid_file = pid_file

        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='[%(asctime)s] %(levelname)s: %(message)s',
        )

    def daemonize(self):
        if os.fork() > 0:
            sys.exit(0)
        os.setsid()
        if os.fork() > 0:
            sys.exit(0)

        sys.stdout.flush()
        sys.stderr.flush()
        with open('/dev/null', 'rb', 0) as f:
            os.dup2(f.fileno(), sys.stdin.fileno())
        with open('/dev/null', 'ab', 0) as f:
            os.dup2(f.fileno(), sys.stdout.fileno())
            os.dup2(f.fileno(), sys.stderr.fileno())

        os.chdir('/')
        os.umask(0)

    def cpu_memory_monitor(self):
        while self.running:
            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory().percent
            logging.info(f"CPU: {cpu}%  Memory: {mem}%")
            time.sleep(self.interval)

    def handle_client(self, conn):
        logging.info("Client connected")
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                message = data.decode().strip()
                logging.info(f"Received: {message}")
                response = f"Processed: {message}".encode()
                conn.sendall(response)

                if message == "shutdown":
                    logging.info("Shutdown command received. Initiating shutdown...")
                    self.running = False
                    break
        except Exception as e:
            logging.error(f"Client error: {e}")
        finally:
            conn.close()
            logging.info("Client disconnected")

    def write_pid_file(self):
        try:
            with open(self.pid_file, 'w') as f:
                f.write(str(os.getpid()))
        except Exception as e:
            logging.error(f"Failed to write PID file: {e}")

    def remove_pid_file(self):
        try:
            if os.path.exists(self.pid_file):
                os.remove(self.pid_file)
        except Exception as e:
            logging.error(f"Failed to remove PID file: {e}")

    def socket_server(self):
        if os.path.exists(self.socket_path):
            os.remove(self.socket_path)

        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.bind(self.socket_path)
            s.listen()
            logging.info(f"Listening on UDS: {self.socket_path}")
            while self.running:
                try:
                    conn, _ = s.accept()
                    self.handle_client(conn)
                except Exception as e:
                    logging.error(f"Socket error: {e}")

        logging.info("Exiting socket server loop")
        if os.path.exists(self.socket_path):
            os.remove(self.socket_path)
        self.stop()

    def stop(self, signum=None, frame=None):
        logging.info("Shutting down daemon...")
        self.running = False
        self.remove_pid_file()
        sys.exit(0)

    def check_if_already_running(self):
        if os.path.exists(self.pid_file):
            with open(self.pid_file) as f:
                pid = int(f.read())
            try:
                os.kill(pid, 0)
                print(f"Daemon already running with PID {pid}")
                sys.exit(1)
            except ProcessLookupError:
                self.remove_pid_file()

    def run(self):
        self.check_if_already_running()
        self.daemonize()
        self.write_pid_file()
        signal.signal(signal.SIGTERM, self.stop)
        signal.signal(signal.SIGINT, self.stop)

        monitor_thread = threading.Thread(target=self.cpu_memory_monitor)
        monitor_thread.daemon = True
        monitor_thread.start()

        self.socket_server()

if __name__ == "__main__":
    daemon = SysMonDaemonUDS()
    daemon.run()

