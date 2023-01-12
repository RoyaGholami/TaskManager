# this program is for a small business that can help it to manage tasks assigned to each member of the team
# it is using two files for store users and tasks data, 
# admin user is the only user that can add new user and view the statistics
# all user can add new task, view all tasks, and view owned tasks


import os
import datetime

# file paths are used several time ine the code by using these constants 
# we can easily change the path in future
USER_FILE_PATH = "./user.txt"
TASKS_FILE_PATH = "./tasks.txt"

# ask user to enter their username and password and check 
# if combination of these data is valid then display the menu 
# otherwise ask user to enter their username and password agin 
login_data = {}
with open(USER_FILE_PATH, "r") as users_file:
    for user in users_file.readlines():
        username, password = user.strip("\n").split(", ")
        login_data[username.lower()] = password

while True:
    username = input("Please enter your username: ").lower()
    password = input("Please enter your password: ")

    user = login_data.get(username)

    if (user == None or login_data[username] != password):
        print("The username or password is not valid!\n")
    else:
        break

# store current user name and whether is user admin or not,
#  to use in other part of code
current_user = username
is_admin = (current_user == "admin")

# main process of the program, 
# presenting the menu to the user till user select exit option
while True:

    # clear screen before show the menu
    os.system("cls")

    # the menu is different based on user is admin or not
    if (is_admin):
        menu = input('''Select one of the following Options below:
r  - Registering a user
a  - Adding a task
va - View all tasks
vm - View my task
st - View statistics
e  - Exit
: ''').lower()
    else:
        menu = input('''Select one of the following Options below:
a  - Adding a task
va - View all tasks
vm - View my task
e  - Exit
: ''').lower()

    print()

    # add a new user, ask username, password and confirmation password
    # check the username not duplicate and password and confirmation password are match
    # finally, store these data to file
    # only admin user access to this option
    if menu == 'r' and is_admin:
        while True:
            username = input("Please enter new username: ").lower()
            user = login_data.get(username)
            
            if (user == None):
                break
            else:
                print("The username is duplicate!\n")

        while True:
            password = input("Please enter new password: ")
            check_password = input("Please enter password again: ")
            
            if (password != check_password):
                print("The passwords are not match!\n")
            else:
                break

        with open(USER_FILE_PATH, "a") as users_file:
            users_file.writelines(f"{username}, {password}\n")

        # add new user to login_data dictionary to keep it update
        login_data[username.lower()] = password

        print("Adding a new user was successful")
        input("Press Enter to back to Main Menu...")

    # add a new task, ask title, username, description and due date
    # check the username exist, title not empty and due date is valid 
    # finally, store these data to file 
    elif menu == 'a':
        while True:
            task_title = input("Please enter title of task: ")
            
            if (task_title.strip() == ""):
                print("Task title can\'t be empty!\n")
            else:
                break

        while True:
            username = input("Enter the username to assign the task: ").lower()
            user = login_data.get(username)
            
            if (user == None):
                print("The username is invalid!\n")
            else:
                break

        task_description = input("Enter description of the task: ")

        while True:
            due_date = input("Enter due date of the task:[DD-MM-YYYY] ")

            # try to parse input string as a date by specific format, 
            # if it not successful exception occur and ask to input date agin 
            try:
                due_date = datetime.datetime.strptime(due_date, "%d-%m-%Y")
                break
            except ValueError:
                print("Date format is invalid!\n")

        today = datetime.date.today()

        # convert date variables to sting by specific format
        today_str = today.strftime("%d %b %Y")
        due_date_str = due_date.strftime("%d %b %Y")

        with open(TASKS_FILE_PATH, "a") as tasks_file:
            tasks_file.writelines(f"{username}, {task_title}, {task_description}, {today_str}, {due_date_str}, No\n")
        
        print("Adding a new task was successful")
        input("Press Enter to back to Main Menu...")

    # view all tasks, read all tasks from file and display them in user friendly manner 
    elif menu == 'va':
        with open(TASKS_FILE_PATH, "r") as task_file:
            tasks = task_file.readlines()

        # check is there any task in the file
        if (len(tasks) == 0):
            print("No task found!")

        for index, task in enumerate(tasks, 1):
            username, task_title, task_description, today_str, due_date_str, is_completed = task.strip("\n").split(", ")
            print(f"_____________________________________ Task {index} _______________________________________\n")
            print(f"Task:\t\t\t{task_title}")
            print(f"Assigned to:\t\t{username}")
            print(f"Date assigned:\t\t{today_str}")
            print(f"Due date:\t\t{due_date_str}")
            print(f"Task completed:\t\t{is_completed}")
            print(f"Task description:\n    {task_description}")

        print("___________________________________________________________________________________\n")
        input("Press Enter to back to Main Menu...")

    # view user's tasks, read tasks assigned to the current user from file and display them in user friendly manner 
    elif menu == 'vm':
        with open(TASKS_FILE_PATH, "r") as task_file:
            tasks = task_file.readlines()

        index = 0
        is_any_task_found = False

        for task in tasks:
            username, task_title, task_description, today_str, due_date_str, is_completed = task.strip("\n").split(", ")

            if (username.lower() != current_user):
                continue
            
            index +=1
            is_any_task_found = True
            print(f"_____________________________________ Task {index} _______________________________________\n")
            print(f"Task:\t\t\t{task_title}")
            print(f"Assigned to:\t\t{username}")
            print(f"Date assigned:\t\t{today_str}")
            print(f"Due date:\t\t{due_date_str}")
            print(f"Task completed:\t\t{is_completed}")
            print(f"Task description:\n    {task_description}")

        # check is there any task assigned to the current user
        if (not is_any_task_found):
            print("No task found!")

        print("___________________________________________________________________________________\n")
        input("Press Enter to back to Main Menu...")

    # display statistics, show user count and completed task count, not completed task count, and total task count
    # only admin user access to this option
    elif menu == 'st' and is_admin:
        user_count = len(login_data)
        not_completed_count = 0

        with open(TASKS_FILE_PATH, "r") as task_file:
            tasks = task_file.readlines()

        total_count = len(tasks)

        for task in tasks:
            username, task_title, task_description, today_str, due_date_str, is_completed = task.strip("\n").split(", ")

        if (is_completed.lower() == "no"):
            not_completed_count += 1

        completed_count = total_count - not_completed_count
        print("___________________________________________________________________________________\n")
        print(f"User count:\t\t {user_count}")
        print(f"Total tasks:\t\t {total_count}")
        print(f"Completed tasks:\t {completed_count}")
        print(f"Not completed tasks:\t {not_completed_count}")
        print("___________________________________________________________________________________\n")

        input("Press Enter to back to Main Menu...")

    # exit the program
    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    # otherwise show an error message
    else:
        print("You have made a wrong choice, Please Try again")
        input("Press Enter to back to Main Menu...")
