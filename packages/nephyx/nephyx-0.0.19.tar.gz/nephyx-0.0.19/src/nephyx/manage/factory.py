import json
from pathlib import Path
import subprocess
from typing import Annotated
from fastapi import FastAPI
import typer
import sys
import getpass

from nephyx.manage.postgres import setup_database


def build_cli(fastapi_app: FastAPI, get_settings) -> typer.Typer:

    app = typer.Typer()

    @app.command()  # TODO get from settings
    def init_db():
        db_host = "localhost"
        db_port = "5432"

        db_admin_user = typer.prompt("Enter database admin user")
        db_admin_password = getpass.getpass("Enter database admin password")

        # take from config
        db_name = typer.prompt("Enter database name")
        db_user = typer.prompt("Enter database user")
        db_password = getpass.getpass("Enter database password")

        admin_config = {
            "host": db_host,
            "port": db_port,
            "user": db_admin_user,
            "password": db_admin_password,
        }

        setup_database(admin_config, db_name, db_user, db_password)

    @app.command()
    def export_openapi():
        sys.path.insert(0, "")
        openapi = fastapi_app.openapi()
        with Path("openapi.json").open("w") as f:
            json.dump(openapi, f, indent=2)

    @app.command()
    def makemigrations(comment: Annotated[str, typer.Argument()] = "auto"):
        """
        Make Alembic migrations
        """
        try:
            revision_command = f"alembic revision --autogenerate -m {comment}"
            print(f"Running Alembic migrations: {revision_command}")
            subprocess.run(revision_command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"[red]Error:[/red] {e}")
            return
        print("[green]Make migrations complete[/green]")


    @app.command()
    def migrate():
        """
        Run Alembic migrations
        """
        try:
            upgrade_command = "alembic upgrade head"
            print(f"Running Alembic upgrade: {upgrade_command}")
            subprocess.run(upgrade_command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"[red]Error:[/red] {e}")
            return
        print("[green]Migration complete[/green]")


    @app.command()
    def runserver():
        """
        Run the FastAPI server
        """
        try:
            server_command = (
                "fastapi dev app/main.py"
                if get_settings().debug
                else "fastapi run app/main.py"
            )
            print(f"Running FastAPI server: {server_command}")
            subprocess.run(server_command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"[red]Error:[/red] {e}")
            return

    return app
