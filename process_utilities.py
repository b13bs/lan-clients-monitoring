import os
import subprocess
import time
import signal
import psutil

def killall_processes(path, name, interpreter):
    #['python3', '/var/www/html/lan_clients_monitor/lan_clients_monitor/scan.py']
    for proc in psutil.process_iter():
        if interpreter in proc.name():
            if os.path.join(path, name) in ' '.join(proc.cmdline()):
                proc.kill()


def start_process(path, name, interpreter):
    pipe = subprocess.Popen([interpreter, os.path.join(path, name)])
    return pipe.pid


def resume_process(pid):
    os.kill(pid, signal.SIGCONT)


# https://unix.stackexchange.com/questions/2107/how-to-suspend-and-resume-processes
def pause_process(pid, duration):
    os.kill(pid, signal.SIGSTOP)
    time.sleep(int(duration))
    resume_process(pid)
