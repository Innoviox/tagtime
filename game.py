import random
from questions import *


class Game:
    def __init__(self, db, start_location, start_time, run_time):
        self.db = db
        self.start_location = start_location
        self.start_time = start_time
        self.run_time = run_time

        self.current_paths = []
        self.current_hider_spot = None
        self.current_seeker_spot = None

    def play(self):
        self.current_paths = self.db.search(
            self.start_location, self.start_time, self.run_time
        )
        # self.current_hider_spot = random.choice(self.current_paths[1:]).last_station()
        self.current_hider_spot = self.current_paths[-1].last_station()

        self.current_seeker_spot = self.start_location
        self.total_time = 0

        print(f"Hider at {self.db.name_for_station_id(self.current_hider_spot)}")

        while True:
            best_question = None
            best_score = None  # todo: bits
            for question in self.db.make_all_questions(
                self.current_seeker_spot, self.start_time + self.total_time
            ):
                total = self.db.rate_question(question, self.current_paths)
                print(f"{question}: {total}/{len(self.current_paths)}")
                score = abs(
                    total - len(self.current_paths) / 2
                )  #  * (question.time + 1)
                if not best_score or score < best_score:
                    best_score = score
                    best_question = question

            print(
                f"At {self.total_time}: Seeker at {self.db.name_for_station_id(self.current_seeker_spot)}"
            )
            print(f"Best question: {best_question}, score: {best_score}")
            answer = best_question.query(self.current_hider_spot)
            self.total_time += best_question.time
            print(f"Answer: {answer}")
            self.current_paths = [
                path
                for path in self.current_paths
                if answer == best_question.query(path.last_station())
            ]
            if len(self.current_paths) == 1:
                print(f"Found hider at {self.current_paths[0].last_station()}")
                break
            print(f"Possibilities left: {len(self.current_paths)}")
            for path in self.current_paths:
                print(f"\t{self.db.name_for_station_id(path.last_station())}")
            if isinstance(best_question, ThermometerQuestion):
                self.current_seeker_spot = best_question.end.stop_id
            input()
