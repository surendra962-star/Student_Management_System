import tkinter as tk
from PIL import Image, ImageTk
import os


def get_logo_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "assets", "logo.png")


root = tk.Tk()

root.title("Student Management System - Logo Test")
root.geometry("700x600")
root.configure(bg="#f4f6f9")

logo_path = get_logo_path()

if not os.path.exists(logo_path):
    error_label = tk.Label(
        root,
        text="Logo file not found!\n\nExpected location:\nassets/logo.png",
        font=("Arial", 16, "bold"),
        bg="#f4f6f9",
        fg="#c0392b",
        justify="center"
    )
    error_label.pack(
        expand=True
    )

else:

    image = Image.open(logo_path)

    # Keep the logo inside a reasonable size
    image.thumbnail(
        (350, 350),
        Image.Resampling.LANCZOS
    )

    logo_image = ImageTk.PhotoImage(image)

    logo_label = tk.Label(
        root,
        image=logo_image,
        bg="#f4f6f9"
    )

    logo_label.pack(
        pady=(40, 20)
    )

    title_label = tk.Label(
        root,
        text="Student Management System",
        font=("Arial", 22, "bold"),
        bg="#f4f6f9",
        fg="#1f4e78"
    )

    title_label.pack(
        pady=10
    )

    subtitle_label = tk.Label(
        root,
        text="Logo Test Successful",
        font=("Arial", 12),
        bg="#f4f6f9",
        fg="#666666"
    )

    subtitle_label.pack(
        pady=5
    )


root.mainloop()