# Task Manager

# =====importing libraries===========
import datetime
import os


def login_password(user_name, password):
    """
    Function will validate if username and password exsits in textfile
    """
    # Read a file
    with open("user.txt", "r", encoding="utf-8") as user_in_file:
        for line in user_in_file:
            # Split the line by comma in to two parts
            parts = line.strip().split(", ")
            if len(parts) == 2:
                stored_user_name, stored_password = parts
                if user_name == stored_user_name and password == stored_password:
                    return True  # Both username and password match in textfile
    return False  # User not found


def new_user():
    """
    Function will add new users and check if passwords match
    """
    while True:
        new_name = input("Please enter a new username: ").strip()
        if new_name == "":
            print("Please do not leave empty fields!")
            continue

        new_password = input("Please enter a new password: ").strip()
        confirm_password = input("Re-Enter your password: ").strip()

        if new_password != confirm_password:
            print("Password miss-match please try again!")
        elif new_password == "" and confirm_password == "":
            print("Please do not leave empty fields!")
        else:
            with open("user.txt", "a", encoding="utf-8") as user_out_file:
                user_out_file.write(f"{new_name}, {new_password}\n")
            print("New user has been added")
            break


def task_adder():
    """
    Function to add a new task into textfile
    """
    while True:
        print("Enter the following information: ")
        task_user = input("Task user: ").strip()
        task_title = input("Task title: ").strip()
        task_description = input("Task description: ").strip()
        task_due_date = input("Due date(Eg.27 Nov 2024): ").strip()

        if not task_user or not task_title or not task_description or not task_due_date:
            print("One of the fields are invalid please try again.")
            continue
        # Validate due date
        try:
            due_date = datetime.datetime.strptime(task_due_date, '%d %b %Y')
            if due_date < datetime.datetime.now():
                print("Date due cannot be in the past!")
                continue
        except ValueError:
            print("Incorrect format please try (dd mm yyyy)")
            continue
        # Date assigned gets todays date
        # Got help from
        # https://www.programiz.com/python-programming/datetime/current-datetime
        task_assigned = datetime.datetime.now().strftime('%d %b %Y')
        task_complete = "No"
        full_task = f"{task_user}, {task_title}, {task_description}, {task_due_date}, {task_assigned}, {task_complete}"

        with open("tasks.txt", "a", encoding="utf-8") as task_out_file:
            task_out_file.write(f"{full_task}\n")
        print('Task has been added')
        break


def view_all_tasks():
    """
    View all tasks
    """
    with open("tasks.txt", "r", encoding="utf-8") as task_in_file:
        for line in task_in_file:
            # Breaks the line into 6 different parts at the comma
            parts = line.strip().split(", ")
            print(f"\n{'*' * 30}\nTitle: {parts[1]}\n{'-' * 30}")
            print(f"Assigned to: {parts[0]}\nDescription: {parts[2]}")
            print(f"Assigned Date: {parts[3]} \nDue Date: {parts[4]}")
            print(f"Completed: {parts[5]}\n{'-' * 30}")


def view_personal_tasks(username):
    """
    View user specific tasks
    """
    # same code used in view all tasks function with added if statement
    with open("tasks.txt", "r", encoding="utf-8") as task_in_file:
        for line in task_in_file:
            parts = line.strip().split(", ")
            if parts[0].lower() == username.lower():
                print(f"\n{'*' * 30}\nTitle: {parts[1]}\n{'-' * 30}")
                print(f"Assigned to: {parts[0]}\nDescription: {parts[2]}")
                print(f"Assigned Date:{parts[3]} \nDue Date: {parts[4]}")
                print(f"Completed: {parts[5]}\n{'-' * 30}")


def user_stats():
    """
    Display users statistics
    """
    with open("user.txt", "r", encoding="utf-8") as user_in_file:
        users = user_in_file.readlines()
    with open("tasks.txt", "r", encoding="utf-8") as task_in_file:
        tasks = task_in_file.readlines()

    print(f"Total users: {len(users)}")
    print(f"Total tasks: {len(tasks)}")


def main():
    """
    Will run all the code
    """
    # Checks if files exsist in order to use them
    if not os.path.exists("user.txt"):
        # utf-8 encoding is used to avoid errors and boost compatability
        # Learnt about it here:https://blog.hubspot.com/website/what-is-utf-8
        with open("user.txt", "w", encoding="utf-8") as f:
            f.write("admin, admin")
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w", encoding="utf-8") as f:
            pass

    # Loop for errors in the login
    while True:
        username = input("Please enter your username: ").strip()
        password = input("Please enter your password: ").strip()
        if login_password(username, password):
            print("Succesful Login")
            break
        else:
            print("Invalid username or password!Please try again")

    while True:
        # Present the menu to the user and
        # make sure that the user input is converted to lower case.
        if username == "admin":
            menu = input('''Select one of the following options:
        r - register a user
        a - add task
        va - view all tasks
        vm - view my tasks
        s - statistics
        e - exit
        : ''').lower()
        else:
            menu = input('''Select one of the following options:
        a - add task
        va - view all tasks
        vm - view my tasks
        e - exit
        : ''').lower()

        if menu == 'r' and username == "admin":
            new_user()
        elif menu == 'a':
            task_adder()
        elif menu == 'va':
            view_all_tasks()
        elif menu == 'vm':
            view_personal_tasks(username)
        elif menu == "s" and username == "admin":
            user_stats()
        elif menu == 'e':
            print('Goodbye have an amazing day!!!')
            exit()
        else:
            print("You have entered an invalid input. Please try again")


if __name__ == "__main__":
    main()
