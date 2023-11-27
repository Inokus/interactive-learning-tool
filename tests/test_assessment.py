from unittest.mock import patch
from classes.assessment import Assessment


class MockFileHandler:
    def get_enabled_questions(self):
        return [
            {
                "id": 1,
                "question": "Question 1",
                "type": "quiz",
                "options": "A|B|C",
                "answer": "A",
            },
            {
                "id": 2,
                "question": "Question 2",
                "type": "quiz",
                "options": "A|B|C",
                "answer": "B",
            },
            {
                "id": 3,
                "question": "Question 3",
                "type": "quiz",
                "options": "A|B|C",
                "answer": "C",
            },
        ]

    def update_user_stats(self, mode, question_id, result):
        pass


assessment = Assessment(MockFileHandler())


def test_assessment_required_length():
    with patch("builtins.input", side_effect=["\n"]):
        assert assessment.required_length(0) == False

    assert assessment.required_length(3) == True
    assert assessment.required_length(5) == True


def test_assessment_convert_letter_to_answer():
    options = ["Option A", "Option B", "Option C"]
    options_letters = ["a", "b", "c"]

    assert (
        assessment.convert_letter_to_answer(options, options_letters, "a") == "Option A"
    )
    assert (
        assessment.convert_letter_to_answer(options, options_letters, "B ")
        == "Option B"
    )
    assert (
        assessment.convert_letter_to_answer(options, options_letters, " c ")
        == "Option C"
    )

    assert assessment.convert_letter_to_answer(options, options_letters, "x") == "x"
    assert assessment.convert_letter_to_answer(options, options_letters, "") == ""
    assert assessment.convert_letter_to_answer(options, options_letters, "123") == "123"


def test_assessment_evaluate_answer():
    questions = assessment.file_handler.get_enabled_questions()

    assert assessment.evaluate_answer("practice", questions[0], "A") == True
    assert assessment.evaluate_answer("practice", questions[1], "C") == False
    assert assessment.evaluate_answer("test", questions[2], "C") == True
