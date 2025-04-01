import asyncio
import json
import os
import signal
import subprocess
import sys
from functools import wraps
from pathlib import Path
from typing import Any

import typer
from pydantic import JsonValue


def set_pp_pythonpath(this_file: str | None = None) -> str:
    app_path = str(Path(this_file or __file__).absolute().parent.parent)
    sys.path.append(app_path)
    # typer.echo(f"{app_path} added to PYTHONPATH")
    print(f"{app_path} added to PYTHONPATH")
    return app_path


def call(
    cmd: str,
    cwd: str | None = None,
    pythonpath_set: bool = True,
    extra_envvars: dict[str, Any] | None = None,
    stdout: Any = None,
    dry_run: bool = False,
) -> subprocess.CompletedProcess[bytes]:
    if dry_run:
        print(cmd)
        return b""

    my_env = os.environ.copy()

    if pythonpath_set:
        my_env["PYTHONPATH"] = set_pp_pythonpath()

    if cwd:
        typer.echo(f"[{cwd}] {cmd}")
    else:
        typer.echo(cmd)

    if extra_envvars:
        for k, v in extra_envvars.items():
            typer.echo(f"setting envvar {k}")
            my_env[k] = v

    return subprocess.run(
        cmd,
        shell=True,
        env=my_env,
        cwd=cwd,
        stdout=stdout,
    )


def call_json(
    cmd: str,
) -> dict[str, JsonValue]:
    query = call(
        cmd,
        stdout=subprocess.PIPE,
    )
    raw = query.stdout
    # print(f"{raw=}, xxx")
    return json.loads(raw.decode())


def host_only(host: str) -> str:
    """
    '[2a01:4f9:2a:25d5::17]' -> '2a01:4f9:2a:25d5::17'
    'localhost' -> 'localhost'
    """
    host = host.strip()
    if host.startswith("["):
        host = host[1:]
    if host.endswith("]"):
        host = host[:-1]

    return host


# see https://github.com/fastapi/typer/issues/950#issuecomment-2351076467
def cli_coro(
    signals=(signal.SIGHUP, signal.SIGTERM, signal.SIGINT),
    shutdown_func=None,
):
    """Decorator function that allows defining coroutines with click."""

    def decorator_cli_coro(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            loop = asyncio.get_event_loop()
            if shutdown_func:
                for ss in signals:
                    loop.add_signal_handler(ss, shutdown_func, ss, loop)
            return loop.run_until_complete(f(*args, **kwargs))

        return wrapper

    return decorator_cli_coro
