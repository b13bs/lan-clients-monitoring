import os
import subprocess
import time
import signal
import config


def start_process():
    pipe = subprocess.Popen(["%s/%s" % (config.process_path, config.process_name)])
    return pipe.pid


def resume_process(pid):
    os.kill(pid, signal.SIGCONT)


# https://unix.stackexchange.com/questions/2107/how-to-suspend-and-resume-processes
def pause_process(pid, duration):
    os.kill(pid, signal.SIGTSTP)
    time.sleep(int(duration))
    resume_process(pid)

