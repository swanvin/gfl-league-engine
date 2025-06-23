import json
from tabulate import tabulate

# Load the latest season stats
with open("data/season_stats.json", "r") as f:
    season = json.load(f)

teams = season["teams"]

# Prepare rows for the standings table
table = []
for team, stats in teams.items():
    wins = stats["wins"]
    losses = stats["losses"]
    pf = stats["points_scored"]
    pa = stats["points_allowed"]
    diff = pf - pa
    mvp = stats["mvp_awards"]
    table.append([team, wins, losses, pf, pa, diff, mvp])

# Sort: first by wins descending, then point diff
table.sort(key=lambda x: (-x[1], -x[5]))

# Print standings
headers = ["Team", "W", "L", "PF", "PA", "Diff", "MVPs"]
print("\n📊 GFL LEAGUE STANDINGS\n")
print(tabulate(table, headers=headers, tablefmt="fancy_grid"))
