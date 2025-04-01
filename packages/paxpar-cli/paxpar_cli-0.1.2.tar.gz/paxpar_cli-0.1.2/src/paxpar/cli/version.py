import json
import tempfile
import typer
from rich.console import Console
from paxpar.cli.tools import call
import sys
import yaml
import toml


def pyproject_version_get(target: str):
    """
    get version in a pyproject.toml file
    """
    data = toml.load(open(target))
    return data["project"]["version"]


def pyproject_version_set(target: str, version: str):
    """
    set version in a pyproject.toml file
    """
    try:
        data = toml.load(open(target))
        data["project"]["version"] = version
        toml.dump(data, open(target, "w"))
        print(target + " set to " + version)
    except Exception as e:
        print("Erreur pyproject_version")
        print(e)


def helm_version_set(target: str, version: str):
    """
    set version in a Helm Chart
    """
    # data = yaml.safe_load(open("deploy/paxpar/Chart.yaml"))
    data = yaml.safe_load(open(target))
    data["appVersion"] = version
    data["version"] = version
    yaml.safe_dump(data, open(target, "w"))
    print(f"{target} set to " + version)


console = Console()

app = typer.Typer(help="Misc pp commands")


@app.command()
def show():
    # version = pyproject_version_get("pyproject.toml")
    version = open("VERSION").read().strip()
    print(f"version {version}")


@app.command()
def bump(
    dry_run: bool = False,
): ...


@app.command()
def set(
    version: str,
    dry_run: bool = False,
):
    # assert len(sys.argv) == 2, "version arg is missing !"
    # version = sys.argv[1].strip()
    print("set-version to " + version)

    # set VERSION file
    open("VERSION", "w").write(version)
    print("VERSION set to " + version)

    # set helm chart version
    helm_version_set("packages/pp-api/deploy/paxpar/Chart.yaml", version)

    # set pyproject.toml files
    pyproject_version_set("pyproject.toml", version)
    # pyproject_version('services/core/pyproject.toml', version)

    print("set-version done for " + version)
