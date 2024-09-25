import tkinter as tk
from functools import partial
import json
import string


db = "database.json"
#creates the main window where the tasks are listed
#contains inner functions for the main task window
def taskscreen(window, User):
    #writes changes into the JSON file, rereads the file and calls the new information into the main window
    def save_refresh(data_dict):
        #write into the dictionary
        json_dict = json.dumps(data_dict)
        file = open(db, "w")
        file.write(json_dict)
        file.close

        #reopen the JSON file and load the updated dictionary
        file = open(db, "r")
        x = file.readline()
        data_dict = json.loads(x)
        file.close

        #iterates through all the users and matches the current user to the updated list
        #Then, recall for the main window function    
        for the_user in data_dict["users"]:
            if User['username'] == the_user['username']:
                taskscreen(window, the_user)

    #reopens the main task window and closes the current window
    def cancel(currentwin):
        win1.deiconify()
        currentwin.withdraw()

    #edits or adds a task into the JSON file for the current user
    def newtask(win2, title, descr, deadline, status, priority, action):
        #opens and reads the JSON file dictionary
        file = open(db, "r")
        x = file.readline()
        data_dict = json.loads(x)
        file.close

        user_index = 0
        for Users in data_dict["users"]: #checks every user in the JSON
            if User["username"] == Users["username"]: #checks if the username matches
                if action == "new":
                    task = {"title": title.get(), "description": descr.get(), "deadline": deadline.get(), "status": status.get(), "priority": priority.get()}
                    data_dict["users"][user_index]["tasks"].append(task) #adds the new task to the list of tasks
                elif action == "edit":
                    task = {"title": title.get(), "description": descr.get(), "deadline": deadline.get(), "status": status.get(), "priority": priority.get()}
                    data_dict["users"][user_index]["tasks"][select.get()] = task #overewrites a task with edited data
            else:
                user_index += 1

        save_refresh(data_dict)
        win2.withdraw()

    #opens a window prompting the user to enter a new task
    def newtaskwin():
        #initialize window
        win1.withdraw()
        win2 = tk.Toplevel(window)
        win2.geometry('250x175')
        win2.title("New Task")

        #creates labels and text boxes for each component of the task
        task = tk.Label(win2, text="Task:")
        task.grid(column=0, row=0, ipadx=15)
        task_entry = tk.Entry(win2)
        task_entry.grid(column=1, row=0,)

        descr = tk.Label(win2, text="Description:")
        descr.grid(column=0, row=1, ipadx=15)
        descr_entry = tk.Entry(win2)
        descr_entry.grid(column=1, row=1)

        deadline = tk.Label(win2, text="deadline:")
        deadline.grid(column=0, row=2, ipadx=15)
        deadline_entry = tk.Entry(win2)
        deadline_entry.grid(column=1, row=2)

        status = tk.Label(win2, text="Status:")
        status.grid(column=0, row=3, ipadx=15)
        status_entry = tk.Entry(win2)
        status_entry.grid(column=1, row=3)

        priorityoptions = ["Urgent", "High", "Medium", "Low"] #options for priority
        prioritytype = tk.StringVar(win2) #initialize variable for priority type
        prioritytype.set(priorityoptions[2]) #set default priority type to "Medium"
        priority = tk.Label(win2, text="Priority:")
        priority.grid(column=0, row=4, ipadx=15)
        priority_entry = tk.OptionMenu(win2, prioritytype, *priorityoptions) #implement drop down menu
        priority_entry.configure(width=14)
        priority_entry.grid(column=1, row=4)

        #button to submit task values to write into JSON
        tasksubmit = tk.Button(win2, text="Submit", command=partial(newtask, win2, task_entry, descr_entry, deadline_entry, status_entry, prioritytype, "new"))
        tasksubmit.grid(column=1, row=5)

        #button to cancel creating a new task
        canceladd = tk.Button(win2, text="Cancel", command=partial(cancel, win2))
        canceladd.grid(column=0, row=5)

    #deletes selected task via radio button
    def delete():
        win1.withdraw() #closes main window
        #opens JSON
        file = open(db, "r")
        x = file.readline()
        data_dict = json.loads(x)
        file.close

        user_index = 0
        for Users in data_dict["users"]: #iterates through each user in JSON
            if User["username"] == Users["username"]: #check if current user matches the iteration
                del data_dict["users"][user_index]["tasks"][select.get()] #delete selected task
            else: 
                user_index += 1

        save_refresh(data_dict) #writes and reopens the JSON

    #edit the values of the selected task
    def edit():
        win1.withdraw() #closes main window
        #opens JSON
        file = open(db, "r")
        x = file.readline()
        data_dict = json.loads(x)
        file.close
        #initialize window
        win3 = tk.Toplevel(window)
        win3.geometry('250x175')
        win3.title("Edit Task")

        user_index = 0
        for Users in data_dict["users"]: #iterate through users in JSON
            if User["username"] == Users["username"]: #check if the username matches the iteration
                current_task = data_dict["users"][user_index]["tasks"][select.get()] #gets the selected task
                break
            else:
                user_index += 1

        #creates labels and text boxes for each component of the task
        task = tk.Label(win3, text="Task:")
        task.grid(column=0, row=0, ipadx=15)
        task_entry = tk.Entry(win3)
        task_entry.insert(0, current_task["title"]) #inserts the original data into the text box
        task_entry.grid(column=1, row=0,)

        descr = tk.Label(win3, text="Description:")
        descr.grid(column=0, row=1, ipadx=15)
        descr_entry = tk.Entry(win3)
        descr_entry.insert(0, current_task["description"])
        descr_entry.grid(column=1, row=1)

        deadline = tk.Label(win3, text="deadline:")
        deadline.grid(column=0, row=2, ipadx=15)
        deadline_entry = tk.Entry(win3)
        deadline_entry.insert(0, current_task["deadline"])
        deadline_entry.grid(column=1, row=2)

        status = tk.Label(win3, text="Status:")
        status.grid(column=0, row=3, ipadx=15)
        status_entry = tk.Entry(win3)
        status_entry.insert(0, current_task["status"])
        status_entry.grid(column=1, row=3)
        
        priorityoptions = ["Urgent", "High", "Medium", "Low"] #options for priority
        priority = tk.Label(win3, text="Priority:")
        priority.grid(column=0, row=4, ipadx=15)
        prioritytype = tk.StringVar(win3) #initialize priority variable
        prioritytype.set(current_task["priority"])
        priority_entry = tk.OptionMenu(win3, prioritytype, *priorityoptions) #drop down menu
        priority_entry.configure(width=12)
        priority_entry.grid(column=1, row=4, ipadx=20)

        #button to submit the edited task values to the JSON
        tasksubmit = tk.Button(win3, text="Submit", command=partial(newtask, win3, task_entry, descr_entry, deadline_entry, status_entry, prioritytype, "edit"))
        tasksubmit.grid(column=1, row=5)

        #button to cancel editing the task values
        canceladd = tk.Button(win3, text="Cancel", command=partial(cancel, win3))
        canceladd.grid(column=0, row=5)

    #sort the taks by priority
    def sorttasks(type):
        sortedtasks = []
        #iterates through each priority level and appends them to a list to sort
        for Task in User["tasks"]: 
            if Task["priority"] == "Urgent":
                sortedtasks.append(Task)
        for Task in User["tasks"]:
            if Task["priority"] == "High":
                sortedtasks.append(Task)
        for Task in User["tasks"]:
            if Task["priority"] == "Medium":
                sortedtasks.append(Task)
        for Task in User["tasks"]:
            if Task["priority"] == "Low":
                sortedtasks.append(Task)
        if type == "ascending": #flips the list if sorting my ascending
            sortedtasks.reverse()
        User["tasks"] = sortedtasks
        win1.withdraw()
        taskscreen(window, User) #recalls the main screen

    #return to login window
    def logout():
        win1.withdraw() #closes main window
        loginscreen() #opens login window

    #initialize main task window
    win1 = tk.Toplevel(window)
    win1.geometry('1200x800')
    win1.title("Task List")
    
    #creates headings for each component of the tasks on the main window
    taskheading = tk.Label(win1, text="Task", font=("Arial", "15"))
    taskheading.grid(column=1, row=0, ipadx=50)

    descriptionheading = tk.Label(win1, text="Description", font=("Arial", "15"))
    descriptionheading.grid(column=2, row=0, ipadx=50)

    deadlineheading = tk.Label(win1, text="Deadline", font=("Arial", "15"))
    deadlineheading.grid(column=3, row=0, ipadx=50)

    statusheading = tk.Label(win1, text="Status", font=("Arial", "15"))
    statusheading.grid(column=4, row=0, ipadx=50)

    priorityheading = tk.Label(win1, text="Priority", font=("Arial", "15"))
    priorityheading.grid(column=5, row=0, ipadx=50)

    tasknum = 0 #initialize row number
    select = tk.IntVar() #initialize a variable for the radio button
    #writes each task on the task window
    for Task in User["tasks"]: #iterates through each task
        tasknum += 1 #increases row number
        task = tk.Label(win1, text=Task["title"], font=("Arial", "10"))
        task.grid(column=1, row=tasknum, ipadx=50)

        descr = tk.Label(win1, text=Task["description"], font=("Arial", "10"))
        descr.grid(column=2, row=tasknum, ipadx=50)

        deadline = tk.Label(win1, text=Task["deadline"], font=("Arial", "10"))
        deadline.grid(column=3, row=tasknum, ipadx=50)

        status = tk.Label(win1, text=Task["status"], font=("Arial", "10"))
        status.grid(column=4, row=tasknum, ipadx=50)

        priority = tk.Label(win1, text=Task["priority"], font=("Arial", "10"))
        priority.grid(column=5, row=tasknum, ipadx=50)

        selector = tk.Radiobutton(win1, value=tasknum-1, variable=select)
        selector.grid(column=0, row=tasknum, ipadx=10, sticky="W")

    #creates the function buttons
    buttons_initializer = len(User["tasks"]) #variable to ensure the buttons will not overwrite a task
    new_task =  tk.Button(win1, text="New Task", command=newtaskwin)
    new_task.grid(column=1, row=buttons_initializer + 1)

    edit_task = tk.Button(win1, text="Edit", command=edit)
    edit_task.grid(column=2, row=buttons_initializer + 1)

    delete_task = tk.Button(win1, text="Delete", command=delete)
    delete_task.grid(column=3, row=buttons_initializer + 1)

    sort_asc = tk.Button(win1, text="Sort Priority Ascending", command=partial(sorttasks, "ascending"))
    sort_asc.grid(column=4, row=buttons_initializer + 1)

    sort_desc = tk.Button(win1, text="Sort Priority Descending", command=partial(sorttasks, "descending"))
    sort_desc.grid(column=5, row=buttons_initializer + 1)

    quit_button = tk.Button(win1, text="Exit", command=quit)
    quit_button.grid(column=6, row=0)

    logout_button = tk.Button(win1, text="Logout", command=logout)
    logout_button.grid(column=6, row=1)

#creates the loginscreen window
#contains functions for the login screen
def loginscreen():
    #checks if the username and password is correct and opens the main window
    def login():
        #open and read JSON
        file = open(db, "r")
        x = file.readline()
        data_dict = json.loads(x)
        file.close

        usercounter = 0 #variable to count how many users have been checked
        for User in data_dict["users"]:
            if username.get() == User["username"] and password.get() == User["password"]: #if the entered username and password are correct, launch main window
                window.withdraw()
                taskscreen(window, User)
                break
            else:
                usercounter += 1
        if usercounter == len(data_dict["users"]): #if all users have been checked and the username and password do not match, reveal error message
            incorrect_login_label.pack()            
    
    #closes current window and relaunches the specified screen
    def close(currentwin, close_type):
        currentwin.withdraw()
        if close_type == "okay":
            createuser()
        elif close_type == "return to login":
            loginscreen()

    #creates a window with errors
    def error_msg(error_list):
        #initialize window
        win5 = tk.Tk()
        win5.geometry('400x200')
        win5.title("New User Error")

        #iterates though the list of errors and writes them on the window
        for i in range(len(error_list)):
            error = error_list[i]
            message = tk.Label(win5, text=error)
            message.pack()

        okay = tk.Button(win5, text="Okay", command=partial(close, win5, "okay")) #button to close the error window
        okay.pack()

    #checks if entered data passes all conditions and creates the user or an error
    def create_user(win4, newusername, password1, password2, security_question, security_question_ans, security_question_options):
        win4.withdraw() #closes prev window
        #initialize new user window
        file = open(db, "r")
        x = file.readline()
        data_dict = json.loads(x)
        file.close

        error_list = [] #list containing current errors
        #conditions to add an error to error list
        for User in data_dict["users"]:
            if newusername.get() == User["username"]:
                error_list.append("The inputted username already exists.")
        if password1.get() != password2.get():
            error_list.append("The inputted passwords do not match.")
        if not len(password1.get()) >= 10:
            error_list.append("The inputted password is not at least 10 characters long.")
        if any(password1.get() in string.ascii_uppercase for _ in password1.get()) == False:
            error_list.append("The inputted password does not contain at least 1 capital letter.")
        if any(password1.get() in string.digits for _ in password1.get()) == False:
            error_list.append("The inputted password does not contain at least 1 digit.")
        if any(password1.get() in string.punctuation for _ in password1.get()) == False:
            error_list.append("The inputted password does not contain at least 1 punctuation character.")
        if security_question_ans.get() == "" or security_question.get() not in security_question_options:
            error_list.append("Please select and answer a security question.")
        if not error_list: #if not errors, create the user
            data_dict["users"].append({"username": newusername.get(), "password": password1.get(), "security question": security_question.get(), "security password": security_question_ans.get(), "tasks": []})

            #saves new user data in JSON
            json_dict = json.dumps(data_dict)
            file = open(db, "w")
            file.write(json_dict)
            file.close

            #window to confirm that the new user has been created
            win6 = tk.Tk()
            win6.geometry('150x50')
            win6.title("New User Successfully Created")

            success = tk.Label(win6, text="The new user was successfully created.")
            success.pack()
            
            okay = tk.Button(win6, text="Okay", command=partial(close, win6, "return to login")) #button to return to login
            okay.pack()

        else:
            error_msg(error_list) #opens error window

    #creates a window to create a new user
    def createuser():
        #initialize new user window
        window.withdraw()
        win4 = tk.Tk()
        win4.geometry('800x300')
        win4.title("New User")

        #creates labels and entry boxes
        newusernamelabel = tk.Label(win4, text="Username: ")
        newusernamelabel.grid(column=0, row=0)
        newusername = tk.Entry(win4)
        newusername.grid(column=1, row=0)

        pwlabel1 = tk.Label(win4, text="Password: ")
        pwlabel1.grid(column=0, row=1)
        password1 = tk.Entry(win4, show="*")
        password1.grid(column=1, row=1)
        pwlabel2 = tk.Label(win4, text="Confirm Password: ")
        pwlabel2.grid(column=0, row=2)
        password2 = tk.Entry(win4, show="*")
        password2.grid(column=1, row=2)

        spacer1 = tk.Label(win4, text="")
        spacer1.grid(column=0, row=3)

        security_question_options = ["What's your mother's maiden name?", "What is the name of your favourite high school teacher?", "What's your favourite security question?", "What's a significant date in your life? (YYYYMMDD)"]
        security_question_label = tk.Label(win4, text="Security Question:") 
        security_question_label.grid(column=0, row=4)
        security_question = tk.StringVar(win4)
        security_question.set("Select a Security Question")
        security_question_dropdown = tk.OptionMenu(win4, security_question, *security_question_options)
        security_question_dropdown.grid(column=1, row=4)
        security_question_ans_label = tk.Label(win4, text="Security Question Answer:")
        security_question_ans_label.grid(column=0, row=5)
        security_question_ans = tk.Entry(win4, show="*")
        security_question_ans.grid(column=1, row=5)

        spacer2 = tk.Label(win4, text="")
        spacer2.grid(column=0, row=6)

        cancel = tk.Button(win4, text="Cancel", command=partial(close, win4, "return to login")) #button closes new user window and reopens the login window
        cancel.grid(column=0, row=6)
        create = tk.Button(win4, text="Submit", command=partial(create_user, win4, newusername, password1, password2, security_question, security_question_ans, security_question_options)) #submits the new user info
        create.grid(column=1, row=6)

    #window prompts enter the username of the account you want to reset password
    #contains other functions needed for the password change
    def resetpw():
        #checks if the entered username is in the JSON and opens the security question page
        def checkuser():
            usercounter = 0
            for User in data_dict["users"]: #iterates through all users
                if resetusername.get() == User["username"]: #checks if the entered user matches
                    win7.withdraw() #close username window
                    SQinfo(User) #calls security question window
                    break
                else:
                    usercounter += 1
            if usercounter == len(data_dict["users"]): #after iterating through and the number of iterations matches the total number of users, give an error
                nouser.pack()

        #window containing the user's security question and prompt for an answer
        def SQinfo(User):
            #initialize window
            win8 = tk.Tk()
            win8.geometry('300x200')
            win8.title("Reset Password")

            #labels and entry boxes
            security_q = tk.Label(win8, text=User["security question"])
            security_q.pack()
            security_ans = tk.Entry(win8)
            security_ans.pack()
            incorrectSQans = tk.Label(win8, text="The inputted answer is not corrent.")
            changepwsubmit = tk.Button(win8, text="Submit", command=partial(checkSQ, win8, User, security_ans, incorrectSQans)) #button to submit security question answer
            changepwsubmit.pack()
            cancel = tk.Button(win8, text="Cancel", command=partial(close, win8, "return to login")) #cancel changing password and return to login
            cancel.pack()

        #checks if the security question answer matches
        def checkSQ(win8, User, security_ans, incorrectSQans):
            if security_ans.get() == User["security password"]: #checks if the answer matches
                win8.withdraw() 
                changepwwin() #opens the change password window
            else:
                incorrectSQans.pack() #show error message

        #window to change password
        def changepwwin():
            #initialize window
            win9 = tk.Tk()
            win9.geometry('250x175')
            win9.title("Change Password")
            
            #labels and entry boxes
            pwlabel1 = tk.Label(win9, text="Password: ")
            pwlabel1.grid(column=0, row=1)
            password1 = tk.Entry(win9, show="*")
            password1.grid(column=1, row=1)
            pwlabel2 = tk.Label(win9, text="Confirm Password: ")
            pwlabel2.grid(column=0, row=2)
            password2 = tk.Entry(win9, show="*")
            password2.grid(column=1, row=2)
            
            cancel = tk.Button(win9, text="Cancel", command=partial(close, win9, "return to login")) #button to cancel and reopen login window
            cancel.grid(column=0, row=6)
            submit = tk.Button(win9, text="Submit", command=partial(changepw, win9, password1, password2)) #submit the password change
            submit.grid(column=1, row=6)
        
        #checks if the new password meets requirements and either gives errors or changes the password
        def changepw(win9, password1, password2):
            error_list = []
            if password1.get() != password2.get():
                error_list.append("The inputted passwords do not match.")
            if not len(password1.get()) >= 10:
                error_list.append("The inputted password is not at least 10 characters long.")
            if any(password1.get() in string.ascii_uppercase for _ in password1.get()) == False:
                error_list.append("The inputted password does not contain at least 1 capital letter.")
            if any(password1.get() in string.digits for _ in password1.get()) == False:
                error_list.append("The inputted password does not contain at least 1 digit.")
            if any(password1.get() in string.punctuation for _ in password1.get()) == False:
                error_list.append("The inputted password does not contain at least 1 punctuation character.")
            if not error_list: #if there are no errors, iterate though the list of users and match the username before changing password
                userindex = 0
                for User in data_dict["users"]: #iterate through all users
                    if User["username"] == resetusername.get(): #if username matches the iterated name
                        data_dict["users"][userindex]["password"] = password1 #save the password change in the list

                        #save changes into JSON
                        json_dict = json.dumps(data_dict)
                        file = open(db, "w")
                        file.write(json_dict)
                        file.close

                        #initialize and open window indicating the password changed
                        win9.withdraw()
                        win10 = tk.Tk()
                        win10.geometry('150x50')
                        win10.title("Password Successfully Changed")

                        success = tk.Label(win10, text="The oassword successfully changed.")
                        success.pack()

                        okay = tk.Button(win10, text="Okay", command=partial(close, win10, "return to login"))
                        okay.pack()
                    userindex += 1
            else: #creates a window containing all unmatched password conditions
                newpw_error_msg(error_list)

        #creates the window with all unmatched conditions/errors
        def newpw_error_msg(error_list):
            #initialize window
            win11 = tk.Tk()
            win11.geometry('400x200')
            win11.title("New User Error")

            #adds each error onto the window
            for i in range(len(error_list)):
                error = error_list[i]
                message = tk.Label(win11, text=error)
                message.pack()

            okay = tk.Button(win11, text="Okay", command=partial(close, win11, "self")) #closes error window and reopens the password page
            okay.pack()
    
        window.withdraw() #closes login screen window

        #initializes reset password username entry window
        win7 = tk.Tk()
        win7.geometry('300x200')
        win7.title("Reset Password")

        #opens and reads JSON
        file = open(db, "r")
        x = file.readline()
        data_dict = json.loads(x)
        file.close

        #labels and entry boxes
        resetusernamelabel = tk.Label(win7, text="Username: ")
        resetusernamelabel.pack()
        resetusername = tk.Entry(win7)
        resetusername.pack()

        nouser = tk.Label(win7, text="No such user exists.")

        submitusername = tk.Button(win7, text="Submit", command=checkuser) #button to check if the user exists
        submitusername.pack()

        cancel = tk.Button(win7, text="Cancel", command=partial(close, win7, "return to login")) #button to cancel password recovery/change and return to login screen
        cancel.pack()

    #initialize login screen
    window = tk.Tk()
    window.geometry('300x300')
    window.title("Login Screen")

    #creates labels and entry boxes
    usernamelabel = tk.Label(window, text="Username: ")
    usernamelabel.pack()
    username = tk.Entry(window)
    username.pack()

    pwlabel = tk.Label(window, text="Password: ")
    pwlabel.pack()
    password = tk.Entry(window, show="*")
    password.pack()

    incorrect_login_label = tk.Label(window, text="The username or password is incorrect.") #error message but kept hidden
    
    loginsubmit = tk.Button(window, text="Submit", command=login) #submit the login details
    loginsubmit.pack()

    newuser = tk.Button(window, text="New User", command=createuser) #make a new user
    newuser.pack()

    forgotpassword = tk.Button(window, text="Forgot Password?", command=resetpw) #password recovery
    forgotpassword.pack()

    window.mainloop()

loginscreen()