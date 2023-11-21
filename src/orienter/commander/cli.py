import click


@click.group()
def cli():
    ...
    # this will contain a call to the menu in case no parameters are passed


@cli.command()
@click.argument('user-ids', type=str)
def statistics(user_ids: str):
    click.echo(f"passed ids: {user_ids}")
    # TODO: implement command


@cli.command()
@click.argument('month', type=int)
def races_in_month(month: str):
    click.echo(f"passed month: {month}")
    # TODO: implement command


@cli.command()
@click.argument('race-id', type=int)
def add_race(race_id: int):
    click.echo(f"passed race id: {race_id}")
    # TODO: implement command


@cli.command()
@click.argument('race-id', type=int)
def signedup_racers(race_id: int):
    click.echo(f"passed race id: {race_id}")
    # TODO: implement command


@cli.command()
@click.argument('race-id', type=int)
@click.argument('racer-id', type=int)
def signup_racer_to_api(race_id: int, racer_id: int):
    click.echo(f"passed race id: {race_id}")
    click.echo(f"passed racer id: {racer_id}")
    # TODO: implement command


if __name__ == "__main__":
    cli()
