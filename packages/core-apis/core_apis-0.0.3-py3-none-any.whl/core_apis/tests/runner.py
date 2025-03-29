# -*- coding: utf-8 -*-

from click.decorators import group


@group()
def cli_api():
    pass


@cli_api.command("run-api")
def run_api():
    from core_apis.api import server
    server.run(getattr(cli_api, "app", None))
