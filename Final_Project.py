import tkinter
import mysql.connector
from tkinter import *
#from tkinter.ttk import *

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="louai123",
    database="Final_Project"
)
mycursor = mydb.cursor()


class User:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

    # adding user to the database
    def add_user(self, id, name, email):
        if(id != '' and name != '' and email != ''):
            sql = "INSERT INTO Users (id,name,email) VALUES (%s,%s,%s)"
            val = (id, name, email)
            mycursor.execute(sql, val)
            mydb.commit()
        else:
            print("Please fill out all the details")

class Event(User):

    def __init__(self, event_id, type, description, address, danger_level, user):
        self.event_id = event_id
        self.type = type
        self.description = description
        self.address = address
        self.danger_level = danger_level
        self.user = user

    # adding event to the database
    def add_event(self, event_id, type, description, address, danger_level, user_id):
        if(event_id != '' and type != '' and description !='' and address != '' and danger_level != '' and user_id != ''):
            sql = "INSERT INTO Events (event_id, type,description,address,danger_level,user_id) VALUES (%s, %s,%s, %s,%s, %s)"
            val = (event_id, type, description, address, danger_level, user_id)
            mycursor.execute(sql, val)
            mydb.commit()
            print("Event", event_id, "Successfully added !")
        else:
            print("Please fill out all the details")


    # editing event that already in the database
    def edit_event(self, event_id, type, description, address, danger_level):
        sql_if_Exist = "Select Count(*) from Events where event_id = %s"
        val_if_Exist = (event_id,)
        mycursor.execute(sql_if_Exist, val_if_Exist)
        res = mycursor.fetchall()
        if res[0][0] > 0:
            sql = "Update Events SET type = %s ,description = %s,address = %s , danger_level = %s where event_id = %s "
            val = (type, description, address, danger_level, event_id)
            mycursor.execute(sql, val)
            print("Event", event_id, "successfully edited!")
        else:
            print("Event with id", event_id, "doesn't Exist!")
        mydb.commit()

    # deleting an event from the database
    def delete_event(self, event_id):
        sql_if_Exist = "Select Count(*) from Events where event_id = %s"
        val_if_Exist = (event_id,)
        mycursor.execute(sql_if_Exist, val_if_Exist)
        res = mycursor.fetchall()
        if res[0][0] > 0:
            sql1 = "Delete from Verifiers where event_id = %s"
            val1 = (event_id,)
            mycursor.execute(sql1, val1)
            sql = "Delete from Events where event_id = %s"
            val = (event_id,)
            mycursor.execute(sql, val)
            print("Event", event_id, "successfully deleted!")
        else:
            print("Event with id", event_id, "doesn't Exist!")
        mydb.commit()

    # Show all the events that exist in the database
    def show_all_events():
        event_window = Tk()
        event_window.title('All Events')
        event_window.geometry("400x400")
        event_window.grid_columnconfigure((0, 1), weight=1)
        event_window.configure(bg='#C1CDCD')
        data=''
        mycursor.execute("SELECT * FROM Events ")
        Events = mycursor.fetchall()
        titles = ['Event ID', 'Type', 'Description', 'Location', 'Danger Level', 'From User']
        for e in Events:
            data += "\nEvent Details:\n"
            for i in range(len(e)):
                data += str(titles[i]) + ":" + str(e[i])+'\n'
        T = Text(event_window,font=("Calibri",14))
        T.insert(tkinter.END,data)
        T.grid()

    # Approving an event
    def approve_event(self, event_id, user_id):
        sql_check_user_existing = "Select count(*) from Users where id = %s"
        val_check_user_existing = (user_id,)
        mycursor.execute(sql_check_user_existing, val_check_user_existing)
        query_ans = mycursor.fetchall()
        if query_ans[0][0] > 0:
            sql_bdeka = "select user_id from Events where event_id= %s"  # user_id hon ho el reporter
            val_bdeka = (event_id,)
            mycursor.execute(sql_bdeka, val_bdeka)
            bdika = mycursor.fetchall()  # user_id hon ho el reporter
            if str(bdika[0][0]) != user_id:  # hon mnf7s eza el verifier nfsu el reporter
                sql = "INSERT INTO Verifiers (event_id,Verifier_id) values (%s,%s)"
                values = (event_id, user_id,)
                mycursor.execute(sql, values)
                sql1 = "update Users set Money_from_Verifies = Money_from_Verifies + 3 where id = %s "
                values1 = (user_id,)
                mycursor.execute(sql1, values1)
                sql_check = "Select count(*) from Verifiers where event_id = %s"
                val_check = (event_id,)
                mycursor.execute(sql_check, val_check)
                Verifiers_Per_Event = mycursor.fetchall()
                if Verifiers_Per_Event[0][0] == 5:
                    sql_add = "update Users set Money_from_Reports = Money_from_Reports + 10 where id = %s"
                    val_add = (str(bdika[0][0]),)
                    mycursor.execute(sql_add, val_add)
                    mydb.commit()
                if Verifiers_Per_Event[0][0] > 5:
                    sql_add = "update Users set Money_from_Reports = Money_from_Reports + 2 where id = %s"
                    val_add = (str(bdika[0][0]),)
                    mycursor.execute(sql_add, val_add)
                    mydb.commit()
            else:
                print("You Cant Verify your own Event report!")
        else:
            print("User Not Found!!\nadd it by using (add_user) function , or check it's ID again... ")
        mydb.commit()


    # Showing the users that approved an specific event
    def show_approved_users(self, event_id):
        event_window = Tk()
        event_window.title('All Approved Users of specific')
        event_window.geometry("400x400")
        event_window.grid_columnconfigure((0, 1), weight=1)
        event_window.configure(bg='#C1CDCD')
        sql_check_event_existing = "select count(*) from Events where event_id = %s"
        val_check_event_existing = (event_id,)
        mycursor.execute(sql_check_event_existing, val_check_event_existing)
        query_ans = mycursor.fetchall()
        text = ''
        if query_ans[0][0] > 0:
            sql = "select Verifier_id from Verifiers where event_id=%s"
            val = (event_id,)
            mycursor.execute(sql, val)
            res = mycursor.fetchall()
            titles = ["ID","Name","Email"]
            if len(res) > 0:
                text += f"The users that Verified {event_id} Event are:\n"
                for i in res:
                    sql_user_info = "select id,name,email from Users where id = %s"
                    val_user_info = (str(i[0]),)
                    mycursor.execute(sql_user_info, val_user_info)
                    User_info = mycursor.fetchall()
                    for v in User_info:
                        text += "\n"
                        text += "User Details:\n"
                        for i in range(len(v)):
                            text += f"{titles[i]} : {str(v[i])} \n"
            else:
                text += f"The Event '{event_id}' has no Verifies!!"
        else:
            text += f"Event {event_id} Doesn't Exist!"
        T = Text(event_window, font=("Calibri", 14))
        T.insert(tkinter.END, text)
        T.grid()

    # Showing the events that reported by a specific user
    def show_reported_events(self, user_id):
        event_window = Tk()
        event_window.title('All Reported Events By User')
        event_window.geometry("400x400")
        event_window.grid_columnconfigure((0, 1), weight=1)
        event_window.configure(bg='#C1CDCD')
        sql_check_user_existing = "Select count(*) from Users where id = %s"
        val_check_user_existing = (user_id,)
        mycursor.execute(sql_check_user_existing, val_check_user_existing)
        query_ans = mycursor.fetchall()
        text = ''
        titles = ['Event ID', 'Type', 'Description', 'Location', 'Danger Level', 'From User']
        if query_ans[0][0] > 0:
            sql = "select * from Events where user_id = %s"
            val = (user_id,)
            mycursor.execute(sql, val)
            res = mycursor.fetchall()
            if(len(res) > 0):
                text += f"The Events that Reported by user {user_id} are:\n"
                for i in res:
                    text += "\n"
                    text += "Event Details:\n"
                    for v in range(len(i[:len(i) - 1])):
                        text += f"{titles[v]}: {i[:len(i) - 1][v]} \n"
            else:
                text += f"No Events reported by user {user_id}"
        else:
            text += f"User {user_id} Doesn't Exist!!"
        T = Text(event_window, font=("Calibri", 14))
        T.insert(tkinter.END, text)
        T.grid()

    # Showing report of the user.
    def show_report(self, user_id):
        event_window = Tk()
        event_window.title('User Report 1')
        event_window.geometry("600x600")
        event_window.grid_columnconfigure((0, 1), weight=1)
        event_window.configure(bg='#C1CDCD')
        sql_check_user_existing = "Select count(*) from Users where id = %s"
        val_check_user_existing = (user_id,)
        mycursor.execute(sql_check_user_existing, val_check_user_existing)
        query_ans = mycursor.fetchall()
        report = ''
        if query_ans[0][0] > 0:
            sql = "select Count(*) from Events where user_id = %s"
            val = (user_id,)
            mycursor.execute(sql, val)
            reported = mycursor.fetchall()
            report += f"The user {user_id} has been Reported {reported[0][0]} Events\n"
            sql1 = "Select Count(*) from Verifiers where Verifier_id=%s"
            val1 = (user_id,)
            mycursor.execute(sql1, val1)
            verified = mycursor.fetchall()
            report += f"The user {user_id} has been Verified {verified[0][0]} Events"
        else:
            report += f"User {user_id} Doesn't exist!!"
        T = Text(event_window, font=("Calibri", 18))
        T.insert(tkinter.END, report)
        T.grid()


    # ------------------------------------Part 2------------------------------------

    # showing report 2 of the user
    def show_report2(self, user_id):
        event_window = Tk()
        event_window.title('User Report 2')
        event_window.geometry("600x600")
        event_window.grid_columnconfigure((0, 1), weight=1)
        event_window.configure(bg='#C1CDCD')
        sql_check_user_existing = "Select count(*) from Users where id = %s"
        val_check_user_existing = (user_id,)
        mycursor.execute(sql_check_user_existing, val_check_user_existing)
        query_ans = mycursor.fetchall()
        report = ''
        if query_ans[0][0] > 0:
            sql = "Select Money_from_Reports,Money_from_Verifies from Users where id = %s "
            val = (user_id,)
            mycursor.execute(sql, val)
            res = mycursor.fetchall()
            Money_from_reports = res[0][0]
            Money_from_verifies = res[0][1]
            report += f"The money that user {user_id} has gained from reporting events is: {Money_from_reports}\n"
            report += f"The money that user {user_id} has gained from Verifying events is: {Money_from_verifies}\n"
        else:
            report += f"User {user_id} Doesn't exist!!"
        T = Text(event_window, font=("Calibri", 16))
        T.insert(tkinter.END, report)
        T.grid()


class Comment:
    def __init__(self, user_id, Text):
        self.user_id = user_id
        self.Text = Text

    # Adding a comment to an event
    def add_comment(self, event_id, user_id, comment):
        sql_check_user_existing = "Select count(*) from Users where id = %s"
        val_check_user_existing = (user_id,)
        mycursor.execute(sql_check_user_existing, val_check_user_existing)
        query_ans = mycursor.fetchall()
        sql_check_event_existing = "select count(*) from Events where event_id = %s"
        val_check_event_existing = (event_id,)
        mycursor.execute(sql_check_event_existing, val_check_event_existing)
        query_ans_event = mycursor.fetchall()
        query_reporter = "select user_id from Events where event_id = %s"
        val_reporter = (event_id,)
        mycursor.execute(query_reporter, val_reporter)
        reporter = mycursor.fetchall()
        reporter = reporter[0][0]
        if query_ans[0][0] > 0 and query_ans_event[0][0] > 0 and str(reporter) != user_id:
            sql = "Insert into Comment (event_id,From_User,event_comment) VALUES (%s,%s,%s)"
            val = (event_id, user_id, comment,)
            mycursor.execute(sql, val)
            print("The Comment has been added successfully!")
        else:
            print("Event id or user id are not Available")
        mydb.commit()

    # editing a comment to an event
    def edit_comment(self, event_id, user_id, comment):
        sql_if_Exist = "Select Count(*) from Comment where event_id = %s and From_User = %s "
        val_if_Exist = (event_id,user_id,)
        mycursor.execute(sql_if_Exist, val_if_Exist)
        res = mycursor.fetchall()
        if res[0][0] > 0:
            sql = "Update Comment SET event_id = %s ,From_User = %s ,event_Comment = %s  where event_id = %s "
            val = (event_id, user_id, comment ,event_id,)
            mycursor.execute(sql, val)
            print("Event", event_id, "successfully edited!")
        else:
            print("Event with id", event_id, "doesn't Exist!")
        mydb.commit()

    # deleting a comment from an event
    def delete_comment(self, event_id, user_id):
        sql_if_Exist = "Select Count(*) from Comment where event_id = %s and From_user = %s"
        val_if_Exist = (event_id, user_id)
        mycursor.execute(sql_if_Exist, val_if_Exist)
        res = mycursor.fetchall()
        if res[0][0] > 0:
            sql1 = "Delete from Comment where event_id = %s and From_user = %s"
            val1 = (event_id, user_id)
            mycursor.execute(sql1, val1)
            # sql = "Delete from Comment where event_id = %s"
            # val = (event_id,)
            # mycursor.execute(sql, val)
            print("Comment that written on event", event_id, "by user", user_id, "successfully deleted!")
        else:
            print("Comment that written on event", event_id, "by user", user_id, "doesn't Exist!")
        mydb.commit()

class System:

    # Show the user that have maximum reports
    def max_reports():
        event_window = Tk()
        event_window.title('Maximum Reports')
        event_window.geometry("400x400")
        event_window.grid_columnconfigure((0, 1), weight=1)
        event_window.configure(bg='#C1CDCD')
        mycursor.execute(
            """select id, name, email , count(user_id)
             from Events e join Users u on e.user_id = u.id 
             group by user_id
              order by count(user_id) desc
              LIMIT 1""")
        text = ''
        data = mycursor.fetchall()
        titles = ["ID", "Name", "Email"]
        text += "The User With Maximum Reports is:\n"
        for line in data:
            for i in range(len(line)):
                if (i != len(line) - 1):
                    text += f"{titles[i]}: {line[i]}\n"
                else:
                    text += f"Reported Times: {line[len(line) - 1]}"
        T = Text(event_window,bg='#C1CDCD', font=("Calibri", 16))
        T.insert(tkinter.END, text)
        T.grid()


    # Show the user that have maximum revenue
    def max_revenue():
        event_window = Tk()
        event_window.title('Maximum Revenue')
        event_window.geometry("400x400")
        event_window.grid_columnconfigure((0, 1), weight=1)
        event_window.configure(bg='#C1CDCD')
        mycursor.execute(
            "select id, name, email, revenue from Users where revenue = (select max(revenue) from Users ) ")
        data = mycursor.fetchall()
        text = ''
        titles = ["ID", "Name", "Email","Revenue"]
        text += "The user with maximum revenue is:\n"
        for line in data:
            for i in range(len(line)):
                text += f"{titles[i]}: {line[i]}\n"
        T = Text(event_window,bg='#C1CDCD', font=("Calibri", 16))
        T.insert(tkinter.END, text)
        T.grid()


    # Showing the count of the events type (easy/medium/hard)
    def types_count():
        event_window = Tk()
        event_window.title('Types Count')
        event_window.geometry("250x250")
        event_window.grid_columnconfigure((0, 1), weight=1)
        event_window.configure(bg='#C1CDCD')
        mycursor.execute("select danger_level,Count(*) from Events Group by danger_level")
        data = mycursor.fetchall()
        text = ''
        text += "Count the Events By type:\n"
        for line in data[1:]:
            for value in line:
                text += f"{value} "
            text+="\n"
        T = Text(event_window, bg='#C1CDCD',font=("Calibri", 16))
        T.insert(tkinter.END, text)
        T.grid()


# =========================================================================================================
## ======================   GUI PART  =====================================================================
# secondary window opens after clicking on add user button
def add_user_window():
    user_window = Tk()
    user_window.title('Add User')
    user_window.geometry("350x350")
    user_window.grid_columnconfigure((0, 1), weight=1)
    user_window.configure(bg='#C1CDCD')
    MainLabel = Label(user_window, bg='#C1CDCD', text="Add User Info", font=("Arial", 30))
    MainLabel.grid(row=0, column=1)
    labelID = Label(user_window, bg='#C1CDCD', text='ID:', font=("Arial", 25))
    labelID.grid(row=1, column=0)
    enrtyID = Entry(user_window, bd=3)
    enrtyID.grid(row=1, column=1)
    space = Label(user_window, bg='#C1CDCD', text='\n', font=("Arial", 10))
    space.grid(row=2, column=0)
    labelname = Label(user_window, bg='#C1CDCD', text='Name:', font=("Arial", 25))
    labelname.grid(row=3, column=0)
    enrtyName = Entry(user_window)
    enrtyName.grid(row=3, column=1)
    space1 = Label(user_window, bg='#C1CDCD', text='\n', font=("Arial", 10))
    space1.grid(row=4, column=0)
    labelEmail = Label(user_window, bg='#C1CDCD', text='Email:', font=("Arial", 25))
    labelEmail.grid(row=5, column=0)
    enrtyEmail = Entry(user_window)
    enrtyEmail.grid(row=5, column=1)
    add_btn = Button(user_window, text='ADD',height=2, width=10,
                     command=lambda: [User.add_user('', enrtyID.get(), enrtyName.get(), enrtyEmail.get()),user_window.destroy()])
    add_btn.grid(row=6, column=1)

# secondary window opens after clicking on add event button
def add_event_window():
    event_window = Tk()
    event_window.title('Add Event')
    event_window.geometry("400x400")
    event_window.grid_columnconfigure((0, 1), weight=1)
    event_window.configure(bg='#C1CDCD')
    MainLabel = Label(event_window, bg='#C1CDCD', text="Add Event Info", font=("Arial", 30))
    MainLabel.grid(row=0, column=1)
    labelID = Label(event_window, bg='#C1CDCD', text='Event ID:', font=("Arial", 25))
    labelID.grid(row=1, column=0)
    enrtyID = Entry(event_window)
    enrtyID.grid(row=1, column=1)
    labelType = Label(event_window, bg='#C1CDCD', text='Type:', font=("Arial", 25))
    labelType.grid(row=2, column=0)
    enrtyType = Entry(event_window)
    enrtyType.grid(row=2, column=1)
    labeldescription = Label(event_window, bg='#C1CDCD', text='Description:', font=("Arial", 25))
    labeldescription.grid(row=3, column=0)
    enrtydescription = Entry(event_window)
    enrtydescription.grid(row=3, column=1)
    labeladdress = Label(event_window, bg='#C1CDCD', text='Address:', font=("Arial", 25))
    labeladdress.grid(row=4, column=0)
    enrtyaddress = Entry(event_window)
    enrtyaddress.grid(row=4, column=1)
    labelDanger = Label(event_window, bg='#C1CDCD', text='Danger Level:', font=("Arial", 25))
    labelDanger.grid(row=5, column=0)
    enrtyDanger = Entry(event_window)
    enrtyDanger.grid(row=5, column=1)
    labelReporter = Label(event_window, bg='#C1CDCD', text='Reporter ID:', font=("Arial", 25))
    labelReporter.grid(row=6, column=0)
    enrtyReporter = Entry(event_window)
    enrtyReporter.grid(row=6, column=1)
    space = Label(event_window, text="\n", bg='#C1CDCD', font=("Arial", 8))
    space.grid(row=7, column=1)
    add_btn = Button(event_window, text='ADD', bg="#66CD00", height=2, width=10, font=("Arial", 15),
                     command=lambda: [Event.add_event('', enrtyID.get(), enrtyType.get(), enrtydescription.get(),
                                                     enrtyaddress.get(), enrtyDanger.get(), enrtyReporter.get()),event_window.destroy()])
    add_btn.grid(row=8, column=1)

# secondary window opens after clicking on edit event button
def edit_event_window():
    event_window = Tk()
    event_window.title('Edit Event')
    event_window.geometry("400x400")
    event_window.grid_columnconfigure((0, 1), weight=1)
    event_window.configure(bg='#C1CDCD')
    MainLabel = Label(event_window, bg='#C1CDCD', text="Edit Event", font=("Arial", 30))
    MainLabel.grid(row=0, column=1)
    labelID = Label(event_window, bg='#C1CDCD', text='Event ID:', font=("Arial", 25))
    labelID.grid(row=1, column=0)
    enrtyID = Entry(event_window)
    enrtyID.grid(row=1, column=1)
    labelType = Label(event_window, bg='#C1CDCD', text='Type:', font=("Arial", 25))
    labelType.grid(row=2, column=0)
    enrtyType = Entry(event_window)
    enrtyType.grid(row=2, column=1)
    labeldescription = Label(event_window, bg='#C1CDCD', text='Description:', font=("Arial", 25))
    labeldescription.grid(row=3, column=0)
    enrtydescription = Entry(event_window)
    enrtydescription.grid(row=3, column=1)
    labeladdress = Label(event_window, bg='#C1CDCD', text='Address:', font=("Arial", 25))
    labeladdress.grid(row=4, column=0)
    enrtyaddress = Entry(event_window)
    enrtyaddress.grid(row=4, column=1)
    labelDanger = Label(event_window, bg='#C1CDCD', text='Danger Level:', font=("Arial", 25))
    labelDanger.grid(row=5, column=0)
    enrtyDanger = Entry(event_window)
    enrtyDanger.grid(row=5, column=1)
    space = Label(event_window, text="\n", bg='#C1CDCD', font=("Arial", 8))
    space.grid(row=7, column=1)
    edit_btn = Button(event_window, text='EDIT', bg="#66CD00", height=2, width=10, font=("Arial", 15),
                     command=lambda: [Event.add_event('', enrtyID.get(), enrtyType.get(), enrtydescription.get(),
                                                     enrtyaddress.get(), enrtyDanger.get()),event_window.destroy()])
    edit_btn.grid(row=8, column=1)

# secondary window opens after clicking on delete event button
def delete_event_window():
    event_window = Tk()
    event_window.title('Delete Event')
    event_window.geometry("400x400")
    event_window.grid_columnconfigure((0, 1), weight=1)
    event_window.configure(bg='#C1CDCD')
    MainLabel = Label(event_window, bg='#C1CDCD', text="Delete Event", font=("Arial", 30))
    MainLabel.grid(row=0, column=1)
    labelID = Label(event_window, bg='#C1CDCD', text='Event ID:', font=("Arial", 25))
    labelID.grid(row=1, column=0)
    enrtyID = Entry(event_window)
    enrtyID.grid(row=1, column=1)

    space = Label(event_window, text="\n", bg='#C1CDCD', font=("Arial", 8))
    space.grid(row=7, column=1)
    delete_btn = Button(event_window, text='DELETE', bg="#66CD00", height=2, width=10, font=("Arial", 15),
                     command=lambda: [Event.delete_event('', enrtyID.get()),event_window.destroy()])
    delete_btn.grid(row=8, column=1)

# secondary window opens after clicking on delete event button
def approve_event_window():
    event_window = Tk()
    event_window.title('Approve Event')
    event_window.geometry("400x400")
    event_window.grid_columnconfigure((0, 1), weight=1)
    event_window.configure(bg='#C1CDCD')
    MainLabel = Label(event_window, bg='#C1CDCD', text="Approve Event", font=("Arial", 30))
    MainLabel.grid(row=0, column=1)
    labelID = Label(event_window, bg='#C1CDCD', text='Event ID:', font=("Arial", 25))
    labelID.grid(row=1, column=0)
    enrtyID = Entry(event_window)
    enrtyID.grid(row=1, column=1)
    label_usrID = Label(event_window, bg='#C1CDCD', text='User ID:', font=("Arial", 25))
    label_usrID.grid(row=2, column=0)
    enrty_usrID = Entry(event_window)
    enrty_usrID.grid(row=2, column=1)
    approve_btn = Button(event_window, text='APPROVE', bg="#66CD00", height=2, width=10, font=("Arial", 15),
                      command=lambda: [Event.approve_event('', enrtyID.get(), enrty_usrID.get()), event_window.destroy()])
    approve_btn.grid(row=8, column=1)

# secondary window opens after clicking on show approve users button
def show_approve_users_window():
    event_window = Tk()
    event_window.title('Approved Users')
    event_window.geometry("400x400")
    event_window.grid_columnconfigure((0, 1), weight=1)
    event_window.configure(bg='#C1CDCD')
    MainLabel = Label(event_window, bg='#C1CDCD', text="Approved Users", font=("Arial", 30))
    MainLabel.grid(row=0, column=1)
    labelID = Label(event_window, bg='#C1CDCD', text='Event ID:', font=("Arial", 25))
    labelID.grid(row=1, column=0)
    enrtyID = Entry(event_window)
    enrtyID.grid(row=1, column=1)
    show_btn = Button(event_window, text='SHOW', bg="#66CD00", height=2, width=10, font=("Arial", 15),
                         command=lambda: Event.show_approved_users('', enrtyID.get()))
    show_btn.grid(row=8, column=1)

def show_reported_events_window():
    event_window = Tk()
    event_window.title('Reported Events')
    event_window.geometry("400x400")
    event_window.grid_columnconfigure((0, 1), weight=1)
    event_window.configure(bg='#C1CDCD')
    MainLabel = Label(event_window, bg='#C1CDCD', text="Reported Events", font=("Arial", 30))
    MainLabel.grid(row=0, column=1)
    labelID = Label(event_window, bg='#C1CDCD', text='User ID:', font=("Arial", 25))
    labelID.grid(row=1, column=0)
    enrtyID = Entry(event_window)
    enrtyID.grid(row=1, column=1)
    show_btn = Button(event_window, text='SHOW', bg="#66CD00", height=2, width=10, font=("Arial", 15),
                      command=lambda: Event.show_reported_events('', enrtyID.get()))
    show_btn.grid(row=8, column=1)

def show_report1_events_window():
    event_window = Tk()
    event_window.title('User Report')
    event_window.geometry("400x400")
    event_window.grid_columnconfigure((0, 1), weight=1)
    event_window.configure(bg='#C1CDCD')
    MainLabel = Label(event_window ,bg='#C1CDCD', text="User Report", font=("Arial", 30))
    MainLabel.grid(row=0, column=1)
    labelID = Label(event_window, bg='#C1CDCD', text='User ID:', font=("Arial", 25))
    labelID.grid(row=1, column=0)
    enrtyID = Entry(event_window)
    enrtyID.grid(row=1, column=1)
    show_btn = Button(event_window, text='SHOW REPORT', bg="#66CD00", height=2, width=15, font=("Arial", 15),
                      command=lambda: Event.show_report('', enrtyID.get()))
    show_btn.grid(row=8, column=1)

def show_report2_events_window():
    event_window = Tk()
    event_window.title('User Report 2')
    event_window.geometry("400x400")
    event_window.grid_columnconfigure((0, 1), weight=1)
    event_window.configure(bg='#C1CDCD')
    MainLabel = Label(event_window, bg='#C1CDCD', text="User Report 2", font=("Arial", 30))
    MainLabel.grid(row=0, column=1)
    labelID = Label(event_window, bg='#C1CDCD', text='User ID:', font=("Arial", 25))
    labelID.grid(row=1, column=0)
    enrtyID = Entry(event_window)
    enrtyID.grid(row=1, column=1)
    show_btn = Button(event_window, text='SHOW REPORT', bg="#66CD00", height=2, width=15, font=("Arial", 15),
                      command=lambda: Event.show_report2('', enrtyID.get()))
    show_btn.grid(row=8, column=1)

def add_comment_window():
    event_window = Tk()
    event_window.title('Add Comment')
    event_window.geometry("400x400")
    event_window.grid_columnconfigure((0, 1), weight=1)
    event_window.configure(bg='#C1CDCD')
    MainLabel = Label(event_window, bg='#C1CDCD', text="Add Comment Info", font=("Arial", 30))
    MainLabel.grid(row=0, column=1)
    labelID = Label(event_window, bg='#C1CDCD', text='Event ID:', font=("Arial", 25))
    labelID.grid(row=1, column=0)
    enrtyID = Entry(event_window)
    enrtyID.grid(row=1, column=1)
    label_usrID = Label(event_window, bg='#C1CDCD', text='User ID:', font=("Arial", 25))
    label_usrID.grid(row=2, column=0)
    enrty_usrID = Entry(event_window)
    enrty_usrID.grid(row=2, column=1)
    labelcmnt = Label(event_window, bg='#C1CDCD', text='Comment:', font=("Arial", 25))
    labelcmnt.grid(row=3, column=0)
    enrtycmnt = Entry(event_window)
    enrtycmnt.grid(row=3, column=1)
    show_btn = Button(event_window, text='ADD COMMENT', bg="#66CD00", height=2, width=15, font=("Arial", 15),
                      command=lambda: [Comment.add_comment('', enrtyID.get(),enrty_usrID.get(),enrtycmnt.get()),event_window.destroy()])
    show_btn.grid(row=8, column=1)

def edit_comment_window():
    event_window = Tk()
    event_window.title('Edit Comment')
    event_window.geometry("400x400")
    event_window.grid_columnconfigure((0, 1), weight=1)
    event_window.configure(bg='#C1CDCD')
    MainLabel = Label(event_window, bg='#C1CDCD', text="Edit Comment Info", font=("Arial", 30))
    MainLabel.grid(row=0, column=1)
    labelID = Label(event_window, bg='#C1CDCD', text='Event ID:', font=("Arial", 25))
    labelID.grid(row=1, column=0)
    enrtyID = Entry(event_window)
    enrtyID.grid(row=1, column=1)
    label_usrID = Label(event_window, bg='#C1CDCD', text='User ID:', font=("Arial", 25))
    label_usrID.grid(row=2, column=0)
    enrty_usrID = Entry(event_window)
    enrty_usrID.grid(row=2, column=1)
    labelcmnt = Label(event_window, bg='#C1CDCD', text='Comment:', font=("Arial", 25))
    labelcmnt.grid(row=3, column=0)
    enrtycmnt = Entry(event_window)
    enrtycmnt.grid(row=3, column=1)
    show_btn = Button(event_window, text='EDIT', bg="#66CD00", height=2, width=15, font=("Arial", 15),
                      command=lambda: [Comment.edit_comment('', enrtyID.get(), enrty_usrID.get(), enrtycmnt.get()),event_window.destroy()])
    show_btn.grid(row=8, column=1)

def delete_comment_window():
    event_window = Tk()
    event_window.title('Delete Comment')
    event_window.geometry("400x400")
    event_window.grid_columnconfigure((0, 1), weight=1)
    event_window.configure(bg='#C1CDCD')
    MainLabel = Label(event_window, bg='#C1CDCD', text="Delete Comment", font=("Arial", 30))
    MainLabel.grid(row=0, column=1)
    labelID = Label(event_window, bg='#C1CDCD', text='Event ID:', font=("Arial", 25))
    labelID.grid(row=1, column=0)
    enrtyID = Entry(event_window)
    enrtyID.grid(row=1, column=1)
    label_usrID = Label(event_window, bg='#C1CDCD', text='User ID:', font=("Arial", 25))
    label_usrID.grid(row=2, column=0)
    enrty_usrID = Entry(event_window)
    enrty_usrID.grid(row=2, column=1)
    show_btn = Button(event_window, text='DELETE', bg="#66CD00", height=2, width=15, font=("Arial", 15),
                      command=lambda: [Comment.delete_comment('', enrtyID.get(), enrty_usrID.get()),event_window.destroy()])
    show_btn.grid(row=8, column=1)

# to change buttons's color when the mouse hover on the button
def changeOnHover(button, colorOnHover, colorOnLeave):
    # adjusting backgroung of the widget
    # background on entering widget
    button.bind("<Enter>", func=lambda e: button.config(
        highlightbackground=colorOnHover))

    # background color on leving widget
    button.bind("<Leave>", func=lambda e: button.config(
        highlightbackground=colorOnLeave))

# Main Window GUI


Main_Window = Tk()
Main_Window.title('Events Reporting Application')
Main_Window.geometry("370x420")

add_User_btn = Button(Main_Window, text='Add User',width=20, height=3,borderwidth=2 ,command=add_user_window)
add_User_btn.grid(row=1,column=0)
changeOnHover(add_User_btn, "green", "white")

add_event_btn = Button(Main_Window, text="Add Event",width=20,height=3, command=add_event_window)
add_event_btn.grid(row=2,column=0)
changeOnHover(add_event_btn, "green", "white")

edit_event_btn = Button(Main_Window, text="Edit Event",width=20,height=3, command=edit_event_window)
edit_event_btn.grid(row=3,column=0)
changeOnHover(edit_event_btn, "orange", "white")

delete_event_btn = Button(Main_Window, text="Delete Event",width=20, height=3, command=delete_event_window)
delete_event_btn.grid(row=4,column=0)
changeOnHover(delete_event_btn, "red", "white")

approve_event_btn = Button(Main_Window, text="Approve Event",width=20,height=3, command=approve_event_window)
approve_event_btn.grid(row=5,column=0)
changeOnHover(approve_event_btn, "green", "white")

Show_all_events_btn = Button(Main_Window, text="Show All Events",width=20,height=3, command=Event.show_all_events)
Show_all_events_btn.grid(row=6,column=0)
changeOnHover(Show_all_events_btn, "#00BFFF", "white")

Show_users_btn = Button(Main_Window, text="Show Approved Users",width=20, height=3, command=show_approve_users_window)
Show_users_btn.grid(row=7,column=0)
changeOnHover(Show_users_btn, "#00BFFF", "white")

show_reported_events_btn = Button(Main_Window, text="Show Reported Events",width=20,height=3,  command=show_reported_events_window)
show_reported_events_btn.grid(row=8,column=0)
changeOnHover(show_reported_events_btn, "#00BFFF", "white")

show_report1_events_btn = Button(Main_Window, text="Show User Report",width=20,height=3, command=show_report1_events_window)
show_report1_events_btn.grid(row=1,column=1)
changeOnHover(show_report1_events_btn, "#00BFFF", "white")

show_report2_events_btn = Button(Main_Window, text="Show User Report 2",width=20,height=3,  command=show_report2_events_window)
show_report2_events_btn.grid(row=2,column=1)
changeOnHover(show_report2_events_btn, "#00BFFF", "white")

add_comment_btn = Button(Main_Window, text='Add Comment',width=20,height=3,  command=add_comment_window)
add_comment_btn.grid(row=3,column=1)
changeOnHover(add_comment_btn, "green", "white")

edit_comment_btn = Button(Main_Window, text='Edit Comment',width=20,height=3,  command=edit_comment_window) # b3dhaaa
edit_comment_btn.grid(row=4,column=1)
changeOnHover(edit_comment_btn, "orange", "white")

delete_comment_btn = Button(Main_Window, text='Delete Comment',width=20,height=3,  command=delete_comment_window)
delete_comment_btn.grid(row=5,column=1)
changeOnHover(delete_comment_btn, "red", "white")

max_reports_btn = Button(Main_Window, text='Max Reports',width=20,height=3,  command=System.max_reports)
max_reports_btn.grid(row=6,column=1)
changeOnHover(max_reports_btn, "#00BFFF", "white")

max_revenue_btn = Button(Main_Window, text='Max Revenue',width=20,height=3,  command=System.max_revenue)
max_revenue_btn.grid(row=7,column=1)
changeOnHover(max_revenue_btn, "#00BFFF", "white")

Types_count_btn = Button(Main_Window, text='Types Count',width=20,height=3,  command=System.types_count)
Types_count_btn.grid(row=8,column=1)
changeOnHover(Types_count_btn, "#00BFFF", "white")

mydb.commit()

Main_Window.mainloop()
