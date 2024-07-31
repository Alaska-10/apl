import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import mysql.connector
from PIL import Image, ImageTk
from io import BytesIO
import requests
import subprocess
import cart  # Import cart.py here

class GroceryStore:
    def __init__(self, root):
        self.root = root
        self.root.title("Groceria")
        self.root.geometry("1200x800")
        ctk.set_appearance_mode("light")

        self.create_widgets()

    def create_widgets(self):
        # Main frame with navy blue background
        self.main_frame = ctk.CTkFrame(self.root, width=1200, height=800, fg_color="navy",bg_color="navy")
        self.main_frame.pack(fill="both", expand=True)

        # Top frame with increased height and navy blue background
        self.top_frame = ctk.CTkFrame(self.main_frame, height=100, fg_color="navy", bg_color="navy")
        self.top_frame.pack(side="top", fill="x", padx=10, pady=10)

        # Back button
        self.back_button = ctk.CTkButton(self.top_frame, text="Back", command=self.confirm_exit)
        self.back_button.pack(side="left", padx=5)

        self.search_label = ctk.CTkLabel(self.top_frame, text="Search by Product ID or Name:", text_color="white")
        self.search_label.pack(side="left", padx=5)

        self.search_entry = ctk.CTkEntry(self.top_frame, placeholder_text="Enter Product ID or Name", width=250)
        self.search_entry.pack(side="left", padx=5)

        # Replace search button with an image
        self.search_image = Image.open("icon.jpeg")
        self.search_image = self.search_image.resize((30, 30))
        self.search_photo = ImageTk.PhotoImage(self.search_image)
        
        self.search_button = tk.Label(self.top_frame, image=self.search_photo, bg="navy", cursor="hand2")
        self.search_button.pack(side="left", padx=5)
        self.search_button.bind("<Button-1>", lambda e: self.search_product())

        # Title "GROCERIA"
        self.title_label = ctk.CTkLabel(self.top_frame, text="GROCERIA", text_color="white", font=("Helvetica", 16, "bold"))
        self.title_label.pack(side="left", padx=30)

        # Menu Button
        self.menu_button_image = Image.open("menu_icon.png")  # Replace with your menu icon image
        self.menu_button_image = self.menu_button_image.resize((30, 30))
        self.menu_button_photo = ImageTk.PhotoImage(self.menu_button_image)
        
        self.menu_button = tk.Label(self.top_frame, image=self.menu_button_photo, bg="navy", cursor="hand2")
        self.menu_button.pack(side="right", padx=10)
        self.menu_button.bind("<Button-1>", lambda e: self.toggle_menu())

        # Sidebar Menu Frame
        self.menu_frame = ctk.CTkFrame(self.main_frame, width=200, height=800, fg_color="#f0f0f0", corner_radius=10)
        self.menu_frame.place(x=1200, y=100)  # Initially hidden off-screen
        self.menu_frame.pack_propagate(False)  # Prevent frame from resizing to fit its content

        self.cart_button = ctk.CTkButton(self.menu_frame, text="Cart", command=self.show_cart)
        self.cart_button.pack(fill="x", pady=5)

        self.profile_button = ctk.CTkButton(self.menu_frame, text="Profile", command=self.show_profile)
        self.profile_button.pack(fill="x", pady=5)

        self.orders_button = ctk.CTkButton(self.menu_frame, text="Orders", command=self.show_orders)
        self.orders_button.pack(fill="x", pady=5)

        self.history_button = ctk.CTkButton(self.menu_frame, text="History", command=self.show_history)
        self.history_button.pack(fill="x", pady=5)
        
        self.create_product_display()

    def create_product_display(self):
        # Create a Canvas for scrolling
        self.canvas = tk.Canvas(self.main_frame, bg="lavender")
        self.scroll_y = tk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scroll_y.set)
        
        # Create a Frame inside the Canvas for product display
        self.product_frame = tk.Frame(self.canvas, bg="lavender")
        self.canvas.create_window((0, 0), window=self.product_frame, anchor="nw")

        # Pack the Canvas and Scrollbar
        self.canvas.place(x=0, y=79, width=1200 ,relheight=1)
        self.scroll_y.pack(side="right", fill="y")

        self.populate_product_display()

        # Update Canvas scrolling region
        self.product_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def populate_product_display(self, search_term=""):
        for widget in self.product_frame.winfo_children():
            widget.destroy()

        try:
            with self.get_db_connection() as connection:
                with connection.cursor() as cursor:
                    query = "SELECT * FROM inventory WHERE product_id LIKE %s OR product_name LIKE %s"
                    params = (f"%{search_term}%", f"%{search_term}%")
                    cursor.execute(query, params)
                    data = cursor.fetchall()

                    # Create a grid with 4 columns for product display
                    for index, record in enumerate(data):
                        row = index // 4
                        column = index % 4

                        # Frame with white background and light grey border
                        box_frame = ctk.CTkFrame(self.product_frame, fg_color="white", width=250, height=300, corner_radius=5)
                        box_frame.grid(row=row, column=column, padx=7, pady=7, sticky="nsew")

                        # Inner frame to simulate border
                        border_frame = ctk.CTkFrame(box_frame, fg_color="white", width=248, height=298, corner_radius=5)
                        border_frame.pack(padx=1, pady=1, fill="both", expand=True)  # Create a 1-unit padding to simulate border

                        # Load and display the image
                        image_url = record[10]  # Assuming 'image_path' is the 11th column
                        img = self.load_image_from_url(image_url, width=240, height=230)
                        if img:
                            image_label = tk.Label(border_frame, image=img, bg="white")
                            image_label.image = img
                            image_label.pack()

                        product_name = record[1]
                        price = f"${float(record[4].replace('$', '').replace(',', '')):.2f}"
                        rating = int(record[11])  # Assuming 'rating' is the 12th column
                        name_price_label = ctk.CTkLabel(border_frame, text=f"Name: {product_name}\nPrice: {price}", anchor="w", fg_color="white")
                        name_price_label.pack(anchor="w")

                        # Display the rating with a white background
                        self.display_rating(border_frame, rating)

                        # Add to Cart button with yellow background, black text, and border width
                        add_to_cart_button = ctk.CTkButton(border_frame, text="Add to Cart", text_color='black', command=lambda r=record: self.add_to_cart(r), fg_color="yellow", border_width=0.88)
                        add_to_cart_button.pack(pady=9)

                        box_frame.bind("<Button-1>", lambda e, r=record: self.show_product_details(r))

                    # Configure grid weights to ensure boxes expand evenly
                    for i in range(4):
                        self.product_frame.grid_columnconfigure(i, weight=1)
                    self.product_frame.grid_rowconfigure(row, weight=1)

                    # Update Canvas scrolling region
                    self.product_frame.update_idletasks()
                    self.canvas.config(scrollregion=self.canvas.bbox("all"))

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def get_db_connection(self):
        return mysql.connector.connect(
            host="127.0.0.1",
            database="grocery_store",
            user="root",
            password="ADXXSTAR$"
        )

    def show_product_details(self, record):
        product_name = record[1]
        price = f"${float(record[4].replace('$', '').replace(',', '')):.2f}"
        description = record[12]  # Assuming 'description' is the 13th column
        image_url = record[10]  # Assuming 'image_path' is the 11th column

        subprocess.Popen(["python", "items.py", product_name, price, description, image_url])

    def load_image_from_url(self, url, width=240, height=230):
        try:
            response = requests.get(url)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            img = img.resize((width, height))  # Resize image for display
            return ImageTk.PhotoImage(img)
        except requests.RequestException as e:
            print(f"Error fetching image: {e}")
            return None

    def display_rating(self, frame, rating):
        rating_label = ctk.CTkLabel(frame, fg_color="white")
        rating_label.pack()
        stars = "⭐️" * rating
        empty_stars = "⭐️" * (5 - rating)
        rating_label.configure(text=stars + empty_stars, font=("Arial", 12))

    def add_to_cart(self, product):
        cart.add_product_to_cart(product)  # Ensure this function is properly defined in cart.py

    def show_cart(self):
        subprocess.Popen(["python", "cart.py"])

    def show_profile(self):
        subprocess.Popen(["python", "profile.py"])

    def show_orders(self):
        subprocess.Popen(["python", "orders.py"])

    def show_history(self):
        subprocess.Popen(["python", "history.py"])

    def toggle_menu(self):
        if self.menu_frame.winfo_x() == 1200:  # Check if the menu is off-screen
            self.menu_frame.place(x=0)  # Slide in menu
        else:
            self.menu_frame.place(x=1200)  # Slide out menu

    def confirm_exit(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()

if __name__ == "__main__":
    root = ctk.CTk()
    app = GroceryStore(root)
    root.mainloop()
