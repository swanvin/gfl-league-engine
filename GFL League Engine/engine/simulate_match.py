# engine/simulate_match.py

import random
from engine.player_model import GFLPlayer

# Simulated teams with real players
def create_team(name):
    positions = ["Attacker", "Midfield", "Defender", "Flex", "Specialist"]
    return [GFLPlayer(f"{name[:2]}_{pos[:2]}_{i}", pos) for i, pos in enumerate(positions)]

# Simulate one match with full player logic
def simulate_match(team1_name, team2_name):
    print(f"\n🕹 Simulating: {team1_name} vs. {team2_name}")

    team1 = create_team(team1_name)
    team2 = create_team(team2_name)
    score = {team1_name: 0, team2_name: 0}
    events = []

    for quarter in range(1, 5):
        print(f"\n🏀 Q{quarter} Begins")
        for _ in range(6):  # 6 possessions per quarter
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

            # Random defensive play from opposing team
            defense_team = team1 if name == team2_name else team2
            defender = random.choice(defense_team)
            block_result = defender.simulate_defense()
            if block_result:
                events.append({
                    "quarter": quarter,
                    "team": defender.name,
                    "player": defender.name,
                    "description": block_result,
                    "points": 0
                })

    # Output summary
    print(f"\n🔚 Final Score: {team1_name} {score[team1_name]} – {team2_name} {score[team2_name]}")
    return {
        "score": score,
        "events": events,
        "team1": team1,
        "team2": team2
    }

# Run simulation
if __name__ == "__main__":
    output = simulate_match("Rio Blaze", "Berlin Core")
    for e in output["events"][:5]:
        print(f"Q{e['quarter']} | {e['team']} | {e['description']}")
