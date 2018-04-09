#!/usr/bin/env python3

# TODO add database support for token management instead of text file
from flask import Flask
from flask import request
from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for
from concurrent.futures import ThreadPoolExecutor
import psutil
import os
import re
import token_management
import process_utilities

app = Flask(__name__)


def token_validation(token):
    if token is None:
        flash("Access denied, no token supplied", "alert-danger")
        return False
    elif not token_management.token_is_good_format(token):
        flash("Access denied, bad token format", "alert-danger")
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
            return True


def transform_time(duration):
    r = re.search("^([0-9]+)([s|m|h])$", duration)
    if not r:
        return 3600

    number, unit = r.groups()
    if unit == "s":
        return int(number)
    elif unit == "m":
        return int(number)*60
    elif unit == "h":
        return int(number)*60*60


@app.route("/")
def status_page():
    token = request.args.get('token')
    return_value = token_validation(token)

    if return_value:
        process_pid = app.config["process_pid"]
        p = psutil.Process(process_pid)
        if p.status() == "stopped":
            flash("Scan is sleeping. SHHH, don't wake him up!!", "alert-warning")
        else:
            flash("Scan is currently running", "alert-info")
        return render_template("page.html", token=token)

    return render_template("page.html")


@app.route("/snooze")
def snooze():
    # token parameter
    token = request.args.get('token')
    token_is_valid = token_validation(token)

    # duration parameter
    duration = request.args.get('duration')
    if duration is None:
        duration = "3600"

    nb_seconds = transform_time(duration)

    app.logger.debug("Snoozing for %s seconds!" % nb_seconds)
    if token_is_valid:
        try:
            future
        except NameError:
            pass
        else:
            if future.running():
                value = future.cancel()

        global future
        process_pid = app.config["process_pid"]
        executor = app.config["executor"]
        future = executor.submit(process_utilities.pause_process, process_pid, nb_seconds)
        flash("Snoozed for %s seconds" % nb_seconds, "alert-info")

    return redirect(url_for("status_page", token=token))


@app.route("/unsnooze")
def unsnooze():
    # token parameter
    token = request.args.get('token')
    token_is_valid = token_validation(token)

    if token_is_valid:
        app.logger.debug("Unsnoozing!")
        process_pid = app.config["process_pid"]
        process_utilities.resume_process(process_pid)

    return redirect(url_for("status_page", token=token))


def init_config():
    app.config.from_pyfile("config.py")
    app.config.update(
        DEBUG=True,
        SECRET_KEY="fdkshfjdsfhj",
        PROCESS_PATH=os.path.dirname(os.path.realpath(__file__)),
        LOGGER_NAME="lan_clients_monitor"
    )


if __name__ == "__main__":
    init_config()

    # http://stackoverflow.com/questions/22615475/flask-application-with-background-threads
    executor = ThreadPoolExecutor(5)
    app.config["executor"] = executor

    path = app.config["PROCESS_PATH"]
    name = app.config["PROCESS_NAME"]
    interpreter = app.config["PROCESS_INTERPRETER"]

    process_utilities.killall_processes(path, name, interpreter)

    process_pid = process_utilities.start_process(path=path, name=name, interpreter=interpreter)
    app.config["process_pid"] = process_pid

    token_management.check_token_file_existence()

    app.logger.debug("Scan started. PID=%s" % process_pid)
    app.config['DEBUG'] = False
    app.run(host="0.0.0.0", use_reloader=False)
