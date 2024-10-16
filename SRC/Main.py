import customtkinter as ctk
from DataBase import Database
from tkinter import messagebox
from Utilities import generate_password

ctk.set_appearance_mode("Dark")  # Modes: "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

# Database Instance
db = Database()

class PasswordManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Password Manager")
        self.geometry("800x600")
        
# ----------------------- UI ----------------------- #

        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Password Manager", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = ctk.CTkButton(self.sidebar_frame, text="Add New Password", command=self.add_password_form)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.sidebar_button_2 = ctk.CTkButton(self.sidebar_frame, text="View Passwords", command=self.view_passwords)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                            command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=0, column=1, sticky="nsew")

        self.add_password_form()

    # Change Appearance Mode
    def change_appearance_mode(self, mode):
        ctk.set_appearance_mode(mode)

    # Change Scaling
    def change_scaling_event(self, scaling):
        scale = int(scaling.strip('%')) / 100
        self.tk.call('tk', 'scaling', scale)

    # Form To Add New Password
    def add_password_form(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Website Input
        website_label = ctk.CTkLabel(self.content_frame, text="Website:")
        website_label.pack(pady=5)
        global website_input
        website_input = ctk.CTkEntry(self.content_frame, width=300)
        website_input.pack(pady=5)

        # Email Input
        email_label = ctk.CTkLabel(self.content_frame, text="Email:")
        email_label.pack(pady=5)
        global email_input
        email_input = ctk.CTkEntry(self.content_frame, width=300)
        email_input.pack(pady=5)

        # Username Input
        username_label = ctk.CTkLabel(self.content_frame, text="Username:")
        username_label.pack(pady=5)
        global username_input
        username_input = ctk.CTkEntry(self.content_frame, width=300)
        username_input.pack(pady=5)

        # Password Input
        password_label = ctk.CTkLabel(self.content_frame, text="Password:")
        password_label.pack(pady=5)
        global password_input
        password_input = ctk.CTkEntry(self.content_frame, width=300)
        password_input.pack(pady=5)

        # Buttons
        generate_pass_btn = ctk.CTkButton(self.content_frame, text="Generate Password", command=lambda: generate_password(password_input))
        generate_pass_btn.pack(pady=10)

        save_pass_btn = ctk.CTkButton(self.content_frame, text="Save Password", command=self.save_password)
        save_pass_btn.pack(pady=10)

# ----------------------- Save Password ----------------------- #

    def save_password(self):
        website = website_input.get()
        email = email_input.get()
        username = username_input.get()
        password = password_input.get()

        if not website or not email or not password:
            messagebox.showwarning("Warning", "All fields must be filled!")
        else:
            try:
                db.save_data(website, email, username, password)
                website_input.delete(0, ctk.END)
                email_input.delete(0, ctk.END)
                username_input.delete(0, ctk.END)
                password_input.delete(0, ctk.END)
                messagebox.showinfo("Success", "Password saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save password: {e}")

# ----------------------- View Passwords ----------------------- #

    def view_passwords(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        scrollable_frame = ctk.CTkScrollableFrame(self.content_frame, width=500, height=400)
        scrollable_frame.pack(pady=10, padx=10)

        passwords = db.get_all_passwords()
        if not passwords:
            no_data_label = ctk.CTkLabel(scrollable_frame, text="No saved passwords.")
            no_data_label.pack(pady=20)
        else:
            for i, (website, email, username, password) in enumerate(passwords):
                pass_label = ctk.CTkLabel(scrollable_frame, text=f"{i+1}. {website} | {email} | {username} | {password}")
                pass_label.pack(pady=5)

if __name__ == "__main__":
    app = PasswordManagerApp()
    app.mainloop()
