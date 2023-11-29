from classes.assessment import Practice, Test
from classes.file_handler import FileHandler
from classes.question_handler import AddingQuestions, DisableEnableQuestions
from classes.statistics_viewing import StatisticsViewing
from utils.utils import get_valid_name, change_text_color


def print_menu(condition):
    # If condition is not met print practice and test in gray color
    practice = change_text_color("4 Practice") if not condition else "4 Practice"
    test = change_text_color("5 Test") if not condition else "5 Test"

    print(
        "\n1 Add questions\n"
        "--------------------------------------------\n"
        "2 View statistics\n"
        "--------------------------------------------\n"
        "3 Disable/Enable questions\n"
        "--------------------------------------------\n"
        f"{practice}\n"
        "--------------------------------------------\n"
        f"{test}\n"
        "--------------------------------------------\n"
        "6 Change profile\n"
        "--------------------------------------------\n"
        "7 Exit\n"
    )


def main():
    while True:
        name = get_valid_name()

        # Create file handler for current user and ensure that all files/folders are set up
        file_handler = FileHandler(name)
        if not file_handler.paths_exists():
            file_handler.create_paths()
        # Ensure that in case some other user added questions they're also added to current user stats
        file_handler.write_user_stats()

        # Make sure that at least 5 questions are added before enabling practice and test modes
        enable_practice_and_test = False
        questions_count = file_handler.get_length(file_handler.questions_file_name)
        if questions_count >= 5:
            enable_practice_and_test = True

        print_menu(enable_practice_and_test)
        while True:
            mode = input("Type [1-7] to select: ")
            match mode:
                case "1":
                    adding_questions = AddingQuestions(file_handler)
                    adding_questions.add_questions()
                    file_handler.write_user_stats()
                    questions_count = file_handler.get_length(
                        file_handler.questions_file_name
                    )
                    if questions_count >= 5:
                        enable_practice_and_test = True
                    print_menu(enable_practice_and_test)
                case "2":
                    statistics_viewing = StatisticsViewing(file_handler)
                    statistics_viewing.view_statistics()
                    print_menu(enable_practice_and_test)
                case "3":
                    disable_enable_questions = DisableEnableQuestions(file_handler)
                    disable_enable_questions.change_status()
                    print_menu(enable_practice_and_test)
                case "4":
                    if enable_practice_and_test:
                        practice = Practice(file_handler)
                        practice.start_practice()
                        print_menu(enable_practice_and_test)
                    else:
                        print(
                            f"This mode is currently disabled, add {5 - questions_count} or more questions for access"
                        )
                case "5":
                    if enable_practice_and_test:
                        test = Test(file_handler)
                        test.start_test()
                        print_menu(enable_practice_and_test)
                    else:
                        print(
                            f"This mode is currently disabled, add {5 - questions_count} or more questions for access"
                        )
                case "6":
                    print()
                    break
                case "7":
                    return
                case _:
                    print("Invalid input")


if __name__ == "__main__":
    main()
