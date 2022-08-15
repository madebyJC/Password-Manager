import json
import time
import random
import pyperclip
from tkinter import *
from tkinter import messagebox


def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showwarning(title="Oops! Empty Field", message="Please do not leave any fields empty!")

    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \n"
                                                              f"Email: {email}\n"
                                                              f"Password: {password}\n"
                                                              f"Save?")
        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)

                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0, END)
                email_entry.delete(0, END)
                password_entry.delete(0, END)


def find_password():
    website = website_entry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showwarning(title="Error!", message="No Data File Found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
            email_entry.delete(0, END)
            password_entry.delete(0, END)
            email_entry.insert(END, email)
            password_entry.insert(END, password)
        else:
            messagebox.showwarning(title="Error!", message=f"No details for {website} exists.")


def generate_password():
    password_entry.delete(0, END)

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(END, password)
    pyperclip.copy(password)


local_time = time.localtime()
user_time = time.strftime('%a, %d %b %Y %H:%M:%S', local_time)

window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

logo = PhotoImage(file="logo.png")

canvas = Canvas(width=200, height=200)
canvas.create_image(100, 100, image=logo)
canvas.grid(column=2, row=1)

website_label = Label(text="Website:")
email_label = Label(text="Email/Username:")
password_label = Label(text="Password:")
website_label.grid(column=1, row=2)
email_label.grid(column=1, row=3)
password_label.grid(column=1, row=4)

website_entry = Entry(width=21)
email_entry = Entry(width=35)
password_entry = Entry(width=21)
website_entry.grid(column=2, row=2)
website_entry.focus()
email_entry.grid(column=2, row=3, columnspan=2)
email_entry.insert(END, "sample@example.com")
password_entry.grid(column=2, row=4)

search_button = Button(text="Search", width=13, command=find_password)
generate_button = Button(text="Generate Password", command=generate_password)
add_button = Button(text="Add", width=35, command=save)
search_button.grid(column=3, row=2)
generate_button.grid(column=3, row=4)
add_button.grid(column=2, row=5, columnspan=2)

window.mainloop()
