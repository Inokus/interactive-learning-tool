import random
from utils.utils import get_user_input


class Assessment:
    """
    Used as parent for both Practice and Test classes, since both of them share a few methods. 
    Both Practice and Testmodes are only available to user if there's at least 5 questions added 
    and at least 3 of them are enabled.
    """

    def __init__(self, file_handler):
        self.file_handler = file_handler

    def ask_question(self, question):
        print(f"\nQuestion: {question['question']}")
        if question["type"] == "quiz":
            # Get shuffled options list
            options = question["options"].split("|")
            random.shuffle(options)
            options_letters = []
            counter = 97
            print()
            # For each option print out a letter starting at a
            for option in options:
                letter = chr(counter)
                options_letters.append(letter)
                print(f"{letter}) {option}")
                counter += 1
            print(
                "\nSelect a correct option by either entering letter of an answer or answer itself"
            )
            return options, options_letters
        return [], []

    def required_length(self, length):
        if length < 3:
            input(
                f'Currently active questions: {length}, you need to enable at least 3 questions.\n\nPress "enter" to go back to mode selection\n'
            )
            return False
        return True

    def convert_letter_to_answer(self, options, options_letters, user_input):
        if user_input.strip().lower() in options_letters:
            return options[(ord(user_input.strip().lower()) - 97)]
        return user_input

    def evaluate_answer(self, mode, question, user_input):
        if user_input == question["answer"]:
            self.file_handler.update_user_stats(mode, question["id"], True)
            print("Correct!")
            return True

        self.file_handler.update_user_stats(mode, question["id"], False)
        print("Incorrect!")
        return False


class Practice(Assessment):
    """
    Gets all currently enabled questions and keeps asking user questions until they decide to quit. 
    Weights are used to make sure that questions that user answers correctly appear less often and 
    questions that user answers incorrectly appears more often.
    """

    def start_practice(self):
        questions = self.file_handler.get_enabled_questions()
        length = len(questions)
        if not self.required_length(length):
            return

        while True:
            weights = self.file_handler.get_weights(questions)
            question = random.choices(questions, weights)[0]
            options, options_letters = self.ask_question(question)
            print('\n"q" or "quit" to go back to mode selection')
            user_input = get_user_input("\nAnswer: ")

            # Allow user to quit at anytime
            if user_input in ["q", "quit"]:
                break

            if options:
                user_input = self.convert_letter_to_answer(
                    options, options_letters, user_input
                )

            self.evaluate_answer("practice", question, user_input)


class Test(Assessment):
    """
    Similar to Practice, except it asks user for positive integer that doesn't exceed currently enabled 
    questions.User is givenentered amount of questions that are chosen from enabled questions pool randomly. 
    Weights do no influence this mode. At theend user is informed on how many out of how many questions were 
    answered correctly and this data is stored in separate file with a timestamp.
    """

    def start_test(self):
        questions = self.file_handler.get_enabled_questions()
        length = len(questions)
        if not self.required_length(length):
            return

        print(f"\nCurrent number of active questions: {length}")
        while True:
            user_input = get_user_input(
                '\n"q" or "quit" to go back to mode selection\n\nEnter a number of questions that you would like to be on this test: ',
                "sl",
            )

            if user_input in ["q", "quit"]:
                break

            try:
                number = int(user_input)
                if number <= 0:
                    print("It must be a positive number")
                    continue
                if number > length:
                    print("Number must not exceed current number of active questions")
                    continue

                break
            except ValueError:
                print(
                    "It must be a positive number that doesn't exceed current number of active questions"
                )

        score = 0
        selected_questions = random.sample(questions, number)

        for question in selected_questions:
            options, options_letters = self.ask_question(question)

            user_input = get_user_input("\nAnswer: ")

            if options:
                user_input = self.convert_letter_to_answer(
                    options, options_letters, user_input
                )

            if self.evaluate_answer("test", question, user_input):
                score += 1

        self.file_handler.update_user_results(f"{score}/{number}")
        input(
            f'\nYou have answered {score} out of {number} questions correctly.\n\nPress "enter" to go back to mode selection\n'
        )
