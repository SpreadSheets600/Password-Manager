import pyperclip
import re
import sys
import customtkinter as ctk
from DataBase import Database
from tkinter import messagebox
from Utilities import generate_password

MASTER_PASSWORD = "password"

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

ctk.set_widget_scaling(1.0)  # Set the widget scaling to a neutral value.
ctk.set_window_scaling(1.0)  # Set window scaling.

db = Database()

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$'
    return re.match(pattern, email) is not None

def is_valid_username(username):
    return username.isalnum() or '_' in username or '.' in username

class MasterPasswordWindow(ctk.CTk):
    """This window prompts for the master password and controls access to the main PasswordManagerApp."""

    def __init__(self):
        super().__init__()
        self.title("Master Password")
        self.geometry("400x200")

        self.after_id = None  # To keep track of any pending 'after' calls

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.label = ctk.CTkLabel(self.frame, text="Enter Master Password", font=ctk.CTkFont(size=16, weight="bold"))
        self.label.pack(pady=(20, 10))

        self.password_entry = ctk.CTkEntry(self.frame, show="*", placeholder_text="Master Password", width=300)
        self.password_entry.pack(pady=10)

        self.submit_button = ctk.CTkButton(self.frame, text="Submit", command=self.check_password)
        self.submit_button.pack(padx=20, pady=10)

        self.bind("<Return>", lambda event: self.check_password())  # Bind Enter key to submit
    
    def check_password(self):
        """Check if the entered password matches the master password."""
        entered_password = self.password_entry.get()
        print(f"Entered password: {entered_password}")  # Debugging statement
        if entered_password == MASTER_PASSWORD:
            print("Password correct! Opening main app...")  # Debugging statement
            self.open_password_manager()  # Open main app first
        else:
            print("Incorrect password!")  # Debugging statement
            messagebox.showerror("Error", "Incorrect master password. Please try again.")

    def open_password_manager(self):
        """Open the main Password Manager app and close the master password window."""
        self.withdraw()  # Hide the master password window
        app = PasswordManagerApp()  # Create the password manager app
        app.mainloop()  # Start the main loop of the PasswordManagerApp
        self.destroy()  # Safely destroy the master password window after the main app closes
        
class PasswordManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Password Manager")
        self.geometry("900x600")
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Password Manager", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = ctk.CTkButton(self.sidebar_frame, text="Add New Password", command=self.add_password_form)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.sidebar_button_2 = ctk.CTkButton(self.sidebar_frame, text="View Passwords", command=self.view_passwords)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        self.sidebar_button_3 = ctk.CTkButton(self.sidebar_frame, text="Search Passwords", command=self.search_passwords)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                            command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        self.add_password_form()
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        """Handle the window close event."""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.quit()  # Exit the mainloop
            sys.exit()
        
    def change_appearance_mode(self, mode):
        ctk.set_appearance_mode(mode)

    def add_password_form(self, pw_data=None):
        self.clear_content_frame()

        form_frame = ctk.CTkFrame(self.content_frame)
        form_frame.pack(expand=True, fill="both", padx=20, pady=20)

        ctk.CTkLabel(form_frame, text="Add New Password" if pw_data is None else "Edit Password", font=ctk.CTkFont(size=25, weight="bold")).pack(pady=(0, 20))

        fields = [("Website", "website"), ("Email", "email"), ("Username", "username"), ("Password", "password")]
        self.entry_widgets = {}

        for label, attr in fields:
            ctk.CTkLabel(form_frame, text=label).pack(anchor="w", padx=5, pady=(10, 0))
            entry = ctk.CTkEntry(form_frame, width=300)
            entry.pack(pady=(0, 10), padx=5, fill="x")
            self.entry_widgets[attr] = entry

        button_frame = ctk.CTkFrame(form_frame)
        button_frame.pack(fill="x", pady=(20, 0))

        if pw_data is None:
            ctk.CTkButton(button_frame, text="Generate Password", command=self.generate_password).pack(side="left", padx=(0, 10))
            ctk.CTkButton(button_frame, text="Save Password", command=self.save_password).pack(side="left")
        else:
            ctk.CTkButton(button_frame, text="Update Password", command=lambda: self.update_password(pw_data)).pack(side="left")
        
        if pw_data:
            self.entry_widgets["website"].insert(0, pw_data[0])
            self.entry_widgets["email"].insert(0, pw_data[1])
            self.entry_widgets["username"].insert(0, pw_data[2])
            self.entry_widgets["password"].insert(0, pw_data[3])


    def generate_password(self):
        data = {key: widget.get() for key, widget in self.entry_widgets.items()}
        if not data['username']:
            messagebox.showwarning("Warning", "Please fill username for customized password!")
            return
        
        last_word = data['username'].split()[-1] 
        password = generate_password(min_length=10)  # Password generation

        # Removed strength check
        self.entry_widgets["password"].delete(0, ctk.END)
        self.entry_widgets["password"].insert(0, last_word + password)


    def save_password(self):
        data = {key: widget.get() for key, widget in
