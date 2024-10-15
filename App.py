from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import csv
from tkinter import ttk

FONT = ("Consolas", 10, "bold")

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Password Generator

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    [password_list.append(random.choice(letters)) for _ in range(nr_letters)]
    [password_list.append(random.choice(symbols)) for _ in range(nr_symbols)]
    [password_list.append(random.choice(numbers)) for _ in range(nr_numbers)]

    random.shuffle(password_list)
    password = "".join(password_list)

    pyperclip.copy(password)

    password_input.delete(0, END)
    password_input.insert(0, str(password))


# ---------------------------- SAVE PASSWORD ------------------------------- #

def add():
    keys = ["website", "email", "username", "password"]

    if website_input.get() == "" or username_input.get() == "" or password_input.get() == "":
        messagebox.showinfo(title="Listen Up", message="No Empty Fields Allowed")

    else:
        value_entry = [website_input.get(), email_input.get(), username_input.get(), password_input.get()]
        entry_dict = {key: value for (key, value) in zip(keys, value_entry)}

        if messagebox.askyesno(title="Please Confirm", message=f"{entry_dict}\nIs This Okay?"):
            website_input.delete(0, END)
            email_input.delete(0, END)
            username_input.delete(0, END)
            password_input.delete(0, END)

            with open("data.csv", "a", newline="") as data_file:
                writer = csv.writer(data_file)
                writer.writerow(value_entry)


# Function to display saved passwords
def display_passwords():
    # Create a new window for displaying passwords
    passwords_window = Toplevel()
    passwords_window.title("Saved Passwords")

    # Create a Treeview widget
    tree = ttk.Treeview(passwords_window)
    tree['columns'] = ('Website', 'Email', 'Username', 'Password')

    # Define column headings
    tree.heading('#0', text='ID')
    tree.heading('Website', text='Website')
    tree.heading('Email', text='Email')
    tree.heading('Username', text='Username')
    tree.heading('Password', text='Password')

    # Format column widths
    tree.column('#0', width=50)
    tree.column('Website', width=150)
    tree.column('Email', width=150)
    tree.column('Username', width=150)
    tree.column('Password', width=150)

    # Read data from file and insert into treeview
    with open("data.csv", "r") as data_file:
        csv_reader = csv.reader(data_file)
        for i, row in enumerate(csv_reader):
            tree.insert(parent='', index='end', iid=i, text=str(i+1), values=row)

    # Delete selected item from the treeview
    def delete_item():
        selected_item = tree.selection()
        if selected_item:
            # Prompt user for confirmation
            confirm = messagebox.askyesno(title="Confirm Deletion", message="Are you sure you want to delete this record?")
            if confirm:
                # Delete item from treeview
                tree.delete(selected_item)
                # Update data file
                with open("data.csv", "w", newline="") as data_file:
                    writer = csv.writer(data_file)
                    for item in tree.get_children():
                        values = tree.item(item, 'values')
                        writer.writerow(values)
                messagebox.showinfo(title="Deletion Successful", message="Record deleted successfully.")
        else:
            messagebox.showinfo(title="No Selection", message="Please select an item to delete.")

    # Create a Delete button
    delete_button = Button(passwords_window, text="Delete", command=delete_item)
    delete_button.pack()

    # Pack the treeview
    tree.pack()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

# Website Label
website = Label(text="Website :", font=FONT, anchor="w")
website.grid(row=1, column=0, sticky="w", pady=5)

# Email Label
email = Label(text="Email :", font=FONT, anchor="w")
email.grid(row=2, column=0, sticky="w", pady=5)

# Username Label
username = Label(text="Username :", font=FONT, anchor="w")
username.grid(row=3, column=0, sticky="w", pady=5)

# Password Label
password = Label(text="Password :", font=FONT, anchor="w")
password.grid(row=4, column=0, sticky="w", pady=5)

# Website Input
website_input = Entry(width=35)
website_input.focus()
website_input.grid(row=1, column=1, columnspan=2, sticky="w", pady=5)

# Email Input
email_input = Entry(width=35)
email_input.grid(row=2, column=1, columnspan=2, sticky="w", pady=5)

# Username Input
username_input = Entry(width=35)
username_input.grid(row=3, column=1, columnspan=2, sticky="w", pady=5)

# Password Input
password_input = Entry(width=35)
password_input.grid(row=4, column=1, sticky="w", pady=5)

# Generate Password Button
gen_pass = Button(text="Generate Password", width=29, command=generate_password)
gen_pass.grid(row=5, column=1, sticky="w", pady=5)

# Add Button
add_button = Button(text="Add", width=29, command=add)
add_button.grid(row=6, column=1, sticky="w", pady=5)

# Display Passwords Button
display_button = Button(text="Display Passwords", width=29, command=display_passwords)
display_button.grid(row=7, column=1, sticky="w", pady=5)

window.mainloop()
