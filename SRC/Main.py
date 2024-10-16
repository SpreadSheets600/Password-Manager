import customtkinter as ctk
from DataBase import Database
from tkinter import messagebox
from Utilities import generate_password

ctk.set_appearance_mode("Dark") 
ctk.set_default_color_theme("blue") 

db = Database()

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_input.get()
    email = email_input.get()
    username = username_input.get()
    password = password_input.get()

    if not website or not email or not password:
        messagebox.showwarning("Warning", "All fields must be filled!")
    else:
        if messagebox.askyesno("Confirm", f"Save the following details?\nWebsite: {website}\nUsername: {username}"):
            db.save_data(website, email, username, password)
            website_input.delete(0, ctk.END)
            email_input.delete(0, ctk.END)
            username_input.delete(0, ctk.END)
            password_input.delete(0, ctk.END)

# ---------------------------- UI SETUP ------------------------------- #
app = ctk.CTk()
app.title("Password Manager")
app.geometry("500x400")

website_label = ctk.CTkLabel(app, text="Website:")
website_label.grid(row=0, column=0, pady=10, padx=10)
website_input = ctk.CTkEntry(app, width=300)
website_input.grid(row=0, column=1, padx=10)

email_label = ctk.CTkLabel(app, text="Email:")
email_label.grid(row=1, column=0, pady=10, padx=10)
email_input = ctk.CTkEntry(app, width=300)
email_input.grid(row=1, column=1, padx=10)

username_label = ctk.CTkLabel(app, text="Username:")
username_label.grid(row=2, column=0, pady=10, padx=10)
username_input = ctk.CTkEntry(app, width=300)
username_input.grid(row=2, column=1, padx=10)

password_label = ctk.CTkLabel(app, text="Password:")
password_label.grid(row=3, column=0, pady=10, padx=10)
password_input = ctk.CTkEntry(app, width=300)
password_input.grid(row=3, column=1, padx=10)

# Buttons
generate_pass_btn = ctk.CTkButton(app, text="Generate Password", command=lambda: generate_password(password_input))
generate_pass_btn.grid(row=4, column=1, pady=10, padx=10)

save_pass_btn = ctk.CTkButton(app, text="Save Password", command=save_password)
save_pass_btn.grid(row=5, column=1, pady=10, padx=10)

app.mainloop()
