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
        for entry in statistics:
            print(
                f'id: {entry["id"]}, '
                f'status: {"active" if entry["status"] == "enabled" else "inactive"}, '
                f'question: {entry["question"]}, '
                f'times shown: {entry["times shown"]}, '
                f'percentage of correct answers: {float(entry["percentage of correct answers"]):.2f}%\n'
            )

        input('Press "enter" to go back to mode selection\n')
