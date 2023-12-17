import customtkinter as ctk
from tkinter import messagebox, Toplevel, filedialog
import sqlite3


class DatabaseHandler:
    def __init__(self, database_path=""):
        self.database_path = database_path

    def __enter__(self):
        self.connection = sqlite3.connect(self.database_path)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()


class WelcomeFrame(ctk.CTkFrame):
    def __init__(self, master, username):
        super().__init__(master)
        self.username = username
        self.create_widgets()

    def sign_out_clicked(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.create_widgets()
        self.master.show_login_frame()

    def create_widgets(self):
        self.welcome_label = ctk.CTkLabel(self, text=f"Welcome, {self.username}!")

        return_button = ctk.CTkButton(
            self,
            text="Sign Out",
            command=self.sign_out_clicked,
        )

        self.welcome_label.grid(
            row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew"
        )
        return_button.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        for i in range(2):
            self.columnconfigure(i, weight=1)


class LoginSystem(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hospital Managment System")
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
        button_select_db = ctk.CTkButton(
            self.login_frame, text="Select Database", command=self.select_database
        )

        label_username.grid(row=0, column=0, padx=10, pady=10)
        self.entry_username.grid(row=0, column=1, padx=10, pady=10)
        label_password.grid(row=1, column=0, padx=10, pady=10)
        self.entry_password.grid(row=1, column=1, padx=10, pady=10)
        button_login.grid(row=2, column=0, columnspan=2, pady=10)
        button_select_db.grid(row=3, column=0, columnspan=2, pady=10)

    def create_welcome_widgets(self):
        self.welcome_frame = WelcomeFrame(self, "")

    def authenticate_user(self, username, password):
        try:
            with DatabaseHandler(self.database_path) as cursor:
                cursor.execute(
                    "SELECT * FROM Auth WHERE ID=? AND Password=?",
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

    def show_login_frame(self):
        self.login_frame.pack()
        self.welcome_frame.pack_forget()
        self.geometry("300x200")

    def show_welcome_frame(self, username):
        self.login_frame.pack_forget()
        self.welcome_frame.username = username
        self.welcome_frame.welcome_label.configure(text=f"Welcome, {username}!")
        self.welcome_frame.pack()
        self.geometry("350x250")

    def select_database(self):
        file_path = filedialog.askopenfilename(
            title="Select Database",
            filetypes=[("SQLite Database", "*.db"), ("All files", "*.*")],
        )
        if file_path:
            self.database_path = file_path
            messagebox.showinfo("Database Selected", f"Database path: {file_path}")


if __name__ == "__main__":
    login_system = LoginSystem()
    login_system.mainloop()
