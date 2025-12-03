# main.py
import click
from datetime import datetime
from lib.db.session import get_db, init_db
from lib.db.models import Bookmaker, Bet, Bankroll, BankrollSnapshot
from rich.console import Console
from rich.table import Table

console = Console()

@click.group()
def cli():
    """BetCLI – Professional Sports Betting Tracker"""
    pass

# Run this once at startup
init_db()

@cli.command()
@click.argument("name")
def add_bookmaker(name):
    """Add a new bookmaker"""
    db = next(get_db())
    if db.query(Bookmaker).filter_by(name=name).first():
        click.echo(f"Bookmaker '{name}' already exists!")
        return
    bookmaker = Bookmaker(name=name)
    db.add(bookmaker)
    db.commit()
    click.echo(f"Bookmaker '{name}' added!")

@cli.command()
@click.argument("event")
@click.argument("selection")
@click.argument("odds", type=float)
@click.argument("stake", type=float)
@click.argument("sport")
@click.argument("bookmaker_name")
def add_bet(event, selection, odds, stake, sport, bookmaker_name):
    """Add a new bet"""
    db = next(get_db())
    bookmaker = db.query(Bookmaker).filter_by(name=bookmaker_name).first()
    if not bookmaker:
        click.echo(f"Bookmaker '{bookmaker_name}' not found! Add it first.")
        return
    bet = Bet(event=event, selection=selection, odds=odds, stake=stake, sport=sport, bookmaker=bookmaker)
    db.add(bet)
    db.commit()
    click.echo(f"Bet added: {event} - {selection} at {odds} odds, stake ${stake:.2f} on {sport}")

@cli.command()
def list_bookmakers():
    """List all bookmakers"""
    db = next(get_db())
    bookmakers = db.query(Bookmaker).all()
    from tabulate import tabulate
    if bookmakers:
        headers = ["ID", "Name"]
        rows = [[b.id, b.name] for b in bookmakers]
        click.echo(tabulate(rows, headers=headers, tablefmt="grid"))
    else:
        click.echo("No bookmakers found.")

@cli.command()
def list_bets():
    """List all bets with profit/loss"""
    db = next(get_db())
    bets = db.query(Bet).all()
    table = Table(title="Bets")
    table.add_column("ID")
    table.add_column("Date")
    table.add_column("Sport")
    table.add_column("Event")
    table.add_column("Selection")
    table.add_column("Odds")
    table.add_column("Stake")
    table.add_column("Result")
    table.add_column("P/L")
    table.add_column("Bookmaker")
    for bet in bets:
        table.add_row(
            str(bet.id),
            bet.date_placed.strftime("%Y-%m-%d"),
            bet.sport,
            bet.event,
            bet.selection,
            str(bet.odds),
            f"${bet.stake:.2f}",
            bet.result,
            f"${bet.profit_loss():.2f}",
            bet.bookmaker.name
        )
    console.print(table)

if __name__ == "__main__":
    cli()
