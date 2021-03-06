import os, sys
sys.path.append(os.getcwd())

import click
from flask.cli import with_appcontext
from learnware.app import _db


@click.group()
def cli():
    """Main entry point"""


@cli.command("init")
@with_appcontext
def init():
    from learnware.model.models import DataSource, DataSet, Learnware
    click.echo("___drop_table___")
    _db.drop_all()
    click.echo("__create_table__")
    _db.create_all()
    click.echo("__init_over___")


if __name__ == "__main__":
    cli()
