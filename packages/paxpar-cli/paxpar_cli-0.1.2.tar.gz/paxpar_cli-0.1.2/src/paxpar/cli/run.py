from typing import Optional

import typer
from rich.console import Console
from paxpar.cli.tools import call

# Conditionnal import
try:
    from paxpar.services.core.conf import get_conf

    MODULE_ENABLED = True
except ModuleNotFoundError:
    MODULE_ENABLED = False


console = Console()

app = typer.Typer(help="developement related commands")


if MODULE_ENABLED:

    @app.command()
    def all():
        """
        Start all paxpar services
        See .tmuxp.yaml for session details
        """
        call("""tmuxp load .""")

    @app.command()
    def core(
        container: bool = False,
        dry_run: bool = False,
        version: str = "4.2.1",
        entrypoint: str = "",
    ):
        """
        Start paxpar core service
        """
        # conf = get_conf()
        port = 8881

        if not container:
            # host = host_only(os.environ.get("SVC_CORE_PROXY", "0.0.0.0"))
            host = "0.0.0.0"
            cmd = rf"""
                poetry run uvicorn paxpar.services.core.main:app \
                    --host {host} \
                    --port {port} \
                    --reload \
            """
        else:
            # TODO: inject local IP
            cmd = rf"""
                docker run \
                    -ti \
                    --rm \
                    -p {port}:8881 \
                    -e PP_CONF \
                    --add-host=paxpar-conv:192.168.108.106 \
                    {f"--entrypoint {entrypoint}" if entrypoint != "" else ""} \
                    registry.gitlab.com/arundo-tech/paxpar/paxpar-core:v{version}
            """

        if dry_run:
            print(cmd)
        else:
            call(cmd)

    @app.command()
    def forge(
        browser: bool = True,
        token: Optional[str] = None,
        dry_run: bool = False,
        poetry: bool = True,
        container: bool = False,
    ):
        """
        Start paxpar forge service
        """
        conf = get_conf()
        token = token or conf.NOTEBOOK_TOKEN

        cmd = rf"""alias pp="$PWD/pp && "
            {"poetry run " if poetry else ""}jupyter lab \
            --config=$PWD/paxpar/services/forge/jupyter_notebook_config.json \
            --notebook-dir=$PWD/ref \
            --ServerApp.ip=* \
            --IdentityProvider.token={token} \
            --allow-root \
            {"" if browser else "--no-browser"} \
            -y
        """

        if dry_run:
            print(cmd)
        else:
            call(cmd)

    @app.command()
    def conv():
        """
        Start paxpar conv service
        """
        conf = get_conf()

        call(
            f"""podman run -it --rm \
            -p 0.0.0.0:{conf.services.conv.port}:3000 \
            {conf.services.conv.image}        
        """
        )

    @app.command()
    def store():
        """
        Start paxpar minio service (dev only)
        Shared volume is not working with docker desktop ??
        #-v $PWD/temp/s3:/data \
        #TODO: create bucket if volume is not persistent

        podman run -p 9000:9000 -p 9001:9001 minio/minio server /data --console-address ":9001"

        ./minio server /path/to/data 2>&1 | grep -oP '(?<=RequestHeader: Host: )[^ ]+|(?<=RequestPath: )[^ ]+' | paste -sd' \n'
        """
        conf = get_conf()

        call(
            rf"""podman run -it --rm \
            -v ~/minio/data:/data \
            -p 9000:{conf.services.store.port} \
            -p 9001:9001 \
            -e 'MINIO_ROOT_USER={conf.ref.sources.common.fsspec.key}' \
            -e 'MINIO_ROOT_PASSWORD={conf.ref.sources.common.fsspec.secret}' \
            -e 'MINIO_TRACE=1' \
            {conf.services.store.image} \
            server /data --console-address ":9001"
        """
        )

    @app.command()
    def office():
        """
        Start paxpar only office service (dev only)
        """
        # TODO: move secret to conf
        call(
            r"""
            docker run -it \
                -p 8303:80 \
                -e JWT_SECRET=VAmsYEiQRmOmOc2UomcEXxwLfmXMJWQt \
                onlyoffice/documentserver
        """
        )

else:
    console.print(f"CLI module {__name__} disabled", style="red")
