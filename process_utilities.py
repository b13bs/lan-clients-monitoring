import os
import subprocess
import time
import signal


def start_process(path, name, interpreter):
    pipe = subprocess.Popen([interpreter, os.path.join(path, name)])
    return pipe.pid


def resume_process(pid):
    os.kill(pid, signal.SIGCONT)


# https://unix.stackexchange.com/questions/2107/how-to-suspend-and-resume-processes
def pause_process(pid, duration):
    os.kill(pid, signal.SIGTSTP)
    time.sleep(int(duration))
    resume_process(pid)
