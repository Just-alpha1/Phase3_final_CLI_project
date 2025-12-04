import click
from datetime import datetime
from lib.db.session import getdb, initdb
from lib.db.models import Bookmaker, Bet, Bankroll, BankrollSnapshot
from rich.console import Console
from rich.table import Table

console = Console()

@click.group()
def cli():
    """BetCLI - Scholar betting tracker"""
    pass

initdb()

@cli.command()
@click.argument("name")
def addbookmaker(name: str):
    db = next(getdb())
    if db.query(Bookmaker).filterby(name=name).first():
        click.echo(f"Bookmaker '{name}' already exists!")
        return
    bookmaker = Bookmaker(name=name)
    db.add(bookmaker)
    db.commit()
    click.echo(f"Bookmaker '{name}' added successfully!")

@cli.command()
@click.argument("event")
@click.argument("selection")
@click.argument("odds", type=float)
@click.argument("stake", type=float)
@click.argument("sport")
@click.argument("bookmakername")
def addbet(event: str, selection: str, odds: float, stake: float, sport: str, bookmakername: str):
    db = next(getdb())
    bookmaker = db.query(Bookmaker).filterby(name=bookmakername).first()
    if not bookmaker:
        click.echo(f"Bookmaker '{bookmakername}' not found! Please add it first using 'addbookmaker'.")
        return
    bet = Bet(
        event=event,
        selection=selection,
        odds=odds,
        stake=stake,
        sport=sport,
        bookmaker=bookmaker
    )
    db.add(bet)
    db.commit()
    click.echo(f"Bet placed: {event} - {selection} at {odds} odds, ${stake:.2f} staked on {sport} with {bookmakername}")

@cli.command()
def listbookmakers():
    db = next(getdb())
    bookmakers = db.query(Bookmaker).all()
    if bookmakers:

        table = Table(title="Bookmakers")
        table.addcolumn("ID")
        table.addcolumn("Name")
        for bookmaker in bookmakers:
            table.addrow(str(bookmaker.id), bookmaker.name)
        console.print(table)
    else:
        click.echo("No bookmakers found. Add some using 'addbookmaker'!")

@cli.command()
def listbets():
    db = next(getdb())
    bets = db.query(Bet).all()
    if bets:
        table = Table(title="All Bets")
        table.addcolumn("ID", style="cyan")
        table.addcolumn("Date Placed", style="magenta")
        table.addcolumn("Sport")
        table.addcolumn("Event")
        table.addcolumn("Selection")
        table.addcolumn("Odds")
        table.addcolumn("Stake")
        table.addcolumn("Result")
        table.addcolumn("P/L")
        table.addcolumn("Bookmaker")

        for bet in bets:
            table.addrow(
                str(bet.id),
                bet.dateplaced.strftime("%Y-%m-%d"),
                bet.sport,
                bet.event,
                bet.selection,
                str(bet.odds),
                f"${bet.stake:.2f}",
                bet.result or "Pending",
                f"${bet.profitloss():.2f}",
                bet.bookmaker.name
            )
        console.print(table)
    else:
        click.echo("No bets found. Add some using 'add_bet'!")

if name == "main":
    cli()