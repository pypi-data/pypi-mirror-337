"""
Tabulate the current conference standings.
"""
from tabulate import tabulate

# ANSI escape codes for text formatting
BOLD = '\033[1m'
END = '\033[0m'
RED = '\033[91m'
GREEN = '\033[32m'

def build_standings(standings) -> None:
	"""
	Prints team standings in two separate tables.

	Args:
		standings (dict): Team standings data.
	"""
	eastern_data = []
	western_data = []
	eastern_rank = 1
	western_rank = 1

	for result_set in standings['resultSets']:
		if result_set['name'] == 'Standings':
			for team in result_set['rowSet']:
				conference = team[5]
				team_name = team[4]
				wins = team[12]
				losses = team[13]
				win_pct = team[14]
				gb = team[37]
				home_record = team[17]
				away_record = team[18]
				last_10 = team[19]
				streak = team[35]

				if int(streak) < 0:
					strk_color = f"{RED}{streak}{END}"
				else:
					strk_color = f"{GREEN}{streak}{END}"

				if conference == "East":
					eastern_data.append([
					f"{eastern_rank}",
					f"{team_name}",
					f"{wins}-{losses}",
					f"{win_pct:.3f}",
					f"{gb}",
					f"{strk_color}",
					f"{last_10}",
					f"{home_record}",
					f"{away_record}"
					])
					eastern_rank += 1
				elif conference == "West":
					western_data.append([
						f"{western_rank}",
						f"{team_name}",
						f"{wins}-{losses}",
						f"{win_pct:.3f}",
						f"{gb}",
						f"{strk_color}",
						f"{last_10}",
						f"{home_record}",
						f"{away_record}"
					])
					western_rank += 1

	headers = ["Rank", "Team", "W-L", "PCT", "GB", "STRK", "L10", "HOME", "AWAY"]

	print(f"{BOLD}Eastern Conference Standings:{END}")
	print(tabulate(eastern_data, headers=headers, tablefmt="grid"))

	print("\n")
	print(f"{BOLD}Western Conference Standings:{END}")
	print(tabulate(western_data, headers=headers, tablefmt="grid"))
