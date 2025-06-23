# engine/simulate_match.py

import random
from engine.player_model import GFLPlayer
import json

def create_team_from_json(team_name):
    with open("../data/team_rosters.json", "r") as f:
        rosters = json.load(f)
    team_data = rosters[team_name]
    
    players = []
    for entry in team_data:
        name_part, role_part = entry.rsplit("(", 1)
        name = name_part.strip()
        position = role_part.replace(")", "").strip()
        players.append(GFLPlayer(name, position))
    return players

# Updated simulate_match() — use create_team_from_json
def simulate_match(team1_name, team2_name):
    print(f"\n🕹 Simulating: {team1_name} vs. {team2_name}")

    team1 = create_team_from_json(team1_name)
    team2 = create_team_from_json(team2_name)
    score = {team1_name: 0, team2_name: 0}
    events = []

    for quarter in range(1, 5):
        print(f"\n🏀 Q{quarter} Begins")
        for _ in range(6):
            attacking_team = random.choice([(team1_name, team1), (team2_name, team2)])
            name, roster = attacking_team
            player = random.choice(roster)
            is_clutch = (quarter == 4)
            result = player.simulate_possession({"is_clutch_time": is_clutch, "momentum": 1.0})

            if "scores" in result:
                score[name] += 2
                events.append({
                    "quarter": quarter,
                    "team": name,
                    "player": player.name,
                    "description": result,
                    "points": 2
                })
            elif "turns" in result:
                events.append({
                    "quarter": quarter,
                    "team": name,
                    "player": player.name,
                    "description": result,
                    "points": 0
                })

            defense_team = team1 if name == team2_name else team2
            defender = random.choice(defense_team)
            block_result = defender.simulate_defense()
            if block_result:
                events.append({
                    "quarter": quarter,
                    "team": team2_name if name == team1_name else team1_name,
                    "player": defender.name,
                    "description": block_result,
                    "points": 0
                })

    print(f"\n🔚 Final Score: {team1_name} {score[team1_name]} – {team2_name} {score[team2_name]}")
    return {
        "score": score,
        "events": events,
    }

import json

# Run match
if __name__ == "__main__":
    result = simulate_match("Rio Blaze", "Berlin Core")

    # Save full match log
    with open("../data/sample_match.json", "w") as f:
        json.dump(result, f, indent=4)
