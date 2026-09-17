import json
from pathlib import Path
from typing import List


class Score:
    def __init__(self):
        self.__scores_file = Path("Database/scores.json")
        self.__scores_file.parent.mkdir(exist_ok=True)

        if self.__scores_file.exists():
            with open(self.__scores_file, "r") as f:
                self.__scores = json.load(f)
        else:
            self.__scores = []

    def save_score(self, player_name: str, player_score: int) -> None:
        player_found = False

        for s in self.__scores:
            if s['Player'] == player_name:
                player_found = True

                if player_score > s['score']:
                    s['score'] = player_score
                break

        if not player_found:
            self.__scores.append({'Player': player_name.upper(),
                                  'score': player_score})

        self.__scores.sort(key=lambda score: score['score'], reverse=True)
        self.__scores = self.__scores[:10]

        self.__scores = [{**s, 'rank': i + 1, 'first_3_chars': s['Player'][:3]}
                         for i, s in
                         enumerate(self.__scores)]

        with open(self.__scores_file, "w") as f:
            json.dump(self.__scores, f, indent=4)

    @property
    def get_scores(self) -> List:
        return self.__scores
