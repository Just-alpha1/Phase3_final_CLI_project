##Scholar Betting Tracker

##Description

Scholar Betting Tracker is a professional sports betting CLI application built with Python, SQLAlchemy, and Click. It helps users track their bets, manage bankrolls, calculate profits/losses, and make data-driven decisions to improve long-term betting performance. All data is securely stored in a local SQLite database, ensuring persistent and accurate records without relying on external services.

##Author

Collins Kiaritha Thuo

##Setup Instructions

1.Clone this repository:
   git clone:git@github.com:Just-alpha1/Phase3_final_CLI_project.git
2.Navigate into the project directory:
  cd betting-tracker
3.Install Pipenv if not already installed:
  pip install pipenv
4.Install dependencies and activate the virtual environment:
  pipenv install
  pipenv shell
5.Install the package in editable mode:
  pipenv install -e .

##BDD(Behavior Driven Development)

1.Input: Add a bookmaker with a name (e.g., "Pinnacle")
  Output: Bookmaker added and stored in the database
2.Input: Add a bet with event, selection, odds, stake, sport, and bookmaker
  Output: Bet recorded and saved in the database
3.Input: Invalid input (e.g., negative stake or non-existent bookmaker)
  Output: Error message requesting valid input
4.Input: List all bets
  Output: Beautiful table displaying IDs, dates, sports, events, selections, odds, stakes, results, P/L, and bookmakers
5.Input: Update bet result (e.g., mark as "won" or "lost")
  Output: Result updated, profit/loss calculated, and bankroll adjusted automatically
6.Input: View current bankroll and stats
  Output: Displays current balance, total profit, ROI (%), win rate, average odds, and total bets
7.Input: Calculate Kelly stake with odds, probability, and bankroll
  Output: Recommendations for full, half, and quarter Kelly stakes
8.Input: Export bets to CSV
  Output: All bets exported to a CSV file
9.Input: Exit application
  Output: Program closes successfully

##Technologies Used

1.Python 3.x
2.SQLAlchemy
3.Click 
4.SQLite
5.Pipenv
6.Pytest 
7.Object-Oriented Programming (OOP)

##Contact Information

GitHub:https://github.com/Just-alpha1/Phase3_final_CLI_project.git

##License

MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.