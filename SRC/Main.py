import re
import csv
import sys
import pyperclip
import customtkinter as ctk
from DataBase import Database
from functools import partial
from tkinter import messagebox as msgbox
from Utilities import generate_password, password_strength

MASTER_PASSWORD = "password"

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

ctk.set_widget_scaling(1.0)
ctk.set_window_scaling(1.0)
db = Database()


def is_valid_email(email):
    if not email:
        return True
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$"
    return re.match(pattern, email) is not None


def is_valid_username(username):
    if not username:
        return True
    return username.isalnum() or "_" in username or "." in username


class MasterPasswordWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Master Password")
        self.geometry("400x200")

        self.after_id = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.label = ctk.CTkLabel(
            self.frame,
            text="Enter Master Password",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.label.pack(pady=(20, 10))

        self.password_entry = ctk.CTkEntry(
            self.frame, show="*", placeholder_text="Master Password", width=300
        )
        self.password_entry.pack(pady=10)

        self.submit_button = ctk.CTkButton(
            self.frame, text="Submit", command=self.check_password
        )
        self.submit_button.pack(padx=20, pady=10)

        self.bind("<Return>", lambda event: self.check_password())

    def check_password(self):
        entered_password = self.password_entry.get()
        print(f"Entered Password : {entered_password}")
        if entered_password == MASTER_PASSWORD:
            print("Password Correct! Opening Main App...")
            self.open_password_manager()
        else:
            print("Incorrect password!")
            msgbox.showerror("Error", "Incorrect Master Password. Please Try Again.")

    def open_password_manager(self):

        self.withdraw()
        app = PasswordManagerApp()
        app.mainloop()
        self.destroy()


class PasswordManagerApp(ctk.CTk):

    ITEMS_PER_PAGE = RESULTS_PER_PAGE = 10

    def __init__(self):
        super().__init__()
        self.title("Password Manager")
        self.geometry("900x600")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="Password Manager",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = ctk.CTkButton(
            self.sidebar_frame, text="Add New Password", command=self.add_password_form
        )
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.sidebar_button_2 = ctk.CTkButton(
            self.sidebar_frame, text="View Passwords", command=self.view_passwords
        )
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        self.sidebar_button_3 = ctk.CTkButton(
            self.sidebar_frame, text="Search Passwords", command=self.search_passwords
        )
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        self.sidebar_button_4 = ctk.CTkButton(
            self.sidebar_frame,
            text="Import Passwords",
            command=self.import_passwords,
        )
        self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=10)

        self.appearance_mode_label = ctk.CTkLabel(
            self.sidebar_frame, text="Appearance Mode:", anchor="w"
        )
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(
            self.sidebar_frame,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode,
        )
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        self.add_password_form()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.current_page = 0
        self.total_pages = 0

    def on_close(self):
        if msgbox.askokcancel("Quit", "Do You Want To Quit ?"):
            self.quit()
            sys.exit()

    def change_appearance_mode(self, mode):
        ctk.set_appearance_mode(mode)

    def add_password_form(self, pw_data=None):
        self.current_page = 0
        self.clear_content_frame()

        form_frame = ctk.CTkFrame(self.content_frame)
        form_frame.pack(expand=True, fill="both", padx=20, pady=20)

        ctk.CTkLabel(
            form_frame,
            text="Add New Password" if pw_data is None else "Edit Password",
            font=ctk.CTkFont(size=25, weight="bold"),
        ).pack(pady=(0, 20))

        fields = [
            ("Website", "website"),
            ("Email", "email"),
            ("Username", "username"),
            ("Password", "password"),
        ]
        self.entrywid = {}

        for label, attr in fields:
            ctk.CTkLabel(form_frame, text=label).pack(anchor="w", padx=5, pady=(10, 0))

            if attr == "password":
                self.entrywid[attr] = ctk.CTkEntry(form_frame, width=300)
                self.entrywid[attr].pack(pady=(0, 10), padx=5, fill="x")

                self.password_strng_display = ctk.CTkLabel(
                    form_frame, text="", font=ctk.CTkFont(size=10)
                )
                self.password_strng_display.pack(pady=(0, 10), padx=5, anchor="w")
            else:
                self.entrywid[attr] = ctk.CTkEntry(form_frame, width=300)
                self.entrywid[attr].pack(pady=(0, 10), padx=5, fill="x")

        button_frame = ctk.CTkFrame(form_frame)
        button_frame.pack(fill="x", pady=(20, 0))

        if pw_data is None:
            ctk.CTkButton(
                button_frame, text="Generate Password", command=self.generate_password
            ).pack(side="left", padx=(0, 10))
            ctk.CTkButton(
                button_frame, text="Save Password", command=self.save_password
            ).pack(side="left")
        else:
            ctk.CTkButton(
                button_frame,
                text="Update Password",
                command=lambda: self.update_password(pw_data),
            ).pack(side="left")

        if pw_data:
            self.entrywid["website"].insert(0, pw_data[0])
            self.entrywid["email"].insert(0, pw_data[1])
            self.entrywid["username"].insert(0, pw_data[2])
            self.entrywid["password"].insert(0, pw_data[3])

    def get_strng_color(self, strng):
        if strng == "STRONG":
            return "lime"
        elif strng == "MEDIUM":
            return "yellow"
        elif strng == "WEAK":
            return "red"
        else:
            return "gray"

    def generate_password(self):
        for widget in self.content_frame.winfo_children():
            if isinstance(widget, ctk.CTkLabel) and widget.cget("text").startswith("["):
                widget.destroy()

        data = {key: widget.get() for key, widget in self.entrywid.items()}

        if not data["username"]:
            msgbox.showwarning(
                "Missing Information", "Please fill username for customized password!"
            )
            return

        lstword = data["username"].split()[-1]
        password = generate_password()
        password = lstword + password

        self.entrywid["password"].delete(0, ctk.END)
        self.entrywid["password"].insert(0, password)

        strng = password_strength(password)
        color = self.get_strng_color(strng)

        self.password_strng_display = ctk.CTkLabel(
            self.content_frame,
            text=f"[Password Strength: {strng.upper()}]",
            text_color=color,
        )
        self.password_strng_display.pack(side="right")

    def save_password(self):
        data = {key: widget.get() for key, widget in self.entrywid.items()}

        if not all(data.values()):
            msgbox.showwarning("Missing Information", "All fields must be filled!")
        elif not is_valid_email(data["email"]):
            msgbox.showwarning(
                "Invalid Email",
                "Invalid email format. Please enter a valid email address.",
            )
        elif not is_valid_username(data["username"]):
            msgbox.showwarning(
                "Invalid Username",
                "Username can only contain alphanumeric characters, dots, or underscores.",
            )
        else:
            strng = password_strength(data["password"])

            for widget in self.content_frame.winfo_children():
                if isinstance(widget, ctk.CTkLabel) and widget.cget("text").startswith(
                    "["
                ):
                    widget.destroy()

            color = self.get_strng_color(strng)
            self.password_strng_display = ctk.CTkLabel(
                self.content_frame,
                text=f"[Password Strength: {strng.upper()}]",
                text_color=color,
            )
            self.password_strng_display.pack(side="right")

            msgbox.showinfo(
                "Password Strength", f"The strength of your password is: {strng}"
            )

            if strng == "WEAK":
                res = msgbox.askyesno(
                    "Warning",
                    "You are saving a WEAK password. Do you want to continue?",
                )
                if not res:
                    return

            try:
                db.save_data(**data)
                for widget in self.entrywid.values():
                    widget.delete(0, ctk.END)
                self.password_strng_display.destroy()
                msgbox.showinfo("Success", "Password saved successfully!")
            except Exception as e:
                msgbox.showerror("Error", f"Failed to save password: {e}")

    def view_passwords(self):
        self.clear_content_frame()

        ctk.CTkLabel(
            self.content_frame,
            text="Saved Passwords",
            font=ctk.CTkFont(size=25, weight="bold"),
        ).pack(pady=(0, 20))

        scrollable_frame = ctk.CTkScrollableFrame(self.content_frame)
        scrollable_frame.pack(expand=True, fill="both", padx=20, pady=20)

        passwords = db.get_all_passwords()
        total_items = self.display_passwords(
            passwords, self.current_page, scrollable_frame, paginated=True
        )

        self.total_pages = (total_items - 1) // self.ITEMS_PER_PAGE + 1

        pagination_frame = ctk.CTkFrame(self.content_frame)
        pagination_frame.pack(fill="x", padx=20, pady=20)

        self.setup_pagination(
            total_items,
            pagination_frame,
            self.current_page,
            self.total_pages,
            self.next_page,
            self.prev_page,
        )

    def next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.view_passwords()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.view_passwords()

    def search_passwords(self):
        self.clear_content_frame()

        ctk.CTkLabel(
            self.content_frame,
            text="Search Passwords",
            font=ctk.CTkFont(size=25, weight="bold"),
        ).pack(pady=(0, 20))

        search_frame = ctk.CTkFrame(self.content_frame)
        search_frame.pack(fill="x", padx=20, pady=20)

        self.search_entry = ctk.CTkEntry(
            search_frame, width=300, placeholder_text="Enter Website Name Or Email"
        )
        self.search_entry.pack(side="left", padx=(0, 10))

        ctk.CTkButton(search_frame, text="Search", command=self.perform_search).pack(
            side="left"
        )

        self.search_results_frame = ctk.CTkScrollableFrame(self.content_frame)
        self.search_results_frame.pack(expand=True, fill="both", padx=20, pady=(0, 20))

        self.pagination_frame = ctk.CTkFrame(self.content_frame)
        self.pagination_frame.pack(fill="x", padx=20, pady=(0, 20))

    def perform_search(self):
        query = self.search_entry.get()
        if not query:
            msgbox.showwarning("Warning", "Please Enter A Search Query!")
            return

        self.search_results = db.search_passwords(query)
        self.current_page = 0

        if not self.search_results:
            ctk.CTkLabel(
                self.search_results_frame, text="No Matching Passwords Found."
            ).pack(pady=20)
        else:
            total_items = self.display_passwords(
                self.search_results,
                self.current_page,
                self.search_results_frame,
                paginated=True,
            )
            self.total_pages = (total_items - 1) // self.RESULTS_PER_PAGE + 1

            self.setup_pagination(
                total_items,
                self.pagination_frame,
                self.current_page,
                self.total_pages,
                self.next_page,
                self.prev_page,
            )

    def display_passwords(self, passwords, page, frame, paginated=True):

        for widget in frame.winfo_children():
            widget.destroy()

        total_items = len(passwords)
        if paginated:
            total_pages = (total_items - 1) // self.ITEMS_PER_PAGE + 1
            start_idx = (page) * self.ITEMS_PER_PAGE
            end_idx = start_idx + self.ITEMS_PER_PAGE
            passwords_to_display = passwords[start_idx:end_idx]
        else:
            passwords_to_display = passwords

        if not passwords_to_display:
            ctk.CTkLabel(frame, text="No Saved Passwords Found.").pack(pady=20)
        else:
            for i, (website, email, username, password) in enumerate(
                passwords_to_display, start=start_idx + 1
            ):
                password_frame = ctk.CTkFrame(frame)
                password_frame.pack(fill="x", padx=5, pady=5)

                ctk.CTkLabel(
                    password_frame,
                    text=f"{i}. {website}",
                    font=ctk.CTkFont(weight="bold"),
                ).grid(row=0, column=0, sticky="w", padx=5, pady=2)
                ctk.CTkLabel(password_frame, text=f"Email: {email}").grid(
                    row=1, column=0, sticky="w", padx=5, pady=2
                )
                ctk.CTkLabel(password_frame, text=f"Username : {username}").grid(
                    row=2, column=0, sticky="w", padx=5, pady=2
                )

                password_label = ctk.CTkLabel(
                    password_frame, text="Password : ********"
                )
                password_label.grid(row=3, column=0, sticky="w", padx=5, pady=2)

                show_button = ctk.CTkButton(password_frame, text="Show", width=60)
                show_button.grid(row=3, column=5, padx=5, pady=2)
                show_button.configure(
                    command=partial(
                        self.toggle_password, password, password_label, show_button
                    )
                )

                ctk.CTkButton(
                    password_frame,
                    text="Edit",
                    width=60,
                    command=lambda pw_data=(
                        website,
                        email,
                        username,
                        password,
                    ): self.edit_password(pw_data),
                ).grid(row=0, column=5, padx=5, pady=2)

                ctk.CTkButton(
                    password_frame,
                    text="Copy",
                    width=60,
                    command=lambda p=password: self.copy_to_clipboard(p),
                ).grid(row=1, column=5, padx=5, pady=2)

                ctk.CTkButton(
                    password_frame,
                    text="Delete",
                    width=60,
                    command=lambda pw_data=(
                        website,
                        email,
                        username,
                        password,
                    ): self.delete_password(pw_data),
                ).grid(
                    row=2,
                    column=5,
                    padx=5,
                    pady=2,
                )

        return total_items

    def setup_pagination(
        self, total_items, frame, current_page, total_pages, next_command, prev_command
    ):
        for widget in frame.winfo_children():
            widget.destroy()

        pagination_frame = ctk.CTkFrame(frame)
        pagination_frame.pack(pady=10)

        prev_button = ctk.CTkButton(
            pagination_frame,
            text="Previous",
            command=prev_command,
            state="disabled" if current_page == 0 else "normal",
        )
        prev_button.pack(side="left", padx=(0, 10))

        page_label = ctk.CTkLabel(
            pagination_frame,
            text=f"Page {current_page + 1} Of {total_pages}",
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        page_label.pack(side="left", padx=(0, 10))

        next_button = ctk.CTkButton(
            pagination_frame,
            text="Next",
            command=next_command,
            state="disabled" if current_page >= total_pages - 1 else "normal",
        )
        next_button.pack(side="left", padx=(10, 0))

    def import_passwords(self):
        self.current_page = 0
        self.clear_content_frame()

        ctk.CTkLabel(
            self.content_frame,
            text="Import Passwords From Google",
            font=ctk.CTkFont(size=25, weight="bold"),
        ).pack(pady=(0, 20))

        import_frame = ctk.CTkFrame(self.content_frame)
        import_frame.pack(fill="x", padx=20, pady=20)

        ctk.CTkButton(
            import_frame, text="Select CSV File", command=self.select_csv_file
        ).pack(pady=10)

    def select_csv_file(self):
        file_path = ctk.filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.import_csv(file_path)

    def import_csv(self, file_path):
        passwords = db.get_all_passwords()
        websites_hashmap = {}
        if passwords:
            for website, email, username, password in passwords:
                websites_hashmap[website] = (email, username, password)

        try:
            with open(file_path, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    name = row.get("\ufeffname", "").strip()
                    if not name:
                        row.get("name", "").strip()

                    url = row.get("url", "").strip()
                    username = row.get("username", "").strip()
                    password = row.get("password", "").strip()

                    email = username
                    if not username.endswith(".com"):
                        email = "No Email Provided"

                    if url and username and password:

                        if url in websites_hashmap:
                            should_save = msgbox.askyesno(
                                "Duplicate Entry",
                                f"A Passeord For {url} Already Exists. Do You Want To Save This Password?",
                            )

                            if not should_save:
                                continue

                        db.save_data(url, email, username, password)
                    else:
                        print(f"Failed To Save Password For {name}")

            msgbox.showinfo("Success", "Passwords Imported Sucessfully!")
            self.view_passwords()
        except Exception as e:
            msgbox.showerror("Error", f"Failed To Import Passwords: {e}")

    def toggle_password(self, password, label, button):
        if label.cget("text") == "Password : ********":
            label.configure(text=f"Password : {password}")
            button.configure(text="Hide")
        else:
            label.configure(text="Password : ********")
            button.configure(text="Show")

    def edit_password(self, pw_data):
        self.add_password_form(pw_data)

    def update_password(self, old_data):
        new_data = {key: widget.get() for key, widget in self.entrywid.items()}

        if not all(new_data.values()):
            msgbox.showwarning("Missing Information", "All fields must be filled!")
        elif not is_valid_email(new_data["email"]):
            msgbox.showwarning(
                "Invalid Email",
                "Invalid email format. Please enter a valid email address.",
            )
        elif not is_valid_username(new_data["username"]):
            msgbox.showwarning(
                "Invalid Username",
                "Username can only contain alphanumeric characters, dots, or underscores.",
            )
        else:
            try:
                db.update_password(old_data, new_data)
                self.clear_entries()
                msgbox.showinfo("Success", "Password Updated Successfully!")
                self.view_passwords()
            except Exception as e:
                msgbox.showerror("Error", f"Failed To Update Password : {e}")

    def delete_password(self, pw_data):
        if msgbox.askyesno(
            "Delete Password", "Are You Sure You Want To Delete This Password?"
        ):
            try:
                db.delete_password(pw_data)
                msgbox.showinfo("Success", "Password Deleted Successfully!")
                self.view_passwords()
            except Exception as e:
                msgbox.showerror("Error", f"Failed To Delete Password: {e}")

    def copy_to_clipboard(self, password):
        pyperclip.copy(password)
        msgbox.showinfo("Copied", "Password Copied To Clipboard!")

    def clear_entries(self):
        for entry in self.entrywid.values():
            entry.delete(0, ctk.END)

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    master_password_window = MasterPasswordWindow()
    master_password_window.mainloop()
