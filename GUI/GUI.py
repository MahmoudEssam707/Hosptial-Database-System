import tkinter as tk
from tkinter import messagebox
import sqlite3


class LoginSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login System")
        self.geometry("300x200")  # Set initial geometry for the login frame

        self.login_frame = tk.Frame(self)
        self.welcome_frame = tk.Frame(self)

        self.create_login_widgets()
        self.create_welcome_widgets()

        self.show_login_frame()

    def create_login_widgets(self):
        label_username = tk.Label(self.login_frame, text="Username:")
        label_password = tk.Label(self.login_frame, text="Password:")
        self.entry_username = tk.Entry(self.login_frame)
        self.entry_password = tk.Entry(self.login_frame, show="*")
        button_login = tk.Button(self.login_frame, text="Login", command=self.login_clicked)

        label_username.grid(row=0, column=0, padx=10, pady=10)
        self.entry_username.grid(row=0, column=1, padx=10, pady=10)
        label_password.grid(row=1, column=0, padx=10, pady=10)
        self.entry_password.grid(row=1, column=1, padx=10, pady=10)
        button_login.grid(row=2, column=0, columnspan=2, pady=10)

    def create_welcome_widgets(self):
        self.welcome_label = tk.Label(self.welcome_frame, text="")
        button_sign_out = tk.Button(self.welcome_frame, text="Sign Out", command=self.sign_out_clicked)

        self.welcome_label.grid(row=0, column=0, padx=10, pady=10)
        button_sign_out.grid(row=1, column=0, padx=10, pady=10)

    def authenticate_user(self, username, password):
        try:
            # Connect to the database
            connection = sqlite3.connect("hospital.db")
            cursor = connection.cursor()

            # Execute SQL query to check user credentials
            cursor.execute(
                f"SELECT * FROM Auth WHERE login='{username}' AND password='{password}'"
            )
            user = cursor.fetchone()

            # Close the database connection
            connection.close()

            return user is not None

        except Exception as e:
            print(f"Error: {e}")
            return False

    def login_clicked(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if self.authenticate_user(username, password):
            self.show_welcome_frame(username)
        else:
            messagebox.showerror("Login Error", "You have written something wrong")

    def sign_out_clicked(self):
        self.show_login_frame()

    def show_login_frame(self):
        self.login_frame.pack()
        self.welcome_frame.pack_forget()
        self.geometry("300x200")

    def show_welcome_frame(self, username):
        self.login_frame.pack_forget()
        self.welcome_label.config(text=f"Welcome, {username}!")
        self.welcome_frame.pack()
        self.geometry("800x600")


if __name__ == "__main__":
    login_system = LoginSystem()
    login_system.mainloop()