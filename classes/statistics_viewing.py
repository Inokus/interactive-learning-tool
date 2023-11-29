class StatisticsViewing:
    """
    StatisticsViewing class prints out a list of all questions, their ids, status, with current
    users statistics next to them.
    """

    def __init__(self, file_handler):
        self.file_handler = file_handler

    def view_statistics(self):
        statistics = self.file_handler.get_statistics()
        print()
        if not statistics:
            print("There's currently no questions added\n")
        for entry in statistics:
            print(
                f'id: {entry["id"]}, '
                f'status: {"active" if entry["status"] == "enabled" else "inactive"}, '
                f'question: {entry["question"]}, '
                f'times shown: {entry["times_shown"]}, '
                f'percentage of correct answers: {float(entry["percentage_of_correct_answers"]):.2f}%\n'
            )

        input('Press "enter" to go back to mode selection\n')
