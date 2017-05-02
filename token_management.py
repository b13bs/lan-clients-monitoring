import random
import string
import datetime
import subprocess
import re
import os

dir_name = os.path.dirname(os.path.realpath(__file__))
db_filename = os.path.join(dir_name, "tokens.txt")


def get_current_time():
    return datetime.datetime.now()


def generate_random_string():
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(8))


def write_token(token):
    now = get_current_time()
    with open(db_filename, "a") as f:
        f.write("%s|%s\n" % (now.strftime("%Y-%m-%d-%H-%M-%S"), token))


def get_valid_token():
    # Most efficient way of getting last line
    last_line = subprocess.check_output(['tail', '-1', db_filename]).decode()
    if "|" in last_line:
        last_token_created = last_line.split("|")[1].strip()
        if token_check(last_token_created) == "valid":
            return last_token_created

    token = generate_random_string()
    write_token(token)
    return token


def token_is_good_format(token):
    if re.match("^[0-9A-Za-z]{8}$", token):
        return True
    else:
        return False
    

def token_check(token):
    now = get_current_time()
    with open(db_filename, "r") as f:
        for line in f.readlines():
            token_time, token_read = line.strip().split("|")
            if token == token_read:
                datetime_obj = datetime.datetime.strptime(token_time, "%Y-%m-%d-%H-%M-%S")
                diff_seconds = (now - datetime_obj).total_seconds()
                diff_hours = diff_seconds/(60*60)
                if diff_hours > 1:
                    return "expired"
                else:
                    return "valid"
        return "invalid"

