def valid_name(name):
    length = len(name)

    if length < 3:
        print("Name has to be at least 3 characters long")
        return False

    if not name[0].isalnum() or not name[-1].isalnum():
        print("A name has to start and end with letter or number")
        return False

    for i in range(1, length - 2):
        if not name[i].isalnum() and name[i] != "_":
            print("A name can consist only of letters, numbers and underscores")
            return False
        if name[i] == "_" and name[i + 1] == "_":
            print("Two or more underscores in a row are not allowed")
            return False

    return True


def get_user_input(prompt, options=""):
    user_input = input(prompt)
    while not user_input:
        user_input = input(f"Input can't be empty\n{prompt}")

    if options == "sl":
        return user_input.strip().lower()

    return user_input
