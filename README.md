# interactive-learning-tool

This tool allows users to add questions and answers, manage added questions status and practice answering them.
There's a feature for multiple profiles, statistics are tracked separately, but question pool is shared between users.

Once program starts there's multiple options to choose from:

1. Add questions
   - allows to add quiz or free-form questions, later on you can answer quiz questions by entering letter of an answer or
     answer itself, free-form questions requires full typed out answers. Answer checking is case-sensitive
2. View statistics
   - shows currently selected users statistics for each question (e.g., id: 3, status: active, question: Example question?, times shown: 4, percentage of correct answers: 75.00%)
3. Disable/Enable questions
   - allows to change question status by entering it's id
4. Practice
   - questions are given non-stop so that user can practice. Questions that are answered correctly become less likely to appear,
     while questions that are answered incorrectly become more likely to appear
5. Test
   - let's you select a number of questions for the test, questions are chosen randomly and are unique (won't appear twice in the
     same test). At the end of test user is informed on how many questions was answered correctly, this data is saved in user_data/username_results.txt
     file with timestamp
6. Change profile
   - allows user to change currently active username, usernames are case-insensitive, so "JOHN" would use same data files as "john"
7. Exit

Practice and test modes will appear grayed out until there's at least 5 questions added. After that user is allowed to enter these
modes, but won't be able to start practice or test unless there's at least 3 questions currently active (enabled)
