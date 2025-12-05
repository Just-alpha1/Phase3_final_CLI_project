import click
from datetime import datetime
from lib.db.session import get_db, init_db
from lib.db.models import Bookmaker, Bet, Bankroll, BankrollSnapshot

@click.group()
def cli():
    pass

init_db()

@cli.command()
@click.argument("name")
def add_bookmaker(name):
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
@click.argument("bookmaker_name")
def add_bet(event, selection, odds, stake, bookmaker_name):
    db = next(get_db())
    bookmaker = db.query(Bookmaker).filter_by(name=bookmaker_name).first()
    if not bookmaker:
        click.echo(f"Bookmaker '{bookmaker_name}' not found! Add it first.")
        return
    bet = Bet(event=event, selection=selection, odds=odds, actual_stake=stake, bookmaker=bookmaker)
    db.add(bet)
    db.commit()
    click.echo(f"Bet placed: {event} - {selection} at {odds} odds, ${stake:.2f} staked")

@cli.command()
def list_bookmakers():
    db = next(get_db())
    bookmakers = db.query(Bookmaker).all()
    if bookmakers:
        for b in bookmakers:
            click.echo(f"{b.id}: {b.name}")
    else:
        click.echo("No bookmakers found.")

@cli.command()
def list_bets():
    db = next(get_db())
    bets = db.query(Bet).all()
    if bets:
        for bet in bets:
            click.echo(f"{bet.id}: {bet.date_placed.strftime('%Y-%m-%d')} - {bet.event} - {bet.selection} - {bet.odds} - ${bet.actual_stake:.2f} - {bet.outcome} - ${bet.profit_loss():.2f} - {bet.bookmaker.name}")
    else:
        click.echo("No bets found.")

@cli.command()
@click.argument("bet_id", type=int)
@click.argument("outcome")
def update_bet_result(bet_id, outcome):
    db = next(get_db())
    bet = db.query(Bet).filter_by(id=bet_id).first()
    if not bet:
        click.echo(f"Bet with ID {bet_id} not found!")
        return
    bet.outcome = outcome
    db.commit()
    click.echo(f"Bet {bet_id} outcome updated to '{outcome}'")

@cli.command()
@click.argument("bet_id", type=int)
def delete_bet(bet_id):
    db = next(get_db())
    bet = db.query(Bet).filter_by(id=bet_id).first()
    if not bet:
        click.echo(f"Bet with ID {bet_id} not found!")
        return
    db.delete(bet)
    db.commit()
    click.echo(f"Bet {bet_id} deleted!")

@cli.command()
@click.argument("balance", type=float)
def set_bankroll(balance):
    db = next(get_db())
    bankroll = db.query(Bankroll).first()
    if bankroll:
        bankroll.balance = balance
    else:
        bankroll = Bankroll(balance=balance)
        db.add(bankroll)
    db.commit()
    click.echo(f"Bankroll set to ${balance:.2f}!")

@cli.command()
def show_bankroll():
    db = next(get_db())
    bankroll = db.query(Bankroll).first()
    if bankroll:
        click.echo(f"Current Balance: ${bankroll.balance:.2f}")
    else:
        click.echo("No bankroll set. Use 'set-bankroll' to set one.")

@cli.command()
@click.argument("odds", type=float)
@click.argument("probability", type=float)
@click.argument("bankroll", type=float)
def kelly_calculator(odds, probability, bankroll):
    kelly = ((odds - 1) * probability - (1 - probability)) / (odds - 1)
    full_kelly = kelly * bankroll
    half_kelly = full_kelly / 2
    quarter_kelly = full_kelly / 4
    click.echo(f"Full Kelly: ${full_kelly:.2f}")
    click.echo(f"Half Kelly: ${half_kelly:.2f}")
    click.echo(f"Quarter Kelly: ${quarter_kelly:.2f}")

@cli.command()
@click.argument("filename")
def export_bets(filename):
    db = next(get_db())
    bets = db.query(Bet).all()
    import csv
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ID', 'Date', 'Event', 'Selection', 'Odds', 'Stake', 'Outcome', 'P/L', 'Bookmaker'])
        for bet in bets:
            writer.writerow([
                bet.id,
                bet.date_placed.strftime("%Y-%m-%d"),
                bet.event,
                bet.selection,
                bet.odds,
                bet.actual_stake,
                bet.outcome,
                bet.profit_loss(),
                bet.bookmaker.name
            ])
    click.echo(f"Bets exported to {filename}!")

if __name__ == "__main__":
    cli()
