import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
import mysql.connector
from tkinter import simpledialog

class GroceryStore:
    def __init__(self, root):
        self.root = root
        self.root.title("Groceria")

        # Set appearance mode for Dark Mode
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.create_gui()

    def create_gui(self):
        # Create a frame to hold other widgets
        self.frame = ctk.CTkFrame(self.root, corner_radius=0)
        self.frame.pack(fill="both", expand=True)

        # Create scroll bars
        self.xscroll = ctk.CTkScrollbar(self.frame, orientation="horizontal")
        self.yscroll = ctk.CTkScrollbar(self.frame, orientation="vertical")

        # Style the Treeview to match customtkinter theme
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#D3D3D3",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="#D3D3D3")
        style.map('Treeview',
                  background=[('selected', '#ADD8E6')],
                  foreground=[('selected', 'black')])

        # Create record table
        self.table = ttk.Treeview(self.frame, style="Treeview")

        # Configure scroll bars
        self.xscroll.configure(command=self.table.xview)
        self.yscroll.configure(command=self.table.yview)
        self.table.config(
            yscrollcommand=self.yscroll.set,
            xscrollcommand=self.xscroll.set,
            selectmode="extended",
        )

        # Column configurations
        columns = (
            "Product ID", "Product Name", "Category", "Brand", "Price",
            "Stock Quantity", "Supplier", "Expiry Date", "Discount", "Location",
        )
        self.table["columns"] = columns
        self.table["show"] = "headings"

        for col in columns:
            self.table.heading(col, text=col, anchor=tk.CENTER)
            self.table.column(col, width=150)
            self.table.heading(col, command=lambda _col=col: self.sort_by(_col, 0))

        # Add tooltips
        self.add_tooltips()

        self.populate_table()

        self.table.pack(fill="both", expand=True)
        self.xscroll.pack(side="bottom", fill="x")
        self.yscroll.pack(side="right", fill="y")

        # Advanced Search Entry and Button
        search_frame = ctk.CTkFrame(self.frame)
        search_frame.pack(pady=10)

        self.search_var = tk.StringVar()
        search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var, width=200)
        search_button = ctk.CTkButton(search_frame, text="Search", command=self.search_table)

        search_entry.grid(row=0, column=0, padx=10)
        search_button.grid(row=0, column=1)

        # User Authentication
        self.authenticate_user()

        # User Manual and Contextual Help
        self.create_user_manual()
        self.create_contextual_help()

    def add_tooltips(self):
        tooltips = {
            "Product ID": "The unique identifier for each product.",
            "Product Name": "The name of the product.",
            "Category": "The category to which the product belongs.",
            "Brand": "The brand of the product.",
            "Price": "The price of the product.",
            "Stock Quantity": "The available quantity of the product in stock.",
            "Supplier": "The supplier of the product.",
            "Expiry Date": "The expiration date of the product.",
            "Discount": "Any discount applied to the product.",
            "Location": "The location where the product is stored.",
        }
        for col in self.table["columns"]:
            self.table.heading(col, text=col, anchor=tk.CENTER)
            self.table.heading(col, command=lambda _col=col: self.show_tooltip(tooltips[_col]))

    def show_tooltip(self, text):
        messagebox.showinfo("Tooltip", text)

    def sort_by(self, col, descending):
        data = [(self.table.set(child, col), child) for child in self.table.get_children()]
        data.sort(reverse=descending)
        for index, (_, item) in enumerate(data):
            self.table.move(item, '', index)
        self.table.heading(col, command=lambda: self.sort_by(col, int(not descending)))

    def populate_table(self):
        count = 0
        self.table.tag_configure("oddrow", background="#e8e8e8")
        self.table.tag_configure("evenrow", background="white")
        self.table.tag_configure("specialcolor", background="#FFDDC1")

        try:
            connection = mysql.connector.connect(
                host="localhost",
                database="grocery_store",
                user="root",
                password="ADXXSTAR$"
            )

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM inventory")
                data = cursor.fetchall()

                for record in data:
                    tag = "evenrow" if count % 2 == 0 else "oddrow"
                    if 'Special' in record[1]:
                        tag = "specialcolor"
                    
                    self.table.insert(
                        parent="",
                        index="end",
                        iid=count,
                        text=count,
                        values=record,
                        tags=(tag,),
                    )
                    count += 1
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if connection.is_connected():
                connection.close()

    def search_table(self):
        search_term = self.search_var.get().strip().lower()
        if not search_term:
            messagebox.showinfo("Search Result", "Empty search")
            return

        found = False

        # Reset row backgrounds
        for row in self.table.get_children():
            tags = self.table.item(row, 'tags')
            background = "#e8e8e8" if 'oddrow' in tags else "white"
            if 'specialcolor' in tags:
                background = "#FFDDC1"
            self.table.item(row, tags=tags)
            self.table.tag_configure(tags[0], background=background)

        # Highlight matching rows
        for row in self.table.get_children():
            values = self.table.item(row, 'values')
            if any(search_term in str(value).lower() for value in values):
                self.table.item(row, tags=("highlight",))
                self.table.tag_configure("highlight", background="#add8e6")  # Light blue
                found = True

        if found:
            messagebox.showinfo("Search Result", "Product found")
        else:
            messagebox.showinfo("Search Result", "Product not found")

    def authenticate_user(self):
        # Simple user authentication
        correct_password = "123"  # This should be securely handled in a real application
        password = simpledialog.askstring("Authentication", "Enter the password:")
        if password != correct_password:
            messagebox.showerror("Authentication Error", "Incorrect password!")
            self.root.destroy()

    def create_user_manual(self):
        manual_text = "User Manual:\n\n" \
                      "1. Use the search bar to find products.\n" \
                      "2. Click on column headers to sort the table.\n" \
                      "3. Use the scroll bars to navigate through the table.\n" \
                      "4. Contact support if you encounter any issues."
        self.user_manual_button = ctk.CTkButton(self.frame, text="User Manual", command=lambda: messagebox.showinfo("User Manual", manual_text))
        self.user_manual_button.pack(pady=10)

    def create_contextual_help(self):
        self.help_button = ctk.CTkButton(self.frame, text="Help", command=self.show_contextual_help)
        self.help_button.pack(pady=10)

    def show_contextual_help(self):
        help_text = "Contextual Help:\n\n" \
                    "Click on the column headers to sort the table by that column.\n" \
                    "Use the search bar to find specific products.\n" \
                    "For more details, refer to the User Manual."
        messagebox.showinfo("Contextual Help", help_text)

if __name__ == "__main__":
    root = ctk.CTk()
    app = GroceryStore(root)
    root.geometry("1000x500")
    root.mainloop()
