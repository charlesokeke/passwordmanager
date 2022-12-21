from tkinter import * #Imports Tkinter
import sys #Imports sys, used to end the program later

root=Tk() #Declares root as the tkinter main window
top = Toplevel() #Creates the toplevel window

top.title("Password Manager")
top.config(padx=100, pady=50)
canvas = Canvas(top, height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(155 / 2, 200 / 2, anchor="center", image=logo_img)
canvas.grid(row=0, column=1, sticky="", columnspan=3)
user_label = Label(top,text="Username:", font="san-serif")
user_label.grid(row=1, column=0, sticky=W)
password_label = Label(top,text="Password:", pady=10, font="san-serif")
password_label.grid(row=2, columnspan=1, column=0)
user_entry = Entry(top,width=30, font=("san-serif", 15))
user_password = Entry(top,width=30, font=("san-serif", 15))
submit_button = Button(top,width=36, text="Submit", pady=5, bg="snow3", fg="black", font={"san-serif" "bold"},
                       command=lambda: command1())
submit_button.grid(row=3, column=1)
cancel_button = Button(top,width=36, text="Submit", pady=5, bg="snow3", fg="black", font={"san-serif" "bold"},
                       command=lambda: command2())
cancel_button.grid(row=4, column=1)
user_entry.grid(row=1, column=1)
user_password.grid(row=2, column=1)

def command1():
    if user_entry.get() == "user" and user_password.get() == "password": #Checks whether username and password are correct
        #root.deiconify() #Unhides the root window
        top1= Toplevel()
        label1 = Label(top1, text="This is your main window and you can input anything you want here")
        label1.pack()
        top.destroy() #Removes the toplevel window

def command2():
    top.destroy() #Removes the toplevel window
    root.destroy() #Removes the hidden root window
    sys.exit() #Ends the script


root.withdraw() #This hides the main window, it's still present it just can't be seen or interacted with
root.mainloop() #Starts the event loop for the main window