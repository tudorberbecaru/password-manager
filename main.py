from tkinter import *
from tkinter import messagebox
from random import shuffle, choice, randint
import pyperclip
import json
import os

EMAIL = os.environ.get('EMAIL', 'email@example.com')
LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
SYMBOLS = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():

    # Clear the password entry
    password_entry.delete(0, "end")

    # Generate password components
    password_letters = [choice(LETTERS) for _ in range(randint(8, 10))]
    password_symbols = [choice(SYMBOLS) for _ in range(randint(2, 4))]
    password_numbers = [choice(NUMBERS) for _ in range(randint(2, 4))]

    # Combine and shuffle password components
    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    # Create the password string
    password = "".join(password_list)

    # Insert password into the entry and copy to clipboard
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_entry():

    # Get data from entry fields
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    # Create a dictionary for new entry
    new_data = {
        website: {
            "username": username,
            "password": password
        }
    }

    # Check for empty fields
    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showinfo(title="Error", message="Please make sure you haven't left any fields empty.")
    else:
        # Confirm entry with user
        is_ok = messagebox.askokcancel(title="Confirm Entry", message=f"These are the details entered:\n\n"
                                                                      f"Website: {website}\n"
                                                                      f"Email/Username: {username}\n"
                                                                      f"Password: {password}\n\n"
                                                                      f"Are you sure you want to save these entries?")

        if is_ok:
            try:
                # Try to open existing data file
                with open("data.json", "r") as data_file:
                    # Reading old data
                    data = json.load(data_file)
                    # Updating old data with new data
                    data.update(new_data)
            except FileNotFoundError:
                # If the file does not exist, create a new one
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                # Save data to data.json
                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                # Clear entry fields after saving
                website_entry.delete(0, 'end')
                password_entry.delete(0, 'end')


# ---------------------------- FIND PASSWORD ------------------------------- #


def find_password():
    # Get website from entry
    website = website_entry.get()

    try:
        # Try to open the data file
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        # Display an error message if the file does not exist
        messagebox.showinfo(title="Error", message="data.json does not exist.")
    else:
        # Check if the website is in data.json
        if website in data:
            # Retrieve username and password and display them
            username = data[website]["username"]
            password = data[website]["password"]
            messagebox.showinfo(title="Entry Found", message=f"Email/Username: {username}\nPassword: {password}")
        else:
            # Display a message if no entry is found for the website
            messagebox.showinfo(title="No Entry Found", message=f"No entry was found for {website}.")


# ---------------------------- UI SETUP ------------------------------- #

# Create the main window
window = Tk()
window.title("Password Manager")
window.config(padx=40, pady=50)

# Canvas / Logo
canvas = Canvas(width=200, height=200)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(70, 100, image=logo_image)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website   ", font=("Courier", 12, "bold"))
website_label.grid(column=0, row=1)
username_label = Label(text="Email/Username   ", font=("Courier", 12, "bold"))
username_label.grid(column=0, row=2)
password_label = Label(text="Password   ", font=("Courier", 12, "bold"))
password_label.grid(column=0, row=3)

# Entries
website_entry = Entry(width=43)
website_entry.grid(column=1, row=1, sticky="EW")
website_entry.focus()
username_entry = Entry(width=43)
username_entry.grid(column=1, row=2, columnspan=2, sticky="EW")
username_entry.insert(0, EMAIL)
password_entry = Entry(width=43, show="*")
password_entry.grid(column=1, row=3)

# Buttons
search_button = Button(text="Search", command=find_password)
search_button.grid(row=1, column=2, sticky="EW")
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(column=2, row=3)
add_button = Button(text="Add", command=save_entry)
add_button.grid(column=1, row=4, columnspan=2, sticky="EW")

window.mainloop()
