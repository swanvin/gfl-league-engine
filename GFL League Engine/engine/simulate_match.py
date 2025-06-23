# engine/simulate_match.py

import random
import json
from datetime import datetime

# Load players and teams from data (placeholder logic)
def load_team_data():
    try:
        with open("data/team_rosters.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "Rio Blaze": ["Player A", "Player B", "Player C"],
            "Berlin Core": ["Player X", "Player Y", "Player Z"]
        }

# Core match simulation
def simulate_match(team1, team2):
    print(f"🕹 Simulating match: {team1} vs. {team2}")
    teams = load_team_data()
    score = {team1: 0, team2: 0}
    events = []

    for quarter in range(1, 5):
        for _ in range(6):  # 6 possessions per quarter
            attacker = random.choice([team1, team2])
            defender = team2 if attacker == team1 else team1
            success = random.random() < 0.52  # 52% chance of scoring
            points = 2 if random.random() < 0.8 else 3

            if success:
                score[attacker] += points
                event = {
                    "quarter": quarter,
                    "team": attacker,
                    "points": points,
                    "description": f"{random.choice(teams[attacker])} scores {points} pts"
                }
                events.append(event)

    result = {
        "match_id": f"{team1[:2]}_vs_{team2[:2]}_{datetime.now().strftime('%Y%m%d%H%M')}",
        "score": score,
        "events": events
    }

    return result

# Example usage
if __name__ == "__main__":
    output = simulate_match("Rio Blaze", "Berlin Core")
    print(f"Final Score: {output['score']}")
    print("Sample Event Log:")
    for e in output["events"][:5]:
        print(f"Q{e['quarter']} – {e['description']}")
