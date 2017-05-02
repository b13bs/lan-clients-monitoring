#!/usr/bin/env python3

# TODO add database support for token management instead of text file
from flask import Flask
from flask import request
from flask import render_template
from flask import flash
from concurrent.futures import ThreadPoolExecutor
import psutil
import os
import token_management
import scans_utilities
import config

app = Flask(__name__)
app.secret_key = config.flask_secret_key
process = {"name": "scan.py", "path": os.path.dirname(os.path.realpath(__file__))}


def token_validation(token):
    if token is None:
        flash("Access denied, no token supplied", "alert-danger")
        return False
    elif not token_management.token_is_good_format(token):
        flash("Acces denied, bad token format", "alert-danger")
        return False
    else:
        token_status = token_management.token_check(token)
        if token_status == "expired":
            flash("Expired token", "alert-danger")
            return False
        elif token_status == "invalid":
            flash("Bad token", "alert-danger")
            return False
        elif token_status == "valid":
            flash("Access granted", "alert-success")
            return True


@app.route("/status")
def status_page():
    return_value = token_validation(request.args.get('token'))

    if return_value:
        pid = scans_utilities.get_process_pid(process["name"])
        p = psutil.Process(pid)
        if p.status() == "stopped":
            flash("Scan is sleeping. SHHH, don't wake him up!!", "alert-warning")
        else:
            flash("A scan is currently running", "alert-success")

    return render_template("page.html")


@app.route("/snooze")
def snooze_page():
    return_value = token_validation(request.args.get('token'))
    if return_value:
        executor.submit(scans_utilities.pause_scan, process)
        flash("Snoozed", "alert-success")

    return render_template("page.html")


if __name__ == "__main__":
    # http://stackoverflow.com/questions/22615475/flask-application-with-background-threads
    executor = ThreadPoolExecutor(2)
    executor.submit(scans_utilities.start_scan, process)

    pid = scans_utilities.get_process_pid(process["name"])

    app.logger.debug("Scan started. PID=%s" % pid)
    app.config['DEBUG'] = True
    app.run(host="0.0.0.0") 
