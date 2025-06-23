import json
import os
from collections import defaultdict, Counter

# Load latest match data
with open("data/sample_match.json", "r") as f:
    match = json.load(f)

team1, team2 = list(match["score"].keys())
score1, score2 = match["score"][team1], match["score"][team2]

winner = team1 if score1 > score2 else team2
loser = team2 if winner == team1 else team1

# Determine MVP from impact events
mvp_counter = Counter()
for event in match["events"]:
    name = event["player"]
    desc = event["description"].lower()
    if "scores" in desc:
        mvp_counter[name] += 2
    elif "block" in desc:
        mvp_counter[name] += 1
    elif "turnover" in desc or "turns it over" in desc:
        mvp_counter[name] -= 1
mvp, _ = mvp_counter.most_common(1)[0]

# Load or initialize season stats
season_file = "data/season_stats.json"
if os.path.exists(season_file):
    with open(season_file, "r") as f:
        season = json.load(f)
else:
    season = {"teams": {}, "matches": []}

# Initialize teams if not in season yet
for team in [team1, team2]:
    if team not in season["teams"]:
        season["teams"][team] = {
            "wins": 0, "losses": 0,
            "points_scored": 0, "points_allowed": 0,
            "mvp_awards": 0
        }

# Update records
season["teams"][winner]["wins"] += 1
season["teams"][loser]["losses"] += 1
season["teams"][team1]["points_scored"] += score1
season["teams"][team1]["points_allowed"] += score2
season["teams"][team2]["points_scored"] += score2
season["teams"][team2]["points_allowed"] += score1
season["teams"][winner]["mvp_awards"] += 1

# Log the match
season["matches"].append({
    "team1": team1,
    "score1": score1,
    "team2": team2,
    "score2": score2,
    "winner": winner,
    "mvp": mvp
})

# Save updated season
with open(season_file, "w") as f:
    json.dump(season, f, indent=4)

print("\n✅ GFL Season Tracker Updated\n")

print("🏆 Match Result:")
print(f"• {team1:<12} {score1}")
print(f"• {team2:<12} {score2}")
print(f"• Winner: {winner}")
print(f"• MVP: {mvp} ({mvp_counter[mvp]} impact points)\n")

print("📈 Season Records:")
for team in [winner, loser]:
    rec = season["teams"][team]
    print(f"• {team:<12} — W: {rec['wins']} | L: {rec['losses']} | PF: {rec['points_scored']} | PA: {rec['points_allowed']} | MVPs: {rec['mvp_awards']}")

print(f"\n📂 Match Log Updated — {len(season['matches'])} total match{'es' if len(season['matches']) != 1 else ''} saved to season_stats.json")

