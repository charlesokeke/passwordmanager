from tkinter import *
from tkinter import messagebox
from main_class import Main
from datetime import date
import os
from tkinter.ttk import Treeview

object_handle = Main()
root = Tk()


def find_password_for_site(entry):
    if entry.get():
        records = object_handle.find_password("%" + entry.get()+"%", int(os.environ["id"]))
        entry.delete(0, "end")
        if records:
            password_search_window(records)
        else:
            messagebox.showinfo("No records", "No records found")

    else:
        messagebox.showinfo("Invalid entry","Fill out the site input field")


def find_passwords_search():
    records = object_handle.find_all_password(int(os.environ["id"]))
    password_search_window(records)


def password_search_window(result=None):
    top4 = Toplevel()
    password_search_tree = Treeview(top4,show=['headings'])
    password_search_tree["columns"] = ("Website", "Password","Name", "Date")
   # password_search_tree.column("0#", width=100,anchor=W)
    password_search_tree.column("Website",anchor=W, width=200)
    password_search_tree.column("Password", anchor=W,width=200)
    password_search_tree.column("Name", width=200, anchor=CENTER)
    password_search_tree.column("Date", width=200, anchor=CENTER)

    #password_search_tree.heading("0#", text="Label", anchor=W)
    password_search_tree.heading("Website", text="Website",anchor=W)
    password_search_tree.heading("Password", text="Password", anchor=W)
    password_search_tree.heading("Name", text="Name", anchor=CENTER)
    password_search_tree.heading("Date", text="Date", anchor=CENTER)

    password_search_tree.grid(column=0,row=0, columnspan=3)
    cancel_tree = Button(top4, text="Close window", width=10,command=lambda:cancel(top4))
    cancel_tree.grid(row=1, column=0, columnspan=3, sticky=W)
    if result:
        for index, value in enumerate(result):
            password_search_tree.insert(parent="", index="end", iid=index, text="Parent",
                                        values=(value[len(value) - 1], value[1], value[2], value[4]))
    print("print")


def clear_auth_fields(user,site,password):

    if user:
        user.delete(0, "end")
    if site:
        site.delete(0, "end")
    if password:
        password.delete(0, "end")


def frame2_children(frame,frame3):
    header = Label(frame, text="Password Search",anchor="center", font=("Helvetica", 14))
    header.grid(column=0, row=0, columnspan=3, )
    find_password_label = Label(frame, text="Enter site name: ")
    find_password_label.grid(column=0, row=1)
    find_password_entry = Entry(frame, font=("san-serif",10),width="20")
    find_password_entry.grid(column=1, row=1)
    find_password_button = Button(frame, text="find site password",command=lambda: find_password_for_site(find_password_entry))
    find_password_button.grid(column=2, row=1)

    find_all_password_label = Label(frame, text="Enter username: ")
    find_all_password_label.grid(column=0, row=2)
    find_all_password_entry = Entry(frame, font=("san-serif", 10), width="20")
    find_all_password_entry.grid(column=1, row=2)
    find_all_password_button = Button(frame, text="find all passwords", command=lambda:find_passwords_search())
    find_all_password_button.grid(column=2, row=2)


def save_user_data_and_gen_pass(password, site, user):
    if (password.get() and site.get()) and user.get():
        print(password.get(), user.get(), os.environ['id'])
        object_handle.insert_password((password.get(), user.get(), os.environ['id'], date.today(), site.get()))
        site_name = site.get()
        password.delete(0, "end")
        site.delete(0, "end")
        user.delete(0, "end")
        messagebox.showinfo("Password Saved", f"Password saved for {site_name}")
    else:
        print("fill all boxes")


def insert_generated_password(gened_pass,frame):
    if gened_pass:
        print(os.environ['id'])
        gened_pass.delete(0, "end")
        password = object_handle.init_passwd()
        gened_pass.insert(0, password)
        frame.clipboard_clear()
        frame.clipboard_append(password)
        messagebox.showinfo("Copied", "Generated password has been copied to clipboard")


def authenticated_window(user=None):
    top1 = Toplevel()
    top1.config(cursor="hand2",bd=20)
    top1.grid_rowconfigure(0, weight=1)
    top1.grid_columnconfigure(0, weight=1)
    frame3 = Frame(top1,bg="gray")
    frame3.grid(column=0, row=0)
    frame = Frame(frame3,padx=25,pady=25)

    frame3.configure(pady=25,padx=25)
    frame2 = Frame(frame3, width=400, height=200)
    frame2.config(padx=16.5, pady=16)
    frame2.grid(row=1, column=0,columnspan=3)
    frame.grid(row=0, column=0,columnspan=3)
    top1.title("Authenticated")
    top1.configure(pady=30, padx=10)
    Label(frame, text=f"Welcome {user.capitalize()}", anchor="center", font=('Helvetica', 14), pady=10).grid(row=0, column=0, columnspan=3)
    Label(frame, text="Name").grid(row=1, column=0)
    Label(frame, text="Site name").grid(row=2, column=0)
    Label(frame, text="Generated password").grid(row=3, column=0)
    user_name = Entry(frame, width=30, font=("san-serif", 10))
    user_name.grid(row=1, column=1)
    user_name.insert(0, user)
    site_name = Entry(frame, width=30, font=("san-serif", 10))
    site_name.grid(row=2, column=1)
    generated_password = Entry(frame, width=30, font=("san-serif", 10))
    generated_password.grid(row=3, column=1)
    generate_password_bt = Button(frame, text="Generate password",
                                  command=lambda: insert_generated_password(generated_password,frame))
    clear_password_bt = Button(frame, text="Clear fields",
                                  command=lambda: clear_auth_fields(user_name,site_name,generated_password))
    save_data_bt = Button(frame, width=10, text="Save data",
                          command=lambda: save_user_data_and_gen_pass(generated_password, site_name, user_name))
    generate_password_bt.grid(row=4, column=0)
    save_data_bt.grid(row=4, column=1, columnspan=1, sticky="w")
    cancel_window = Button(frame, text="Cancel", command=lambda: cancel_program())
    cancel_window.grid(row=4, column=1)
    clear_password_bt.grid(row=4, column=1, sticky="e")

    frame2_children(frame2,frame3)
    cancel(top)  # Removes the toplevel window


def get_insert_signup_data(user, pwd, window):
    if user.get() and pwd.get():
        user_name = user.get()
        user_pwd = pwd.get()
        user.delete(0, "end")
        pwd.delete(0, "end")
        insert_data = object_handle.insert_user((user_name, user_pwd, date.today()))
        if insert_data:
            print(insert_data)
            os.environ["id"] = str(insert_data)
            authenticated_window(user_name)
            cancel(window)

    else:
        print("Invalid input")


def sign_up_window():
    top2 = Toplevel()
    top2.title("Signup")
    top2.geometry('400x200')
    top2.configure(pady=30, padx=50, cursor="hand2", bd=10)
    top2.resizable(0, 0)
    Label(top2, text="Register", anchor="center", font=('Helvetica', 14)).grid(row=0, column=0, columnspan=3)
    a = Label(top2, text="Username").grid(row=1, column=0)
    b = Label(top2, text="Password").grid(row=2, column=0)
    user_signup = Entry(top2, width=30, font=("san-serif", 10))
    user_signup.grid(row=1, column=1)
    password_signup = Entry(top2, width=30, font=("san-serif", 10), show="*")
    password_signup.grid(row=2, column=1)
    sign_up_window_submit = Button(top2, text="Submit",
                                   command=lambda: get_insert_signup_data(user_signup, password_signup, top2))
    sign_up_window_cancel = Button(top2, text="Cancel", command=lambda: cancel(top2))
    sign_up_window_submit.grid(row=3, column=0)
    sign_up_window_cancel.grid(row=3, column=1, columnspan=1, sticky="w")


def login():
    if user_entry.get() and user_password.get():
        user_id = user_entry.get()
        user_pwd = user_password.get()
        user_entry.delete(0, "end")
        user_password.delete(0, "end")
        user = object_handle.authenticate(user_id, user_pwd)
        if user:
            os.environ["id"] = str(user[0])
            authenticated_window(user[1])
        else:
            print("Invalid entry")
            messagebox.showerror("Invalid entry", "Wrong username or password")
    else:
        messagebox.showerror("Invalid entry", "Field out username and password field")
        print("fill in the boxes")


def cancel(window):
    window.destroy()  # Removes the toplevel window
    # sys.exit()  # Ends the script


def cancel_program():
    root.destroy()  # Removes the toplevel window
    sys.exit()  # Ends the script


def round_rectangle(x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1 + radius, y1,
              x1 + radius, y1,
              x2 - radius, y1,
              x2 - radius, y1,
              x2, y1,
              x2, y1 + radius,
              x2, y1 + radius,
              x2, y2 - radius,
              x2, y2 - radius,
              x2, y2,
              x2 - radius, y2,
              x2 - radius, y2,
              x1 + radius, y2,
              x1 + radius, y2,
              x1, y2,
              x1, y2 - radius,
              x1, y2 - radius,
              x1, y1 + radius,
              x1, y1 + radius,
              x1, y1]

    return canvas.create_polygon(points, **kwargs, smooth=True)


def update_rectangle_coords(round_rect, x1, y1, x2, y2, r=25):
    points = (
    x1 + r, y1, x1 + r, y1, x2 - r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2, y1 + r, x2, y2 - r, x2, y2 - r, x2, y2,
    x2 - r, y2, x2 - r, y2, x1 + r, y2, x1 + r, y2, x1, y2, x1, y2 - r, x1, y2 - r, x1, y1 + r, x1, y1 + r, x1, y1)
    canvas.coords(round_rect, *points)


#my_rectangle = round_rectangle(50, 50, 150, 100, radius=20, fill="blue")

top = Toplevel(bg="gray")
top.title("Password Manager")
top.config(padx=50, pady=50,cursor="hand2",bd=10)
top.grid_rowconfigure(0, weight=1)
top.grid_columnconfigure(0, weight=1)
frame1 = Frame(top)
frame1.config(pady=50, padx=50)
frame1.grid(column=0, columnspan=3, row=0)
# root.grid_rowconfigure(0, weight=1)
# root.grid_columnconfigure(0, weight=1)
canvas = Canvas(frame1, height=200, width=200)
logo_img = PhotoImage(data=b'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')
canvas.create_image(200 / 2, 200 / 2, anchor="center", image=logo_img)
canvas.grid(row=0, column=0, columnspan=3)
user_label = Label(frame1, text="Username:", font="san-serif")
user_label.grid(row=1, column=0)
password_label = Label(frame1, text="Password:", pady=10, font="san-serif")
password_label.grid(row=2, column=0)
user_entry = Entry(frame1, width=30, font=("san-serif", 10))
user_password = Entry(frame1, width=30, font=("san-serif", 10), show="*")
submit_button = Button(frame1, width=6, text="Login", bg="snow3", fg="black", font={"san-serif" "bold"},
                       command=lambda: login())
cancel_button = Button(frame1, width=6, text="Cancel", bg="snow3", fg="black", font={"san-serif" "bold"},
                       command=lambda: cancel_program())
submit_button.grid(row=3, column=1, sticky="w")
sign_up_button = Button(frame1, width=6, text="Signup",bg="snow3", fg="black", font={"san-serif" "bold"},
                        command=lambda: sign_up_window())
sign_up_button.grid(row=3, column=1)
user_entry.grid(row=1, column=1)
cancel_button.grid(row=3, column=1, sticky="e")
user_password.grid(row=2, column=1)
root.withdraw()
root.mainloop()
