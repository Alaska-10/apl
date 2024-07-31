import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from threading import Thread
import time
import subprocess
import sys
import os

class LoadingPage(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.title("Loading...")
        self.attributes("-fullscreen", True)  # Open window in full screen
        self.configure(bg="white")
        
        # Load and fit background image
        self.background_image = Image.open("/Users/adityadas/Downloads/ebarthur-grocery-shop-87bf58c/login.png")  # Background image path
        self.background_image = self.background_image.resize((self.winfo_screenwidth(), self.winfo_screenheight()))  # Resize to full screen
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.bg_label = tk.Label(self, image=self.background_photo)
        self.bg_label.place(relwidth=1, relheight=1)
        
        # Load logo image and resize it
        self.logo_image = Image.open("/Users/adityadas/Downloads/ebarthur-grocery-shop-87bf58c/vegetables-shopping-cart-trolley-grocery-logo-icon-design-vector-171090350.jpg.webp")
        self.logo_image = self.logo_image.resize((150, 150))  # Resize logo image
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(self, image=self.logo_photo, bg="white")
        self.logo_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)  # Center the logo
        
        # Create a traditional-looking progress bar
        self.progress_bar = ttk.Progressbar(self, length=300, mode='determinate')
        self.progress_bar.place(relx=0.5, rely=0.6, anchor=tk.CENTER)  # Center the progress bar
        
        # Start the loading process
        self.loading_thread = Thread(target=self.loading_process)
        self.loading_thread.start()

    def loading_process(self):
        for i in range(101):
            time.sleep(0.02)  # 2 seconds total for 100 steps
            self.progress_bar['value'] = i
        
        # Destroy the loading page
        self.destroy()

        # Start the cashier app after loading page is destroyed
        cashier_path = "/Users/adityadas/Downloads/ebarthur-grocery-shop-87bf58c/checkout/cashier_app.py"
        if os.path.exists(cashier_path):
            subprocess.Popen([sys.executable, cashier_path])

if __name__ == "__main__":
    app = LoadingPage()
    app.mainloop()
