import csv
from datetime import datetime
import os


class FileHandler:
    """
    Responsible for everything reading and writing related.
    """

    def __init__(self, name):
        self.questions_file_name = "questions.csv"
        self.user_stats_name = f"{name}_stats.csv"
        self.user_results_name = f"{name}_results.txt"
        self.user_folder_name = "user_data"
        self.user_stats_path = os.path.join(self.user_folder_name, self.user_stats_name)
        self.user_results_path = os.path.join(
            self.user_folder_name, self.user_results_name
        )
        self.questions_fieldnames = [
            "id",
            "type",
            "question",
            "answer",
            "options",
            "status",
        ]
        self.user_stats_fieldnames = [
            "id",
            "times shown",
            "times answered correctly",
            "percentage of correct answers",
            "weight",
        ]

    # Reading related functions

    def paths_exists(self):
        if (
            not os.path.exists(self.user_stats_path)
            or not os.path.exists(self.user_results_path)
            or not os.path.exists(self.questions_file_name)
        ):
            return False

        return True

    def read(self, path):
        with open(path, "r") as file:
            reader = csv.DictReader(file)
            return list(reader)

    def read_line(self, path, question_id):
        rows = self.read(path)
        for row in rows:
            if row["id"] == question_id:
                return row

    def get_last_id(self, path):
        rows = self.read(path)
        if not rows:
            return 0
        return int(rows[-1]["id"])

    def get_length(self, path):
        rows = self.read(path)
        return len(rows)

    def get_statistics(self):
        questions = self.read(self.questions_file_name)
        stats = self.read(self.user_stats_path)
        statistics = []

        for i, question in enumerate(questions):
            statistics.append(
                {
                    "id": question["id"],
                    "status": question["status"],
                    "question": question["question"],
                    "times shown": stats[i]["times shown"],
                    "percentage of correct answers": stats[i][
                        "percentage of correct answers"
                    ],
                }
            )

        return statistics

    def get_enabled_questions(self):
        questions = self.read(self.questions_file_name)
        enabled_questions = []

        for question in questions:
            if question["status"] == "enabled":
                enabled_questions.append(question)

        return enabled_questions

    def get_weights(self, questions):
        stats = self.read(self.user_stats_path)
        ids = [question["id"] for question in questions]
        weights = [int(entry["weight"]) for entry in stats if entry["id"] in ids]
        return weights

    # Writing related functions

    def create_paths(self):
        if not os.path.exists(self.user_folder_name):
            os.makedirs(self.user_folder_name)
        if not os.path.exists(self.user_stats_path):
            with open(self.user_stats_path, "w") as file:
                writer = csv.DictWriter(file, fieldnames=self.user_stats_fieldnames)
                writer.writeheader()
        if not os.path.exists(self.user_results_path):
            with open(self.user_results_path, "w") as file:
                pass
        if not os.path.exists(self.questions_file_name):
            with open(self.questions_file_name, "w") as file:
                writer = csv.DictWriter(file, fieldnames=self.questions_fieldnames)
                writer.writeheader()

    def write_questions(self, rows):
        last_id = self.get_last_id(self.questions_file_name)

        with open(self.questions_file_name, "a") as file:
            writer = csv.DictWriter(file, fieldnames=self.questions_fieldnames)
            counter = 1
            for row in rows:
                writer.writerow(
                    {
                        "id": last_id + counter,
                        "type": row.type,
                        "question": row.question,
                        "answer": row.answer,
                        "options": "|".join(row.options),
                        "status": "enabled",
                    }
                )
                counter += 1

    def write_user_stats(self):
        questions = self.read(self.questions_file_name)
        user_stats = self.read(self.user_stats_path)

        with open(self.user_stats_path, "a") as file:
            writer = csv.DictWriter(file, self.user_stats_fieldnames)
            if not user_stats:
                # Write all questions with default values
                for question in questions:
                    writer.writerow(
                        {
                            "id": question["id"],
                            "times shown": 0,
                            "times answered correctly": 0,
                            "percentage of correct answers": 0,
                            "weight": 10,
                        }
                    )
            else:
                # Write only questions starting at last entry id + 1
                last_id = int(user_stats[-1]["id"])
                if last_id < len(questions):
                    for question in questions:
                        if int(question["id"]) > last_id:
                            writer.writerow(
                                {
                                    "id": question["id"],
                                    "times shown": 0,
                                    "times answered correctly": 0,
                                    "percentage of correct answers": 0,
                                    "weight": 10,
                                }
                            )

    def update_status(self, question_id):
        rows = self.read(self.questions_file_name)

        for row in rows:
            if row["id"] == question_id:
                if row["status"] == "enabled":
                    row["status"] = "disabled"
                else:
                    row["status"] = "enabled"
                break

        with open(self.questions_file_name, "w") as file:
            writer = csv.DictWriter(file, fieldnames=self.questions_fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def update_user_stats(self, mode, question_id, correct):
        rows = self.read(self.user_stats_path)

        for row in rows:
            if row["id"] == question_id:
                row["times shown"] = int(row["times shown"]) + 1
                if correct:
                    row["times answered correctly"] = (
                        int(row["times answered correctly"]) + 1
                    )

                if mode == "practice":
                    # Current weight range 1-20, increments of 1, but can be adjusted anytime
                    weight = int(row["weight"])
                    if correct:
                        if weight > 1:
                            row["weight"] = weight - 1
                    else:
                        if weight < 20:
                            row["weight"] = weight + 1

                row["percentage of correct answers"] = (
                    int(row["times answered correctly"]) / row["times shown"]
                ) * 100
                break

        with open(self.user_stats_path, "w") as file:
            writer = csv.DictWriter(file, fieldnames=self.user_stats_fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def update_user_results(self, score):
        now = datetime.now()
        with open(self.user_results_path, "a") as file:
            file.write(f'{score} {now.strftime("%Y/%m/%d %H:%M:%S")}\n')
