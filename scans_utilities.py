import os
import psutil
import subprocess
import time
import signal


def get_process_pid(process_name):
    for proc in psutil.process_iter():
        if process_name in proc.name():
            if proc.status() != psutil.STATUS_ZOMBIE:
                return proc.pid
    return None


def killall_scans(process):
    pid = get_process_pid(process["name"])
    if pid:
        proc = psutil.Process(pid)
        proc.kill()


def start_scan(process):
    killall_scans(process)
    subprocess.Popen(["%s/%s" % (process["path"], process["name"])])


# https://unix.stackexchange.com/questions/2107/how-to-suspend-and-resume-processes
def pause_scan(process):
    pid = get_process_pid(process["name"])
    os.kill(pid, signal.SIGTSTP)
    time.sleep(60)
    os.kill(pid, signal.SIGCONT)
