import customtkinter as ctk
from tkinter import messagebox, Toplevel
import sqlite3


class DatabaseHandler:
    def __enter__(self):
        self.connection = sqlite3.connect("Hospital.db")
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()


class WelcomeFrame(ctk.CTkFrame):
    def __init__(self, master, username):
        super().__init__(master)
        self.username = username
        self.create_widgets()

    def create_widgets(self):
        self.welcome_label = ctk.CTkLabel(self, text=f"Welcome, {self.username}!")

        # Create buttons for different roles
        roles = ["Doctor", "Patient", "Nurse", "Ward Boy"]
        for i, role in enumerate(roles):
            button_role = ctk.CTkButton(
                self,
                text=f"{role} System",
                command=lambda r=role: self.open_role_page(r),
            )
            button_role.grid(row=i // 2, column=i % 2, padx=10, pady=10, sticky="nsew")

        self.welcome_label.grid(
            row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew"
        )

        # Configure column and row weights for responsiveness
        for i in range(2):
            self.columnconfigure(i, weight=1)
        for i in range(3):
            self.rowconfigure(i, weight=1)

    def open_role_page(self, role):
        role_page = RolePage(self, role)
        role_page.geometry("800x200")
        role_page.configure(bg="#2b2b2b")  # Set the background color to black


class RolePage(Toplevel):
    def __init__(self, master, role):
        super().__init__(master)
        self.role = role
        self.create_widgets()

    def create_widgets(self):
        label_role = ctk.CTkLabel(self, text=f"{self.role} System")
        button_update = ctk.CTkButton(self, text="Update", command=self.update_clicked)
        button_delete = ctk.CTkButton(self, text="Delete", command=self.delete_clicked)
        button_add = ctk.CTkButton(self, text="Add", command=self.add_clicked)
        button_show_database = ctk.CTkButton(
            self, text="Show Database", command=self.show_database_clicked
        )

        label_role.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        button_update.grid(row=1, column=0, padx=10, pady=10)
        button_delete.grid(row=1, column=1, padx=10, pady=10)
        button_add.grid(row=1, column=2, padx=10, pady=10)
        button_show_database.grid(row=1, column=3, padx=10, pady=10)

        for i in range(4):
            self.columnconfigure(i, weight=1)

    def update_clicked(self):
        print(f"Updating {self.role} record")

    def delete_clicked(self):
        print(f"Deleting {self.role} record")

    def add_clicked(self):
        print(f"Adding {self.role} record")

    def show_database_clicked(self):
        print(f"Showing {self.role} database")


class LoginSystem(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login System")
        self.geometry("300x200")

        self.login_frame = ctk.CTkFrame(self)
        self.welcome_frame = WelcomeFrame(self, "")

        self.create_login_widgets()
        self.create_welcome_widgets()

        self.show_login_frame()

    def create_login_widgets(self):
        label_username = ctk.CTkLabel(self.login_frame, text="Username:")
        label_password = ctk.CTkLabel(self.login_frame, text="Password:")
        self.entry_username = ctk.CTkEntry(self.login_frame)
        self.entry_password = ctk.CTkEntry(self.login_frame, show="*")
        button_login = ctk.CTkButton(
            self.login_frame, text="Login", command=self.login_clicked
        )

        label_username.grid(row=0, column=0, padx=10, pady=10)
        self.entry_username.grid(row=0, column=1, padx=10, pady=10)
        label_password.grid(row=1, column=0, padx=10, pady=10)
        self.entry_password.grid(row=1, column=1, padx=10, pady=10)
        button_login.grid(row=2, column=0, columnspan=2, pady=10)

    def create_welcome_widgets(self):
        self.welcome_frame = WelcomeFrame(self, "")

    def authenticate_user(self, username, password):
        try:
            with DatabaseHandler() as cursor:
                cursor.execute(
                    "SELECT * FROM Auth WHERE login=? AND password=?",
                    (username, password),
                )
                user = cursor.fetchone()

            return user is not None

        except sqlite3.Error as e:
            print(f"SQLite Error: {e}")
            return False

    def login_clicked(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if self.authenticate_user(username, password):
            self.show_welcome_frame(username)
        else:
            messagebox.showerror("Login Error", "Incorrect username or password")

    def sign_out_clicked(self):
        self.show_login_frame()

    def show_login_frame(self):
        self.login_frame.pack()
        self.welcome_frame.pack_forget()
        self.geometry("300x200")

    def show_welcome_frame(self, username):
        self.login_frame.pack_forget()
        self.welcome_frame.username = username
        self.welcome_frame.welcome_label.configure(text=f"Welcome, {username}!")
        self.welcome_frame.pack()
        self.geometry("300x150")


if __name__ == "__main__":
    login_system = LoginSystem()
    login_system.mainloop()
