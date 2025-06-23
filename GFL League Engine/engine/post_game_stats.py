import json
from collections import defaultdict, Counter

# Load saved match file
with open("data/sample_match.json", "r") as f:
    match_data = json.load(f)

# Initialize stat counters
mvp_counter = Counter()
team_stats = defaultdict(lambda: {"points": 0, "blocks": 0, "turnovers": 0})

# Parse events for stats
for event in match_data["events"]:
    team = event["team"]
    player = event["player"]
    description = event["description"].lower()

    if "scores" in description:
        team_stats[team]["points"] += 2
        mvp_counter[player] += 2
    elif "block" in description:
        team_stats[team]["blocks"] += 1
        mvp_counter[player] += 1
    elif "turnover" in description or "turns it over" in description:
        team_stats[team]["turnovers"] += 1
        mvp_counter[player] -= 1

# Determine MVP
mvp_name, mvp_score = mvp_counter.most_common(1)[0]

# Build report
report = {
    "final_score": match_data["score"],
    "team_stats": dict(team_stats),
    "top_5_plays": match_data["events"][:5],
    "mvp": {
        "name": mvp_name,
        "impact_score": mvp_score
    }
}

# Save report
with open("data/post_game_report.json", "w") as f:
    json.dump(report, f, indent=4)

# Print summary
print(f"\n🏆 MVP: {mvp_name} with impact score {mvp_score}")
print("📊 Team Totals:")
for team, stats in report["team_stats"].items():
    print(f" - {team}: {stats['points']} pts, {stats['blocks']} blocks, {stats['turnovers']} TOs")
