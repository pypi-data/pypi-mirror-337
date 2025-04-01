import json
import tempfile
import typer
from rich.console import Console
from paxpar.cli.tools import call


console = Console()

app = typer.Typer(help="Misc pp commands")


@app.command()
def api(
    REGISTRY_ROOT: str = "rg.fr-par.scw.cloud",
    REGISTRY_PREFIX: str = "pp-registry-test1",
    REGISTRY_USER: str = "nologin",
    REGISTRY_PASSWORD: str = "xxx",
    dry_run: bool = False,
):
    """
    # see https://pythonspeed.com/articles/gitlab-build-docker-image/
    podman run \
        --rm \
        --security-opt label=disable \
        --user podman \
        quay.io/podman/stable \
        podman \
            run \
            --rm \
            docker.io/library/alpine \
                ls /     

    # see https://stackoverflow.com/questions/64509618/podman-in-podman-similar-to-docker-in-docker
    - podman login -u "$CI_REGISTRY_USER" -p "$CI_REGISTRY_PASSWORD" "$CI_REGISTRY"
    - podman build -t "$CI_REGISTRY_IMAGE:podman" .
    - podman push "$CI_REGISTRY_IMAGE:podman"
    """

    VERSION = "0.0.1"

    call(
        f'podman login -u "{REGISTRY_USER}" -p "{REGISTRY_PASSWORD}" "{REGISTRY_ROOT}/{REGISTRY_PREFIX}"',
        dry_run=dry_run,
    )
    call(
        f'podman build -t "{REGISTRY_ROOT}/{REGISTRY_PREFIX}/pp-core:{VERSION}" .',
        cwd="packages/pp-api",
        dry_run=dry_run,
    )
    call(
        f'podman push "{REGISTRY_ROOT}/{REGISTRY_PREFIX}/pp-core:{VERSION}"',
        dry_run=dry_run,
    )

@app.command()
def front(
    dry_run: bool = False,
):
    """
    build front (bun generate)
    """
    call(
        "bun install --frozen-lockfile",
        cwd="packages/pp-front",
        dry_run=dry_run,
    )
    call(
        "bun run generate",
        cwd="packages/pp-front",
        dry_run=dry_run,
    )


@app.command()
def widgets(
    dry_run: bool = False,
):
    """
    build pp-widgets (bun generate)
    """
    call(
        "bun install --frozen-lockfile",
        cwd="packages/pp-widgets",
        dry_run=dry_run,
    )
    call(
        "bun run generate",
        cwd="packages/pp-widgets",
        dry_run=dry_run,
    )


@app.command()
def all():
    """
    build all ... (NOT IMPLEMENTED)
    """
    ...