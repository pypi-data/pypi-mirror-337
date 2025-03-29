"""
This script uses argparse to parse command line arguments.

It imports the required modules and sets up a parser with basic options for demonstration purposes.
"""
import argparse
from nba import fetch_data, scores, standings

def nba() -> None:
        """
        Parse command-line arguments and display either scoreboard or standings.
        """
        parser = argparse.ArgumentParser(description="NBA Scoreboard and Standings")
        parser.add_argument('--scores', '-sc', action='store_true', help='Display the scoreboard')
        parser.add_argument('--standings', '-st', action='store_true', help='Display the standings')
        args = parser.parse_args()

        games, ranks = fetch_data.fetch_data()

        if args.scores:
                scores.build_scoreboard(games, ranks)
        elif args.standings:
                standings.build_standings(ranks)
        else:
                print("Please specify --scores or --standings")
