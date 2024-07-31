import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import re
import cashier_app

def create_user(username, password, email):
    with mysql.connector.connect(
        host="127.0.0.1", database="grocery_store", user="root", password="ADXXSTAR$"
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO User_info (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
            connection.commit()
    messagebox.showinfo("Sign-Up", "User created successfully!")

def authenticate_user(username, password):
    with mysql.connector.connect(
        host="127.0.0.1", database="grocery_store", user="root", password="ADXXSTAR$"
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT password FROM User_info WHERE username = %s", (username,))
            result = cursor.fetchone()
    return result and result[0] == password

def validate_email(email):
    return re.match(r'^[a-zA-Z0-9._%+-]+@(gmail\.com|outlook\.com|duck\.com)$', email) is not None

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login or Sign-Up")
        self.root.geometry("2106x1199")
        self.root.resizable(True, True)
        self.set_background_image()
        self.create_frame()
        self.create_widgets()

    def set_background_image(self):
        bg_image_path = "LG PAGE.png"
        bg_image = Image.open(bg_image_path).resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(bg_image)
        tk.Label(self.root, image=self.bg_image).place(relwidth=1, relheight=1)

    def create_frame(self):
        self.frame = ctk.CTkFrame(self.root, fg_color="white", border_width=2)
        self.frame.place(relx=0.6, rely=0.63, anchor=tk.CENTER, relwidth=0.5, relheight=0.63)
    #   self.user_icon_path = "checkout/HELLO.jpeg"
    #   user_icon = Image.open(self.user_icon_path).resize((500,300), Image.LANCZOS)
    #   self.user_icon = ImageTk.PhotoImage(user_icon)
    #    tk.Label(self.root, image=self.user_icon, bg='white').place(relx=0.49, rely=-0.16, anchor=tk.NW)
    
    def create_widgets(self):
        ctk.CTkLabel(self.frame, text="LOGIN OR SIGN-UP", font=("Arial", 36), text_color="black").place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        self.option_var = ctk.StringVar(value="LOGIN")
        ctk.CTkOptionMenu(self.frame, variable=self.option_var, values=["LOGIN", "SIGN-UP"], command=self.change_option, font=("Arial", 24)).place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        self.create_form_fields()
        self.submit_button = ctk.CTkButton(self.frame, text="SUBMIT", command=self.submit, font=("Arial", 24)).place(relx=0.5, rely=0.7, anchor=tk.CENTER)

    def create_form_fields(self):
        self.username_label = ctk.CTkLabel(self.frame, text="Username:", text_color="black", font=("Arial", 24))
        self.username_entry = ctk.CTkEntry(self.frame, fg_color="white", border_color="black", text_color="black", font=("Arial", 24))
        self.password_label = ctk.CTkLabel(self.frame, text="Password:", text_color="black", font=("Arial", 24))
        self.password_entry = ctk.CTkEntry(self.frame, show='*', fg_color="white", border_color="black", text_color="black", font=("Arial", 24))
        self.email_label = ctk.CTkLabel(self.frame, text="Email:", text_color="black", font=("Arial", 24))
        self.email_entry = ctk.CTkEntry(self.frame, fg_color="white", border_color="black", text_color="black", font=("Arial", 24))
        self.place_form_fields()

    def place_form_fields(self):
        self.username_label.place(relx=0.2, rely=0.35)
        self.username_entry.place(relx=0.41, rely=0.38, anchor=tk.W, relwidth=0.4)
        self.password_label.place(relx=0.2, rely=0.45)
        self.password_entry.place(relx=0.41, rely=0.48, anchor=tk.W, relwidth=0.4)
        self.email_label.place(relx=0.29, rely=0.55)
        self.email_entry.place(relx=0.2, rely=0.58, anchor=tk.W, relwidth=0.4)
        self.email_label.place_forget()
        self.email_entry.place_forget()

    def change_option(self, value):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        if value == "SIGN-UP":
            self.email_label.place(relx=0.2, rely=0.55)
            self.email_entry.place(relx=0.41, rely=0.55, anchor=tk.W, relwidth=0.4)
        else:
            self.email_label.place_forget()
            self.email_entry.place_forget()

    def submit(self):
        username, password, email, option = self.username_entry.get(), self.password_entry.get(), self.email_entry.get(), self.option_var.get()
        if not (username and password):
            messagebox.showerror("Error", "Username or password cannot be empty!")
            return
        if option == "LOGIN":
            if authenticate_user(username, password):
                messagebox.showinfo("Login", f"Welcome, {username}!")
                self.root.destroy()
                self.open_cashier_app()
            else:
                messagebox.showerror("Login", "Invalid username or password!")
        elif option == "SIGN-UP" and validate_email(email):
            create_user(username, password, email)
        else:
            messagebox.showerror("Sign-Up", "Invalid email address!")

    def open_cashier_app(self):
        cashier_root = ctk.CTk()
        app = cashier_app.GroceryStore(cashier_root)
        cashier_root.geometry("1000x500")
        cashier_root.mainloop()

if __name__ == "__main__":
    root = ctk.CTk()
    app = LoginApp(root)
    root.mainloop()
