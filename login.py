import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

from database import create_connection
from dashboard import Dashboard

from theme import (
    PRIMARY,
    PRIMARY_DARK,
    PRIMARY_LIGHT,
    BACKGROUND,
    WHITE,
    TEXT_DARK,
    TEXT_LIGHT,
    BORDER,
    SUCCESS,
    DANGER,
    FONT_TITLE,
    FONT_HEADER,
    FONT_NORMAL,
    FONT_BOLD,
    configure_window,
)


class Login:

    def __init__(self, root):

        self.root = root

        # ----------------------------------------------------
        # WINDOW
        # ----------------------------------------------------

        configure_window(
            self.root,
            "Student Management System - Login"
        )

        self.root.geometry("1000x620")
        self.root.minsize(900, 550)
        self.root.resizable(False, False)

        self.create_login_screen()

    # ========================================================
    # LOGO PATH
    # ========================================================

    def get_logo_path(self):

        base_dir = os.path.dirname(
            os.path.abspath(__file__)
        )

        return os.path.join(
            base_dir,
            "assets",
            "logo.png"
        )

    # ========================================================
    # LOAD LOGO
    # ========================================================

    def load_logo(self, max_width, max_height):

        logo_path = self.get_logo_path()

        if not os.path.exists(logo_path):

            return None

        try:

            image = Image.open(logo_path)

            image.thumbnail(
                (max_width, max_height),
                Image.Resampling.LANCZOS
            )

            return ImageTk.PhotoImage(image)

        except Exception:

            return None

    # ========================================================
    # LOGIN SCREEN
    # ========================================================

    def create_login_screen(self):

        # ----------------------------------------------------
        # MAIN CONTAINER
        # ----------------------------------------------------

        main_frame = tk.Frame(
            self.root,
            bg=BACKGROUND
        )

        main_frame.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=35
        )

        # ----------------------------------------------------
        # LEFT BRANDING PANEL
        # ----------------------------------------------------

        left_frame = tk.Frame(
            main_frame,
            bg=PRIMARY,
            width=400
        )

        left_frame.pack(
            side="left",
            fill="y"
        )

        left_frame.pack_propagate(False)

        # ----------------------------------------------------
        # LOGO
        # ----------------------------------------------------

        self.logo_image = self.load_logo(
            180,
            180
        )

        if self.logo_image:

            logo_label = tk.Label(
                left_frame,
                image=self.logo_image,
                bg=PRIMARY
            )

            logo_label.pack(
                pady=(65, 25)
            )

        else:

            logo_label = tk.Label(
                left_frame,
                text="🎓",
                font=("Arial", 70),
                bg=PRIMARY,
                fg=WHITE
            )

            logo_label.pack(
                pady=(65, 25)
            )

        # ----------------------------------------------------
        # APPLICATION TITLE
        # ----------------------------------------------------

        title_label = tk.Label(
            left_frame,
            text="Student\nManagement\nSystem",
            font=("Arial", 28, "bold"),
            bg=PRIMARY,
            fg=WHITE,
            justify="center"
        )

        title_label.pack()

        # ----------------------------------------------------
        # DESCRIPTION
        # ----------------------------------------------------

        subtitle_label = tk.Label(
            left_frame,
            text="Manage students efficiently\n"
                 "and securely",
            font=("Arial", 12),
            bg=PRIMARY,
            fg="#EAF3FA",
            justify="center"
        )

        subtitle_label.pack(
            pady=(18, 20)
        )

        # ----------------------------------------------------
        # DIVIDER
        # ----------------------------------------------------

        divider = tk.Frame(
            left_frame,
            bg="#6F9FC2",
            height=1,
            width=220
        )

        divider.pack(
            pady=10
        )

        # ----------------------------------------------------
        # FOOTER
        # ----------------------------------------------------

        footer_label = tk.Label(
            left_frame,
            text="Student Administration Portal",
            font=("Arial", 10),
            bg=PRIMARY,
            fg="#D8E8F4"
        )

        footer_label.pack(
            pady=15
        )

        # ----------------------------------------------------
        # RIGHT LOGIN PANEL
        # ----------------------------------------------------

        right_frame = tk.Frame(
            main_frame,
            bg=WHITE
        )

        right_frame.pack(
            side="right",
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # LOGIN CONTENT
        # ----------------------------------------------------

        content_frame = tk.Frame(
            right_frame,
            bg=WHITE
        )

        content_frame.pack(
            fill="both",
            expand=True,
            padx=65
        )

        # ----------------------------------------------------
        # WELCOME TITLE
        # ----------------------------------------------------

        welcome_label = tk.Label(
            content_frame,
            text="Welcome Back!",
            font=("Arial", 27, "bold"),
            bg=WHITE,
            fg=TEXT_DARK
        )

        welcome_label.pack(
            pady=(70, 8)
        )

        # ----------------------------------------------------
        # SUBTITLE
        # ----------------------------------------------------

        login_subtitle = tk.Label(
            content_frame,
            text="Sign in to access your dashboard",
            font=("Arial", 11),
            bg=WHITE,
            fg=TEXT_LIGHT
        )

        login_subtitle.pack(
            pady=(0, 35)
        )

        # ----------------------------------------------------
        # USERNAME LABEL
        # ----------------------------------------------------

        username_label = tk.Label(
            content_frame,
            text="Username",
            font=FONT_BOLD,
            bg=WHITE,
            fg=TEXT_DARK
        )

        username_label.pack(
            anchor="w",
            pady=(0, 7)
        )

        # ----------------------------------------------------
        # USERNAME ENTRY
        # ----------------------------------------------------

        username_frame = tk.Frame(
            content_frame,
            bg=BORDER
        )

        username_frame.pack(
            fill="x"
        )

        self.username_entry = tk.Entry(
            username_frame,
            font=("Arial", 12),
            bg=WHITE,
            fg=TEXT_DARK,
            insertbackground=PRIMARY,
            relief="flat",
            bd=0
        )

        self.username_entry.pack(
            fill="x",
            padx=1,
            pady=1,
            ipady=9
        )

        # ----------------------------------------------------
        # PASSWORD LABEL
        # ----------------------------------------------------

        password_label = tk.Label(
            content_frame,
            text="Password",
            font=FONT_BOLD,
            bg=WHITE,
            fg=TEXT_DARK
        )

        password_label.pack(
            anchor="w",
            pady=(22, 7)
        )

        # ----------------------------------------------------
        # PASSWORD FRAME
        # ----------------------------------------------------

        password_outer_frame = tk.Frame(
            content_frame,
            bg=BORDER
        )

        password_outer_frame.pack(
            fill="x"
        )

        password_frame = tk.Frame(
            password_outer_frame,
            bg=WHITE
        )

        password_frame.pack(
            fill="x",
            padx=1,
            pady=1
        )

        self.password_entry = tk.Entry(
            password_frame,
            font=("Arial", 12),
            bg=WHITE,
            fg=TEXT_DARK,
            insertbackground=PRIMARY,
            relief="flat",
            bd=0,
            show="*"
        )

        self.password_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=9
        )

        # ----------------------------------------------------
        # SHOW PASSWORD BUTTON
        # ----------------------------------------------------

        self.show_password = False

        self.show_button = tk.Button(
            password_frame,
            text="Show",
            command=self.toggle_password,
            font=("Arial", 9, "bold"),
            bg=WHITE,
            fg=PRIMARY,
            activebackground=WHITE,
            activeforeground=PRIMARY_DARK,
            relief="flat",
            bd=0,
            cursor="hand2"
        )

        self.show_button.pack(
            side="right",
            padx=8
        )

        # ----------------------------------------------------
        # BUTTON FRAME
        # ----------------------------------------------------

        button_frame = tk.Frame(
            content_frame,
            bg=WHITE
        )

        button_frame.pack(
            fill="x",
            pady=(32, 15)
        )

        # ----------------------------------------------------
        # LOGIN BUTTON
        # ----------------------------------------------------

        self.login_button = tk.Button(
            button_frame,
            text="LOGIN",
            command=self.login,
            font=("Arial", 11, "bold"),
            bg=PRIMARY,
            fg=WHITE,
            activebackground=PRIMARY_DARK,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            pady=10
        )

        self.login_button.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 6)
        )

        # ----------------------------------------------------
        # CLEAR BUTTON
        # ----------------------------------------------------

        self.clear_button = tk.Button(
            button_frame,
            text="CLEAR",
            command=self.clear_fields,
            font=("Arial", 11, "bold"),
            bg="#E5E7EB",
            fg=TEXT_DARK,
            activebackground="#D1D5DB",
            activeforeground=TEXT_DARK,
            relief="flat",
            bd=0,
            cursor="hand2",
            pady=10
        )

        self.clear_button.pack(
            side="right",
            fill="x",
            expand=True,
            padx=(6, 0)
        )

        # ----------------------------------------------------
        # LOGIN INFORMATION
        # ----------------------------------------------------

        info_label = tk.Label(
            content_frame,
            text="Enter your registered credentials to continue.",
            font=("Arial", 9),
            bg=WHITE,
            fg=TEXT_LIGHT
        )

        info_label.pack(
            pady=(8, 0)
        )

        # ----------------------------------------------------
        # INITIAL FOCUS
        # ----------------------------------------------------

        self.username_entry.focus()

        # ----------------------------------------------------
        # ENTER KEY
        # ----------------------------------------------------

        self.root.bind(
            "<Return>",
            lambda event: self.login()
        )

    # ========================================================
    # TOGGLE PASSWORD
    # ========================================================

    def toggle_password(self):

        if self.show_password:

            self.password_entry.config(
                show="*"
            )

            self.show_button.config(
                text="Show"
            )

            self.show_password = False

        else:

            self.password_entry.config(
                show=""
            )

            self.show_button.config(
                text="Hide"
            )

            self.show_password = True

    # ========================================================
    # CLEAR FIELDS
    # ========================================================

    def clear_fields(self):

        self.username_entry.delete(
            0,
            tk.END
        )

        self.password_entry.delete(
            0,
            tk.END
        )

        self.username_entry.focus()

    # ========================================================
    # LOGIN
    # ========================================================

    def login(self):

        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if username == "" or password == "":

            messagebox.showwarning(
                "Login Required",
                "Please enter username and password."
            )

            return

        # ----------------------------------------------------
        # DATABASE CONNECTION
        # ----------------------------------------------------

        connection = create_connection()

        if connection is None:

            messagebox.showerror(
                "Database Error",
                "Unable to connect to MySQL database."
            )

            return

        cursor = None

        try:

            cursor = connection.cursor()

            # ------------------------------------------------
            # AUTHENTICATION QUERY
            # ------------------------------------------------

            query = """
                SELECT id, username
                FROM users
                WHERE username = %s
                AND password = %s
            """

            cursor.execute(
                query,
                (
                    username,
                    password
                )
            )

            user = cursor.fetchone()

            if user:

                messagebox.showinfo(
                    "Login Successful",
                    f"Welcome, {username}!"
                )

                # --------------------------------------------
                # CLOSE LOGIN WINDOW
                # --------------------------------------------

                self.root.destroy()

                # --------------------------------------------
                # OPEN DASHBOARD
                # --------------------------------------------

                dashboard_root = tk.Tk()

                Dashboard(
                    dashboard_root,
                    username
                )

                dashboard_root.mainloop()

            else:

                messagebox.showerror(
                    "Login Failed",
                    "Invalid username or password."
                )

                self.password_entry.delete(
                    0,
                    tk.END
                )

                self.password_entry.focus()

        except Exception as e:

            if connection:
                try:
                    connection.rollback()
                except Exception:
                    pass

            messagebox.showerror(
                "Error",
                f"An error occurred:\n{e}"
            )

        finally:

            if cursor:

                try:
                    cursor.close()
                except Exception:
                    pass

            try:
                connection.close()
            except Exception:
                pass


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = Login(root)

    root.mainloop()