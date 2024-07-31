import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

def show_cart_window(root):
    cart_window = ctk.CTkToplevel(root)
    cart_window.title("Cart")
    cart_window.geometry("700x500")

    cart_frame = ctk.CTkFrame(cart_window, width=700, height=500, fg_color="white")
    cart_frame.pack(fill="both", expand=True)

    # Create a back button with confirmation dialog
    def go_back():
        if messagebox.askyesno("Confirm", "Do you really want to go back?"):
            cart_window.destroy()
            root.deiconify()  # Show the main application window again

    back_button = ctk.CTkButton(cart_frame, text="Back", command=go_back)
    back_button.pack(side="top", pady=10)

    # Example cart items display (replace with your cart items)
    cart_items = [
        {"name": "Item 1", "price": "$10.00", "description": "Description of Item 1"},
        {"name": "Item 2", "price": "$20.00", "description": "Description of Item 2"},
        # Add more items as needed
    ]

    for item in cart_items:
        item_frame = ctk.CTkFrame(cart_frame, width=680, height=80, fg_color="white", corner_radius=10, border_width=1.3, border_color="lavender")
        item_frame.pack(pady=10, padx=10, fill="x")

        name_label = ctk.CTkLabel(item_frame, text=f"Name: {item['name']}", anchor="w")
        name_label.pack(side="top", padx=10, pady=5)

        price_label = ctk.CTkLabel(item_frame, text=f"Price: {item['price']}", anchor="w")
        price_label.pack(side="top", padx=10, pady=5)

        description_label = ctk.CTkLabel(item_frame, text=f"Description: {item['description']}", anchor="w")
        description_label.pack(side="top", padx=10, pady=5)

if __name__ == "__main__":
    root = ctk.CTk()
    show_cart_window(root)
    root.mainloop()
