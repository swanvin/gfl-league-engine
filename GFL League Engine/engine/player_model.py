# engine/player_model.py

import random

class GFLPlayer:
    def __init__(self, name, position):
        self.name = name
        self.position = position

        # Base traits (can be adjusted per team/player)
        self.scoring = random.randint(65, 90)      # 0–100
        self.defense = random.randint(60, 85)
        self.stamina = 100
        self.clutch = random.randint(70, 95)
        self.momentum_sensitivity = random.uniform(0.8, 1.2)

        self.stats = {
            "points": 0,
            "blocks": 0,
            "turnovers": 0
        }

    def simulate_possession(self, game_context):
        """
        Run 1 offensive possession and return outcome.
        """
        fatigue_penalty = (100 - self.stamina) * 0.3
        clutch_boost = self.clutch if game_context["is_clutch_time"] else 0
        momentum_factor = game_context.get("momentum", 1.0)

        # Scoring chance calculation
        scoring_chance = self.scoring - fatigue_penalty + clutch_boost
        scoring_chance *= momentum_factor * self.momentum_sensitivity

        score = random.random() < (scoring_chance / 150)  # tuned scale
        if score:
            self.stats["points"] += 2
            self.stamina -= random.uniform(3, 6)
            return f"{self.name} scores 2 pts!"
        else:
            self.stamina -= random.uniform(2, 4)
            turnover = random.random() < 0.15
            if turnover:
                self.stats["turnovers"] += 1
                return f"{self.name} turns it over!"
            return f"{self.name} misses the shot."

    def simulate_defense(self):
        block_chance = self.defense * (self.stamina / 100)
        if random.random() < block_chance / 250:
            self.stats["blocks"] += 1
            self.stamina -= random.uniform(2, 5)
            return f"{self.name} makes a game-changing block!"
        return None

    def __str__(self):
        return f"{self.name} ({self.position}) – {self.stats}, stamina: {int(self.stamina)}%"
