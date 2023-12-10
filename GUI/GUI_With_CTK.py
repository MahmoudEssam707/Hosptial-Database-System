import customtkinter as ctk
from tkinter import messagebox
import sqlite3


class DatabaseHandler:
    def __enter__(self):
        self.connection = sqlite3.connect("Hospital.db")
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()


class LoginSystem(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login System")
        self.geometry("300x200")  # Set initial geometry for the login frame

        self.login_frame = ctk.CTkFrame(self)
        self.welcome_frame = ctk.CTkFrame(self)

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
        self.welcome_label = ctk.CTkLabel(self.welcome_frame, text="")
        button_sign_out = ctk.CTkButton(
            self.welcome_frame, text="Sign Out", command=self.sign_out_clicked
        )

        self.welcome_label.grid(row=0, column=0, padx=10, pady=10)
        button_sign_out.grid(row=1, column=0, padx=10, pady=10)

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
        self.welcome_label.configure(text=f"Welcome, {username}!")
        self.welcome_frame.pack()
        self.geometry("800x600")


if __name__ == "__main__":
    login_system = LoginSystem()
    login_system.mainloop()
