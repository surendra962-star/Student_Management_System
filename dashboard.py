import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

from database import create_connection
from student import StudentManagement
from attendance import AttendanceManagement
from marks import MarksManagement

from theme import (
    PRIMARY,
    PRIMARY_DARK,
    BACKGROUND,
    WHITE,
    TEXT_DARK,
    TEXT_LIGHT,
    BORDER,
    SUCCESS,
    DANGER,
    configure_window,
)


class Dashboard:

    def __init__(self, root, username="Admin"):

        self.root = root
        self.username = username

        # ====================================================
        # WINDOW
        # ====================================================

        configure_window(
            self.root,
            "Student Management System - Dashboard"
        )

        self.root.geometry("1250x720")
        self.root.minsize(1050, 620)

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.logout
        )

        # ====================================================
        # COLORS
        # ====================================================

        self.sidebar_color = PRIMARY
        self.sidebar_dark = PRIMARY_DARK
        self.background_color = BACKGROUND
        self.card_color = WHITE
        self.text_color = TEXT_DARK
        self.secondary_text = TEXT_LIGHT

        # ====================================================
        # MAIN UI
        # ====================================================

        self.create_sidebar()
        self.create_main_area()
        self.show_dashboard()

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

        except Exception as e:

            print("Logo loading error:", e)

            return None

    # ========================================================
    # SIDEBAR
    # ========================================================

    def create_sidebar(self):

        self.sidebar = tk.Frame(
            self.root,
            bg=self.sidebar_color,
            width=245
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)

        # ----------------------------------------------------
        # LOGO
        # ----------------------------------------------------

        self.logo_image = self.load_logo(
            105,
            105
        )

        if self.logo_image:

            logo_label = tk.Label(
                self.sidebar,
                image=self.logo_image,
                bg=self.sidebar_color
            )

            logo_label.pack(
                pady=(25, 8)
            )

        else:

            logo_label = tk.Label(
                self.sidebar,
                text="🎓",
                font=("Arial", 45),
                bg=self.sidebar_color,
                fg=WHITE
            )

            logo_label.pack(
                pady=(30, 8)
            )

        # ----------------------------------------------------
        # APPLICATION NAME
        # ----------------------------------------------------

        title = tk.Label(
            self.sidebar,
            text="Student\nManagement\nSystem",
            font=("Arial", 17, "bold"),
            bg=self.sidebar_color,
            fg=WHITE,
            justify="center"
        )

        title.pack(
            pady=(0, 25)
        )

        # ----------------------------------------------------
        # DIVIDER
        # ----------------------------------------------------

        divider = tk.Frame(
            self.sidebar,
            bg="#5E88A7",
            height=1
        )

        divider.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

        # ----------------------------------------------------
        # MENU TITLE
        # ----------------------------------------------------

        nav_label = tk.Label(
            self.sidebar,
            text="MAIN MENU",
            font=("Arial", 9, "bold"),
            bg=self.sidebar_color,
            fg="#C9DCEA",
            anchor="w"
        )

        nav_label.pack(
            fill="x",
            padx=22,
            pady=(0, 8)
        )

        # ----------------------------------------------------
        # NAVIGATION
        # ----------------------------------------------------

        self.create_nav_button(
            "⌂   Dashboard",
            self.show_dashboard,
            active=True
        )

        self.create_nav_button(
            "♙   Students",
            self.open_students
        )

        self.create_nav_button(
            "▣   Attendance",
            self.open_attendance
        )

        self.create_nav_button(
            "▤   Marks & Results",
            self.open_marks
        )

        self.create_nav_button(
            "▧   Reports",
            self.open_reports
        )

        # ----------------------------------------------------
        # SPACER
        # ----------------------------------------------------

        spacer = tk.Frame(
            self.sidebar,
            bg=self.sidebar_color
        )

        spacer.pack(
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # USER INFORMATION
        # ----------------------------------------------------

        user_frame = tk.Frame(
            self.sidebar,
            bg=self.sidebar_dark
        )

        user_frame.pack(
            fill="x",
            padx=15,
            pady=(0, 10)
        )

        user_icon = tk.Label(
            user_frame,
            text="●",
            font=("Arial", 18),
            bg=self.sidebar_dark,
            fg="#A9D5F2"
        )

        user_icon.pack(
            side="left",
            padx=(12, 8),
            pady=10
        )

        user_info = tk.Frame(
            user_frame,
            bg=self.sidebar_dark
        )

        user_info.pack(
            side="left",
            fill="x",
            expand=True,
            pady=7
        )

        user_name = tk.Label(
            user_info,
            text=self.username,
            font=("Arial", 10, "bold"),
            bg=self.sidebar_dark,
            fg=WHITE,
            anchor="w"
        )

        user_name.pack(
            fill="x"
        )

        user_role = tk.Label(
            user_info,
            text="Administrator",
            font=("Arial", 8),
            bg=self.sidebar_dark,
            fg="#C8D8E5",
            anchor="w"
        )

        user_role.pack(
            fill="x"
        )

        # ----------------------------------------------------
        # LOGOUT
        # ----------------------------------------------------

        logout_button = tk.Button(
            self.sidebar,
            text="⇥   Logout",
            font=("Arial", 10, "bold"),
            bg=self.sidebar_dark,
            fg=WHITE,
            activebackground="#102D47",
            activeforeground=WHITE,
            bd=0,
            relief="flat",
            cursor="hand2",
            anchor="w",
            padx=22,
            command=self.logout
        )

        logout_button.pack(
            fill="x",
            padx=15,
            pady=(0, 20),
            ipady=9
        )

    # ========================================================
    # NAVIGATION BUTTON
    # ========================================================

    def create_nav_button(
        self,
        text,
        command,
        active=False
    ):

        background = (
            self.sidebar_dark
            if active
            else self.sidebar_color
        )

        button = tk.Button(
            self.sidebar,
            text=text,
            font=("Arial", 10, "bold"),
            bg=background,
            fg=WHITE,
            activebackground=self.sidebar_dark,
            activeforeground=WHITE,
            bd=0,
            relief="flat",
            anchor="w",
            padx=22,
            cursor="hand2",
            command=command
        )

        button.pack(
            fill="x",
            pady=2,
            padx=10,
            ipady=10
        )

        return button

    # ========================================================
    # MAIN AREA
    # ========================================================

    def create_main_area(self):

        self.main_area = tk.Frame(
            self.root,
            bg=self.background_color
        )

        self.main_area.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.create_header()

        self.content = tk.Frame(
            self.main_area,
            bg=self.background_color
        )

        self.content.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=25
        )

    # ========================================================
    # HEADER
    # ========================================================

    def create_header(self):

        header = tk.Frame(
            self.main_area,
            bg=WHITE,
            height=75
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        # ----------------------------------------------------
        # LEFT
        # ----------------------------------------------------

        title_frame = tk.Frame(
            header,
            bg=WHITE
        )

        title_frame.pack(
            side="left",
            padx=30
        )

        title = tk.Label(
            title_frame,
            text="Dashboard",
            font=("Arial", 21, "bold"),
            bg=WHITE,
            fg=TEXT_DARK
        )

        title.pack(
            anchor="w",
            pady=(14, 0)
        )

        subtitle = tk.Label(
            title_frame,
            text="Student Management Overview",
            font=("Arial", 9),
            bg=WHITE,
            fg=TEXT_LIGHT
        )

        subtitle.pack(
            anchor="w"
        )

        # ----------------------------------------------------
        # RIGHT
        # ----------------------------------------------------

        user_frame = tk.Frame(
            header,
            bg=WHITE
        )

        user_frame.pack(
            side="right",
            padx=30
        )

        user_icon = tk.Label(
            user_frame,
            text="●",
            font=("Arial", 16),
            bg=WHITE,
            fg=PRIMARY
        )

        user_icon.pack(
            side="left",
            padx=(0, 7)
        )

        user_label = tk.Label(
            user_frame,
            text=self.username,
            font=("Arial", 10, "bold"),
            bg=WHITE,
            fg=TEXT_DARK
        )

        user_label.pack(
            side="left"
        )

    # ========================================================
    # DASHBOARD
    # ========================================================

    def show_dashboard(self):

        for widget in self.content.winfo_children():
            widget.destroy()

        # ----------------------------------------------------
        # WELCOME
        # ----------------------------------------------------

        welcome = tk.Label(
            self.content,
            text=f"Welcome back, {self.username}!",
            font=("Arial", 22, "bold"),
            bg=self.background_color,
            fg=self.text_color
        )

        welcome.pack(
            anchor="w",
            pady=(0, 4)
        )

        subtitle = tk.Label(
            self.content,
            text="Here's an overview of your student management system.",
            font=("Arial", 10),
            bg=self.background_color,
            fg=self.secondary_text
        )

        subtitle.pack(
            anchor="w",
            pady=(0, 22)
        )

        # ----------------------------------------------------
        # STATISTICS
        # ----------------------------------------------------

        stats_frame = tk.Frame(
            self.content,
            bg=self.background_color
        )

        stats_frame.pack(
            fill="x"
        )

        self.student_card = self.create_card(
            stats_frame,
            "Students",
            "Total Students",
            "0",
            PRIMARY
        )

        self.course_card = self.create_card(
            stats_frame,
            "Courses",
            "Total Courses",
            "0",
            "#2E86C1"
        )

        self.department_card = self.create_card(
            stats_frame,
            "Departments",
            "Departments",
            "0",
            "#8E44AD"
        )

        self.attendance_card = self.create_card(
            stats_frame,
            "Attendance",
            "Attendance Records",
            "0",
            SUCCESS
        )

        # ----------------------------------------------------
        # RECENT STUDENTS
        # ----------------------------------------------------

        recent_header = tk.Frame(
            self.content,
            bg=self.background_color
        )

        recent_header.pack(
            fill="x",
            pady=(28, 10)
        )

        recent_title = tk.Label(
            recent_header,
            text="Recent Students",
            font=("Arial", 16, "bold"),
            bg=self.background_color,
            fg=self.text_color
        )

        recent_title.pack(
            side="left"
        )

        recent_info = tk.Label(
            recent_header,
            text="Latest 10 registered students",
            font=("Arial", 9),
            bg=self.background_color,
            fg=self.secondary_text
        )

        recent_info.pack(
            side="right"
        )

        # ----------------------------------------------------
        # TABLE
        # ----------------------------------------------------

        table_outer = tk.Frame(
            self.content,
            bg=WHITE,
            bd=1,
            relief="solid"
        )

        table_outer.pack(
            fill="both",
            expand=True
        )

        table_frame = tk.Frame(
            table_outer,
            bg=WHITE
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=1,
            pady=1
        )

        columns = (
            "id",
            "roll_no",
            "name",
            "gender",
            "course",
            "year"
        )

        self.student_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        headings = {
            "id": "ID",
            "roll_no": "Roll No",
            "name": "Student Name",
            "gender": "Gender",
            "course": "Course",
            "year": "Year"
        }

        for column in columns:

            self.student_table.heading(
                column,
                text=headings[column]
            )

        self.student_table.column(
            "id",
            width=60,
            anchor="center"
        )

        self.student_table.column(
            "roll_no",
            width=140,
            anchor="center"
        )

        self.student_table.column(
            "name",
            width=220,
            anchor="w"
        )

        self.student_table.column(
            "gender",
            width=100,
            anchor="center"
        )

        self.student_table.column(
            "course",
            width=220,
            anchor="w"
        )

        self.student_table.column(
            "year",
            width=80,
            anchor="center"
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.student_table.yview
        )

        self.student_table.configure(
            yscrollcommand=scrollbar.set
        )

        self.student_table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # ----------------------------------------------------
        # DATABASE
        # ----------------------------------------------------

        self.load_statistics()
        self.load_recent_students()

    # ========================================================
    # STATISTIC CARD
    # ========================================================

    def create_card(
        self,
        parent,
        icon,
        title,
        value,
        accent_color
    ):

        card = tk.Frame(
            parent,
            bg=WHITE,
            bd=1,
            relief="solid"
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        accent = tk.Frame(
            card,
            bg=accent_color,
            height=4
        )

        accent.pack(
            fill="x"
        )

        card_content = tk.Frame(
            card,
            bg=WHITE
        )

        card_content.pack(
            fill="both",
            expand=True,
            padx=17,
            pady=10
        )

        icon_label = tk.Label(
            card_content,
            text=icon,
            font=("Arial", 9, "bold"),
            bg=WHITE,
            fg=accent_color
        )

        icon_label.pack(
            anchor="w"
        )

        value_label = tk.Label(
            card_content,
            text=value,
            font=("Arial", 22, "bold"),
            bg=WHITE,
            fg=TEXT_DARK
        )

        value_label.pack(
            anchor="w",
            pady=(2, 0)
        )

        title_label = tk.Label(
            card_content,
            text=title,
            font=("Arial", 9),
            bg=WHITE,
            fg=TEXT_LIGHT
        )

        title_label.pack(
            anchor="w"
        )

        return value_label

    # ========================================================
    # LOAD STATISTICS
    # ========================================================

    def load_statistics(self):

        connection = create_connection()

        if connection is None:
            return

        cursor = None

        try:

            cursor = connection.cursor()

            cursor.execute(
                "SELECT COUNT(*) FROM students"
            )

            students = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COUNT(*) FROM courses"
            )

            courses = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COUNT(*) FROM departments"
            )

            departments = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COUNT(*) FROM attendance"
            )

            attendance = cursor.fetchone()[0]

            self.student_card.config(
                text=str(students)
            )

            self.course_card.config(
                text=str(courses)
            )

            self.department_card.config(
                text=str(departments)
            )

            self.attendance_card.config(
                text=str(attendance)
            )

        except Exception as e:

            print(
                "Statistics error:",
                e
            )

        finally:

            if cursor:

                cursor.close()

            connection.close()

    # ========================================================
    # LOAD RECENT STUDENTS
    # ========================================================

    def load_recent_students(self):

        if not hasattr(
            self,
            "student_table"
        ):
            return

        for item in self.student_table.get_children():

            self.student_table.delete(
                item
            )

        connection = create_connection()

        if connection is None:
            return

        cursor = None

        try:

            cursor = connection.cursor()

            query = """
                SELECT
                    s.id,
                    s.roll_no,
                    s.name,
                    s.gender,
                    c.course_name,
                    s.year
                FROM students s
                LEFT JOIN courses c
                    ON s.course_id = c.id
                ORDER BY s.id DESC
                LIMIT 10
            """

            cursor.execute(query)

            students = cursor.fetchall()

            for student in students:

                self.student_table.insert(
                    "",
                    "end",
                    values=student
                )

        except Exception as e:

            print(
                "Student loading error:",
                e
            )

        finally:

            if cursor:

                cursor.close()

            connection.close()

    # ========================================================
    # OPEN STUDENTS
    # ========================================================

    def open_students(self):

        window = tk.Toplevel(
            self.root
        )

        window.title(
            "Student Management"
        )

        window.geometry(
            "1250x720"
        )

        window.minsize(
            1100,
            650
        )

        StudentManagement(
            window
        )

        window.transient(
            self.root
        )

        window.grab_set()

        window.protocol(
            "WM_DELETE_WINDOW",
            window.destroy
        )

    # ========================================================
    # OPEN ATTENDANCE
    # ========================================================

    def open_attendance(self):

        window = tk.Toplevel(
            self.root
        )

        window.title(
            "Attendance Management"
        )

        window.geometry(
            "1200x700"
        )

        window.minsize(
            1000,
            600
        )

        AttendanceManagement(
            window
        )

        window.transient(
            self.root
        )

        window.grab_set()

        window.protocol(
            "WM_DELETE_WINDOW",
            window.destroy
        )

    # ========================================================
    # OPEN MARKS
    # ========================================================

    def open_marks(self):

        window = tk.Toplevel(
            self.root
        )

        window.title(
            "Marks & Results"
        )

        window.geometry(
            "1250x720"
        )

        window.minsize(
            1100,
            650
        )

        MarksManagement(
            window
        )

        window.transient(
            self.root
        )

        window.grab_set()

        window.protocol(
            "WM_DELETE_WINDOW",
            window.destroy
        )

    # ========================================================
    # REPORTS
    # ========================================================

    def open_reports(self):

        messagebox.showinfo(
            "Reports",
            "Reports module will be added in the next stage."
        )

    # ========================================================
    # LOGOUT
    # ========================================================

    def logout(self):

        result = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?"
        )

        if not result:
            return

        # Close dashboard
        self.root.destroy()

        # Open login
        import login

        login_root = tk.Tk()

        login.Login(
            login_root
        )

        login_root.mainloop()


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = Dashboard(
        root,
        "Admin"
    )

    root.mainloop()