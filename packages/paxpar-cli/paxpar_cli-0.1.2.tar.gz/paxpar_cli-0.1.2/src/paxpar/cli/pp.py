# /// script
# dependencies = [
#   "pydantic",
#   "python-dotenv",
#   "pyyaml",
#   "typer",
# ]
# ///
#!/usr/bin/env python3
#
#!.venv/bin/python
#!services/core/.venv/bin/python
#
# bootstrap env with :
#
#    pyenv install --skip-existing
#    poetry install -vv


import os
import signal

import typer
from dotenv import load_dotenv
from paxpar.cli.tools import set_pp_pythonpath

set_pp_pythonpath()

# take environment variables from .env
# this is not the app conf but the devops env conf
if load_dotenv():
    typer.echo(".env found and loaded !")

from pathlib import Path

from paxpar.cli.build import app as app_build
from paxpar.cli.conf import app as app_conf
from paxpar.cli.deploy import app as app_deploy
from paxpar.cli.dev import app as app_dev
from paxpar.cli.image import app as app_image
from paxpar.cli.misc import app as app_misc
from paxpar.cli.py import app as app_py
from paxpar.cli.ref import app as app_ref
from paxpar.cli.run import app as app_run
from paxpar.cli.s3 import app as app_s3
from paxpar.cli.scrap import app as app_scrap
from paxpar.cli.setup import app as app_setup
from paxpar.cli.status import app as app_status
from paxpar.cli.test import app as app_test
from paxpar.cli.version import app as app_version


app = typer.Typer(name="pp cli", help="paxpar command line interface")

# subcommands as a group
#app.add_typer(app_conf, name="conf")
app.add_typer(app_build, name="build")
app.add_typer(app_deploy, name="deploy")
app.add_typer(app_dev, name="dev")
app.add_typer(app_image, name="image")
app.add_typer(app_misc, name="misc")
app.add_typer(app_py, name="py")
app.add_typer(app_ref, name="ref")
app.add_typer(app_run, name="run")
app.add_typer(app_s3, name="s3")
app.add_typer(app_scrap, name="scrap")
app.add_typer(app_setup, name="setup")
app.add_typer(app_status, name="status")
app.add_typer(app_test, name="test")
app.add_typer(app_version, name="version")


# see https://stackoverflow.com/questions/320232/ensuring-subprocesses-are-dead-on-exiting-python-program
USE_KILL = False

# ____________________________________________________________________


if __name__ == "__main__":
    if USE_KILL:
        # see https://stackoverflow.com/questions/320232/ensuring-subprocesses-are-dead-on-exiting-python-program
        os.setpgrp()  # create new process group, become its leader
        try:
            app()
        finally:
            os.killpg(0, signal.SIGKILL)  # kill all processes in my group
    else:
        app()
# ____________________________________________________________________
