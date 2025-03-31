import subprocess

import typer
from rich import print

from .api import api as api_app
from .common import UpdateConfigOption, ensure_root
from .config import config as config_app
from .config.config import get_config
from .service import SharedContext, get_context_obj, service as service_app
from .service.manager import create_service

app = typer.Typer(help="sing-box manager.")
app.add_typer(api_app)
app.add_typer(service_app, name="service")
app.add_typer(config_app, name="config")


@app.callback(invoke_without_command=False)
def callback(ctx: typer.Context) -> None:
    cfg = get_config()
    service = create_service(cfg)
    ctx.obj = SharedContext(config=cfg, service=service)


@app.command()
def run(ctx: typer.Context, update: UpdateConfigOption = False) -> None:
    """Run sing-box if host's service unavailable"""
    ensure_root()
    cfg = get_context_obj(ctx).config
    if update:
        if cfg.update_config():
            pass
        else:
            print("❌ Failed to update configuration.")
            raise typer.Exit(1)

    cmd = [
        str(cfg.bin_path),
        "run",
        "-C",
        str(cfg.config_dir),
        "-D",
        str(cfg.config_dir),
    ]
    subprocess.run(cmd)


@app.command()
def version(ctx: typer.Context) -> None:
    """Show version"""
    from . import __version__

    print(f"🔖 sing-box-cli {__version__}")
    print(f"📦 {get_context_obj(ctx).service.version()}")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
