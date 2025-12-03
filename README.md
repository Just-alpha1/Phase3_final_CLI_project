A professional sports betting tracker CLI application built with Python, SQLAlchemy, and Click.

## Features

- Add and manage bookmakers
- Track bets with odds, stakes, and results
- Bankroll management
- Profit/loss calculations
- Export bets to CSV
- Kelly criterion calculator

## Installation

1. Install Pipenv if not already installed:
   ```bash
   pip install pipenv
   ```

2. Install dependencies:
   ```bash
   pipenv install
   ```

3. Activate the virtual environment:
   ```bash
   pipenv shell
   ```

4. Install the package in editable mode:
   ```bash
   pipenv install -e .
   ```

## Usage

Run the CLI:
```bash
betcli --help
```

Add a bookmaker:
```bash
betcli add-bookmaker "Pinnacle"
```

List bookmakers:
```bash
betcli list-bookmakers
```

## Development

To run tests:
```bash
pytest
=======
# Scholar Betting Tracker

A professional sports betting tracker CLI application built with Python, SQLAlchemy, and Click.

## Problem Statement
Most sports bettors lose money long-term because they fail to track their bets, manage their bankroll properly, and make decisions based on emotion rather than data — Scholar Betting Tracker solves this by providing a fast, local, professional-grade betting tracker and performance analyzer directly from the terminal.

## Features

### MVP (Minimum Viable Product)
- **Add a Bet**: Enter event, selection, decimal odds, stake, sport, date, and bookmaker
- **List All Bets**: Display all bets in a beautiful table with ID, date, sport, event, selection, odds, stake, result, P/L, and bookmaker
- **Delete Bets**: Permanently clear bets from the slip
- **Update Bet Result**: Mark a bet as Won/Lost/Push/Void (automatically updates profit/loss and bankroll)
- **View Current Bankroll & Performance Stats**: Shows current balance, total profit, ROI (%), win rate, average odds, total bets
- **Calculate Kelly Stake**: Input odds and estimated probability → returns full, half, and quarter Kelly stake recommendations
- **Persistent Storage**: All data stored in a local SQLite database
- **Export Data**: Export all bets to CSV with one command

## Installation

1. Install Pipenv if not already installed:
   ```bash
   pip install pipenv
   ```

2. Install dependencies:
   ```bash
   pipenv install
   ```

3. Activate the virtual environment:
   ```bash
   pipenv shell
   ```

4. Install the package in editable mode:
   ```bash
   pipenv install -e .
   ```

## Usage

Run the CLI:
```bash
python main.py --help
```

Add a bookmaker:
```bash
python main.py add-bookmaker "Pinnacle"
```

Add a bet:
```bash
python main.py add-bet "Liverpool vs Chelsea" "Liverpool" 2.1 100 "Soccer" "Pinnacle"
```

List all bets:
```bash
python main.py list-bets
```

Update bet result:
```bash
python main.py update-bet-result 1 won
```

Set bankroll:
```bash
python main.py set-bankroll 1000
```

Show bankroll stats:
```bash
python main.py show-bankroll
```

Kelly calculator:
```bash
python main.py kelly-calculator 2.1 60 1000
```

Export bets to CSV:
```bash
python main.py export-bets
```

## Development

To run tests:
```bash
pytest
