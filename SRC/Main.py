import pyperclip
import customtkinter as ctk
from DataBase import Database
from tkinter import messagebox
from Utilities import generate_password
import re  # Import the regular expression module

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

db = Database()

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

    def change_appearance_mode(self, mode):
        ctk.set_appearance_mode(mode)

    def add_password_form(self, pw_data=None):
        self.clear_content_frame()

        form_frame = ctk.CTkFrame(self.content_frame)
        form_frame.pack(expand=True, fill="both", padx=20, pady=20)

        ctk.CTkLabel(form_frame, text="Add New Password" if pw_data is None else "Edit Password", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(0, 20))

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

    def is_valid_email(self, email):
        # Regular expression for validating an Email
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email)

    def is_valid_username(self, username):
        # Check if username is not empty and meets length requirements
        return len(username) > 0

    def save_password(self):
        data = {key: widget.get() for key, widget in self.entry_widgets.items()}
        
        if not all(data.values()):
            messagebox.showwarning("Warning", "All fields must be filled!")
            return

        if not self.is_valid_email(data["email"]):
            messagebox.showwarning("Warning", "Please enter a valid email address!")
            return

        if not self.is_valid_username(data["username"]):
            messagebox.showwarning("Warning", "Username cannot be empty!")
            return

        try:
            db.save_data(**data)
            for widget in self.entry_widgets.values():
                widget.delete(0, ctk.END)
            messagebox.showinfo("Success", "Password saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save password: {e}")

    def generate_password(self):
        password = generate_password()
        self.entry_widgets["password"].delete(0, ctk.END)
        self.entry_widgets["password"].insert(0, password)

    def view_passwords(self):
        self.clear_content_frame()

        ctk.CTkLabel(self.content_frame, text="Saved Passwords", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(0, 20))

        scrollable_frame = ctk.CTkScrollableFrame(self.content_frame)
        scrollable_frame.pack(expand=True, fill="both", padx=20, pady=20)

        passwords = db.get_all_passwords()
        if not passwords:
            ctk.CTkLabel(scrollable_frame, text="No saved passwords.").pack(pady=20)
        else:
            for i, (website, email, username, password) in enumerate(passwords):
                password_frame = ctk.CTkFrame(scrollable_frame)
                password_frame.pack(fill="x", padx=5, pady=5)

                ctk.CTkLabel(password_frame, text=f"{i+1}. {website}", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", padx=5, pady=2)
                ctk.CTkLabel(password_frame, text=f"Email: {email}").grid(row=1, column=0, sticky="w", padx=5, pady=2)
                ctk.CTkLabel(password_frame, text=f"Username: {username}").grid(row=2, column=0, sticky="w", padx=5, pady=2)
                
                password_label = ctk.CTkLabel(password_frame, text="Password: ********")
                password_label.grid(row=3, column=0, sticky="w", padx=5, pady=2)

                ctk.CTkButton(password_frame, text="Show", width=60, 
                              command=lambda p=password, pl=password_label: self.toggle_password(p, pl)).grid(row=3, column=1, padx=5, pady=2)
                
                ctk.CTkButton(password_frame, text="Edit", width=60,
                              command=lambda pw_data=(website, email, username, password): self.edit_password(pw_data)).grid(row=3, column=2, padx=5, pady=2)
                
                ctk.CTkButton(password_frame, text="Copy", width=60,
                                command=lambda p=password: self.copy_to_clipboard(p)).grid(row=3, column=3, padx=5, pady=2)
                
                ctk.CTkButton(password_frame, text="Delete", width=60,
                                command=lambda pw_data=(website, email, username, password): self.delete_password(pw_data)).grid(row=3, column=4, padx=5, pady=2)

    def search_passwords(self):
        self.clear_content_frame()

        ctk.CTkLabel(self.content_frame, text="Search Passwords", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(0, 20))

        search_frame = ctk.CTkFrame(self.content_frame)
        search_frame.pack(fill="x", padx=20, pady=20)

        self.search_entry = ctk.CTkEntry(search_frame, width=300, placeholder_text="Enter website or email")
        self.search_entry.pack(side="left", padx=(0, 10))

        ctk.CTkButton(search_frame, text="Search", command=self.perform_search).pack(side="left")

        self.search_results_frame = ctk.CTkFrame(self.content_frame)
        self.search_results_frame.pack(expand=True, fill="both", padx=20, pady=(0, 20))

    def perform_search(self):
        query = self.search_entry.get()
        if not query:
            messagebox.showwarning("Warning", "Please enter a search query!")
            return

        for widget in self.search_results_frame.winfo_children():
            widget.destroy()

        results = db.search_passwords(query)
        if not results:
            ctk.CTkLabel(self.search_results_frame, text="No matching passwords found.").pack(pady=20)
        else:
            for website, email, username, password in results:
                result_frame = ctk.CTkFrame(self.search_results_frame)
                result_frame.pack(fill="x", padx=5, pady=5)

                ctk.CTkLabel(result_frame, text=f"Website: {website}", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=5, pady=2)
                ctk.CTkLabel(result_frame, text=f"Email: {email}").pack(anchor="w", padx=5, pady=2)
                ctk.CTkLabel(result_frame, text=f"Username: {username}").pack(anchor="w", padx=5, pady=2)
                
                password_label = ctk.CTkLabel(result_frame, text="Password: ********")
                password_label.pack(side="left", padx=5, pady=2)

                ctk.CTkButton(result_frame, text="Show", width=60, 
                              command=lambda p=password, pl=password_label: self.toggle_password(p, pl)).pack(side="left", padx=5, pady=2)
                
                ctk.CTkButton(result_frame, text="Copy", width=60,
                              command=lambda p=password: self.copy_to_clipboard(p)).pack(side="left", padx=5, pady=2)

    def toggle_password(self, password, label):
        if label.cget("text") == "Password: ********":
            label.configure(text=f"Password: {password}")
        else:
            label.configure(text="Password: ********")

    def edit_password(self, pw_data):
        self.add_password_form(pw_data)

    def update_password(self, old_data):
        new_data = {key: widget.get() for key, widget in self.entry_widgets.items()}
        
        if not all(new_data.values()):
            messagebox.showwarning("Warning", "All fields must be filled!")
            return

        if not self.is_valid_email(new_data["email"]):
            messagebox.showwarning("Warning", "Please enter a valid email address!")
            return

        if not self.is_valid_username(new_data["username"]):
            messagebox.showwarning("Warning", "Username cannot be empty!")
            return

        try:
            db.update_password(old_data, new_data)
            self.clear_entries()
            messagebox.showinfo("Success", "Password updated successfully!")
            self.view_passwords() 
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update password: {e}")

    def delete_password(self, pw_data):
        if messagebox.askyesno("Delete Password", "Are you sure you want to delete this password?"):
            try:
                db.delete_password(pw_data)
                messagebox.showinfo("Success", "Password deleted successfully!")
                self.view_passwords()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete password: {e}")

    def copy_to_clipboard(self, password):
        pyperclip.copy(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")

    def clear_entries(self):
        for entry in self.entry_widgets.values():
            entry.delete(0, ctk.END)

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = PasswordManagerApp()
    app.mainloop()
