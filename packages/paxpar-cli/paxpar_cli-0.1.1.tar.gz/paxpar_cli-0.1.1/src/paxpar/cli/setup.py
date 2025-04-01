from pathlib import Path

import typer
from rich.console import Console

from paxpar.cli.tools import call

console = Console()

app = typer.Typer(help="Setup/clean pp env")


@app.command()
def all():
    """
    Setup paxpar envs

    apt install libqpdf-dev
    """
    # TODO: how to get paxpar base folder ?, __file__ is differend when call from a link/alias
    PYTHON_VERSION = (Path(__file__).parent / ".python-version").open().read().strip()
    # print(f"PYTHON_VERSION={PYTHON_VERSION}")

    # curl https://pyenv.run | bash
    call(f"""pyenv install --skip-existing {PYTHON_VERSION}""")
    call("""pyenv install --skip-existing""", pythonpath_set=False)
    # call(
    #    """pyenv install --skip-existing""", cwd=f"paxpar/services/core", pythonpath_set=False
    # )
    # call("""poetry install -vv""", cwd=f"paxpar/services/core", pythonpath_set=False)
    # call('''pyenv update''')
    call("""poetry self update""")
    call("""yarn install""")

    call(f"""pyenv local {PYTHON_VERSION}""")
    call("""poetry install -vv""")

    call("""pre-commit install""")
    call("""pre-commit autoupdate""")


@app.command()
def clean():
    """
    Clean paxpar env
    """
    # for svc in (
    #    "paxpar/services/core",
    #    "paxpar/services/forge",
    # ):
    #    call("""rm -Rf .venv""", cwd=svc)
    call("""find . -type d -name "__pycache__" | xargs rm -rf {}""")
    call("""rm -Rf node_modules .coverage .mypy_cache""")
    # for svc in ("front",):
    #    call("""rm -Rf node_modules""", cwd=f"services/{svc}")
    call("""rm -Rf .venv""")
    call("""rm -Rf ~/.pyenv""")


@app.command()
def registry_reset():
    """
    Reset the microk8s registry
    """

    """
    TODO: other hints :

        microk8s disable storage:destroy-storage
        microk8s enalbe storage

        microk8s.ctr images list -q | grep paxpa
        microk8s.ctr images remove ###ref
        docker image rm ###
        ctr images remove
    """
    call(
        """
        docker system prune -a -f --volumes
        microk8s.disable registry
        sleep 3
        microk8s.enable registry
    """
    )
