import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO
import requests
import sys

class ItemDetails:
    def __init__(self, root, product_name, price, description, image_url):
        self.root = root
        self.root.title("Item Details")
        self.root.geometry("600x800")

        self.product_name = product_name
        self.price = price
        self.description = description
        self.image_url = image_url

        self.create_widgets()

    def create_widgets(self):
        main_frame = ctk.CTkFrame(self.root, width=600, height=800, bg_color="#ffffff")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Load and display the image
        img = self.load_image_from_url(self.image_url)
        if img:
            image_label = ctk.CTkLabel(main_frame, image=img, bg_color="#ffffff")
            image_label.image = img
            image_label.pack(pady=10)

        # Display product details
        name_label = ctk.CTkLabel(main_frame, text=f"Name: {self.product_name}", font=("Helvetica", 16))
        name_label.pack(pady=5)

        price_label = ctk.CTkLabel(main_frame, text=f"Price: {self.price}", font=("Helvetica", 16))
        price_label.pack(pady=5)

        description_label = ctk.CTkLabel(main_frame, text=f"Description: {self.description}", font=("Helvetica", 14), wraplength=500)
        description_label.pack(pady=10)

    def load_image_from_url(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            img = img.resize((300, 300))  # Resize image for display
            return ImageTk.PhotoImage(img)
        except requests.RequestException as e:
            print(f"Error fetching image: {e}")
            return None

if __name__ == "__main__":
    if len(sys.argv) != 5:
        messagebox.showerror("Error", "Invalid number of arguments.")
        sys.exit(1)

    product_name = sys.argv[1]
    price = sys.argv[2]
    description = sys.argv[3]
    image_url = sys.argv[4]

    root = ctk.CTk()
    app = ItemDetails(root, product_name, price, description, image_url)
    root.mainloop()
