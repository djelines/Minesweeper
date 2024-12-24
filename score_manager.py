import json
import os


class ScoreManager:
    def __init__(self, score_file="scores.json"):
        self.score_file = score_file
        self.data = self.__load_data()

    def __load_data(self):
        if os.path.exists(self.score_file):
            with open(self.score_file, "r", encoding="utf-8") as file:
                return json.load(file)
        return {"scores": {}}

    def __save_data(self):
        with open(self.score_file, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4)

    def add_score(self, player_name, elapsed_time, difficulty, grid_id):
        if difficulty not in self.data["scores"]:
            self.data["scores"][difficulty] = []

        self.data["scores"][difficulty].append({
            "player_name": player_name,
            "elapsed_time": elapsed_time,
            "grid_id": grid_id
        })
        self.data["scores"][difficulty].sort(key=lambda x: x["elapsed_time"])
        self.__save_data()

    def get_hall_of_fame(self, difficulty):
        return self.data["scores"].get(difficulty, [])[:10]
