# media/highlight_script_generator.py

import json
from collections import Counter

def generate_highlights(match_data):
    events = match_data.get("events", [])
    score = match_data.get("score", {})
    team_scores = {team: 0 for team in score}
    highlight_tags = []

    # Track scoring and momentum
    for i, event in enumerate(events):
        team = event["team"]
        points = event["points"]
        team_scores[team] += points

        tag = None

        # Buzzer Beater
        if i == len(events) - 1 and event["quarter"] == 4:
            tag = f"🔥 Buzzer Beater by {team}: {event['description']}"

        # Momentum Swing
        elif i >= 2 and team == events[i-1]["team"] == events[i-2]["team"]:
            tag = f"🚀 {team} goes on a 3-possession streak – Momentum Shift!"

        # Game-Changing Block (placeholder logic — needs future defense events)
        elif "block" in event["description"].lower():
            tag = f"🧱 {team} with a Game-Changing Block!"

        if tag:
            highlight_tags.append({
                "quarter": event["quarter"],
                "event": event["description"],
                "tag": tag
            })

    # Determine MVP (most scoring plays)
    scorer_names = [e["description"].split()[0] for e in events if "scores" in e["description"]]
    if scorer_names:
        top_scorer = Counter(scorer_names).most_common(1)[0][0]
        highlight_tags.append({
            "quarter": "🏆",
            "event": f"{top_scorer} led all scorers",
            "tag": f"👑 MVP Playmaker: {top_scorer}"
        })

    return highlight_tags

# Example usage
if __name__ == "__main__":
    with open("sample_match.json", "r") as f:
        match_data = json.load(f)

    highlights = generate_highlights(match_data)
    for h in highlights:
        print(f"Q{h['quarter']}: {h['tag']}")
