from utils.utils import get_user_input


class AddingQuestions:
    """
    AddingQuestions class is designed to prompt user to add questions and store them in memory, then
    once user is done write those questions into designated file. These questions are supposed to be
    shared among different users.
    """

    def __init__(self, file_handler):
        self.file_handler = file_handler
        self.questions = []

    def add_questions(self):
        while True:
            question_type = get_user_input(
                '\n"q" or "quiz" to add quiz type question\n"f" or "free" to add free-form question\n"!q" or "quit" to save and go back to mode selection\n\nChoose a question type that you would like to add: ',
                "sl",
            )
            if question_type in ["q", "quiz"]:
                self.add_question("quiz")
            elif question_type in ["f", "free"]:
                self.add_question("free")
            elif question_type in ["!q", "quit"]:
                # Before going back to mode selection check if any questions were added and save them in file
                if self.questions:
                    self.file_handler.write_questions(self.questions)
                    self.questions = []

                break

            else:
                print("Invalid input")

    def add_question(self, question_type):
        if question_type == "free":
            question = FreeQuestion()
        else:
            question = QuizQuestion()

        question.set_attributes()
        self.questions.append(question)


class FreeQuestion:
    """
    FreeQuestion class creates an object that holds question data, QuizQuestion expands on it by 
    adding options attribute.
    """

    def __init__(self):
        self.type = "free"
        self.question = ""
        self.answer = ""
        self.options = ""

    def set_attributes(self):
        self.question = get_user_input("\nQuestion: ")
        self.answer = get_user_input("\nCorrect answer: ")


class QuizQuestion(FreeQuestion):
    def __init__(self):
        super().__init__()
        self.type = "quiz"

    def set_attributes(self):
        super().set_attributes()
        self.options = [self.answer]
        counter = 1
        print('\nEnter at least one other answer option, when you\'re done type "done"')
        while True:
            option = get_user_input(f"\nOption {counter}: ")
            if option == "done":
                if len(self.options) > 1:
                    break
                print("Add at least one other option")
            elif option in self.options:
                print("This option already exists")
            else:
                self.options.append(option)
                counter += 1


class DisableEnableQuestions:
    """
    DisableEnableQuestions class informs user on how many questions there are currently stored and 
    asksfor question id as an input. Upon entering the id corresponding question is printed out and 
    user isasked for confirmation, if user complies question status is changed. These changes are 
    shared between users.
    """

    def __init__(self, file_handler):
        self.file_handler = file_handler

    def change_status(self):
        length = self.file_handler.get_length(self.file_handler.questions_file_name)
        print(
            f"\nDisable or enable a question by entering its id, current number of questions: {length}"
        )
        while True:
            question_id = get_user_input(
                '\n"id" number to change question status\n"q" or "quit" to go back to mode selection\n\nChoose id of a question that you would like to disable or enable: ',
                "sl",
            )
            try:
                if question_id in ["q", "quit"]:
                    break
                if int(question_id) < 1 or int(question_id) > length:
                    print("Invalid id")
                else:
                    line = self.file_handler.read_line(
                        self.file_handler.questions_file_name, question_id
                    )
                    print(
                        f'\nid: {line["id"]}, type: {line["type"]}, question: {line["question"]}, answer: {line["answer"]}, status: {line["status"]}'
                    )
                    while True:
                        response = get_user_input(
                            '\nAre you sure you want to change the status of this question?\n\n"y" or "yes" to confirm\n"n" or "no" to cancel\n\nConfirmation: ',
                            "sl",
                        )
                        if response in ["y", "yes"]:
                            self.file_handler.update_status(question_id)
                            break
                        if response in ["n", "no"]:
                            break

                        print("Invalid input")
                        continue

            except ValueError:
                print(
                    "id must be a positive number that doesn't exceed current number of questions"
                )
