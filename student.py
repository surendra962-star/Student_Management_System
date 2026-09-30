import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

from database import create_connection

from validation import (
    validate_required,
    validate_name,
    validate_roll_no,
    validate_email,
    validate_phone,
    validate_date,
    validate_year
)

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
    configure_window
)


class StudentManagement:

    def __init__(self, root):

        self.root = root

        # ====================================================
        # WINDOW
        # ====================================================

        configure_window(
            self.root,
            "Student Management System - Students"
        )

        self.root.geometry("1250x720")
        self.root.minsize(1100, 650)

        self.selected_student_id = None

        # ====================================================
        # CREATE UI
        # ====================================================

        self.create_header()
        self.create_statistics()
        self.create_search_area()
        self.create_student_table()

        # ====================================================
        # LOAD DATA
        # ====================================================

        self.load_students()
        self.load_statistics()

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

    def load_logo(
        self,
        max_width,
        max_height
    ):

        logo_path = self.get_logo_path()

        if not os.path.exists(logo_path):
            return None

        try:

            image = Image.open(
                logo_path
            )

            image.thumbnail(
                (
                    max_width,
                    max_height
                ),
                Image.Resampling.LANCZOS
            )

            return ImageTk.PhotoImage(
                image
            )

        except Exception as e:

            print(
                "Logo loading error:",
                e
            )

            return None

    # ========================================================
    # HEADER
    # ========================================================

    def create_header(self):

        header = tk.Frame(
            self.root,
            bg=WHITE,
            height=75
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        # ----------------------------------------------------
        # LEFT SIDE
        # ----------------------------------------------------

        left_frame = tk.Frame(
            header,
            bg=WHITE
        )

        left_frame.pack(
            side="left",
            padx=25
        )

        # Logo

        self.header_logo = self.load_logo(
            48,
            48
        )

        if self.header_logo:

            logo_label = tk.Label(
                left_frame,
                image=self.header_logo,
                bg=WHITE
            )

            logo_label.pack(
                side="left",
                padx=(0, 12)
            )

        # Title

        title_frame = tk.Frame(
            left_frame,
            bg=WHITE
        )

        title_frame.pack(
            side="left"
        )

        title = tk.Label(
            title_frame,
            text="Student Management",
            font=("Arial", 21, "bold"),
            bg=WHITE,
            fg=PRIMARY
        )

        title.pack(
            anchor="w",
            pady=(12, 0)
        )

        subtitle = tk.Label(
            title_frame,
            text="Student records and information",
            font=("Arial", 9),
            bg=WHITE,
            fg=TEXT_LIGHT
        )

        subtitle.pack(
            anchor="w"
        )

        # ----------------------------------------------------
        # ADD BUTTON
        # ----------------------------------------------------

        add_button = tk.Button(
            header,
            text="+  Add Student",
            command=self.open_add_student,
            font=("Arial", 10, "bold"),
            bg=PRIMARY,
            fg=WHITE,
            activebackground=PRIMARY_DARK,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=18,
            pady=9
        )

        add_button.pack(
            side="right",
            padx=25
        )

    # ========================================================
    # STATISTICS
    # ========================================================

    def create_statistics(self):

        self.stats_frame = tk.Frame(
            self.root,
            bg=BACKGROUND
        )

        self.stats_frame.pack(
            fill="x",
            padx=25,
            pady=(20, 5)
        )

        self.total_students_card = self.create_stat_card(
            self.stats_frame,
            "TOTAL STUDENTS",
            "0",
            PRIMARY
        )

        self.male_students_card = self.create_stat_card(
            self.stats_frame,
            "MALE STUDENTS",
            "0",
            "#2E86C1"
        )

        self.female_students_card = self.create_stat_card(
            self.stats_frame,
            "FEMALE STUDENTS",
            "0",
            "#8E44AD"
        )

        self.courses_card = self.create_stat_card(
            self.stats_frame,
            "REGISTERED COURSES",
            "0",
            SUCCESS
        )

    # ========================================================
    # STATISTIC CARD
    # ========================================================

    def create_stat_card(
        self,
        parent,
        title,
        value,
        accent
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

        accent_bar = tk.Frame(
            card,
            bg=accent,
            height=4
        )

        accent_bar.pack(
            fill="x"
        )

        content = tk.Frame(
            card,
            bg=WHITE
        )

        content.pack(
            fill="both",
            expand=True,
            padx=16,
            pady=7
        )

        title_label = tk.Label(
            content,
            text=title,
            font=("Arial", 8, "bold"),
            bg=WHITE,
            fg=TEXT_LIGHT
        )

        title_label.pack(
            anchor="w"
        )

        value_label = tk.Label(
            content,
            text=value,
            font=("Arial", 20, "bold"),
            bg=WHITE,
            fg=TEXT_DARK
        )

        value_label.pack(
            anchor="w",
            pady=(2, 5)
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

            # Total students

            cursor.execute(
                "SELECT COUNT(*) FROM students"
            )

            total_students = cursor.fetchone()[0]

            # Male students

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM students
                WHERE gender = 'Male'
                """
            )

            male_students = cursor.fetchone()[0]

            # Female students

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM students
                WHERE gender = 'Female'
                """
            )

            female_students = cursor.fetchone()[0]

            # Registered courses

            cursor.execute(
                "SELECT COUNT(*) FROM courses"
            )

            total_courses = cursor.fetchone()[0]

            # Update cards

            self.total_students_card.config(
                text=str(total_students)
            )

            self.male_students_card.config(
                text=str(male_students)
            )

            self.female_students_card.config(
                text=str(female_students)
            )

            self.courses_card.config(
                text=str(total_courses)
            )

        except Exception as e:

            print(
                "Student statistics error:",
                e
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

    # ========================================================
    # SEARCH AREA
    # ========================================================

    def create_search_area(self):

        search_outer = tk.Frame(
            self.root,
            bg=BACKGROUND
        )

        search_outer.pack(
            fill="x",
            padx=25,
            pady=(15, 12)
        )

        # ----------------------------------------------------
        # SEARCH LABEL
        # ----------------------------------------------------

        search_label = tk.Label(
            search_outer,
            text="Search Students",
            font=("Arial", 12, "bold"),
            bg=BACKGROUND,
            fg=TEXT_DARK
        )

        search_label.pack(
            side="left",
            padx=(0, 12)
        )

        # ----------------------------------------------------
        # SEARCH ENTRY
        # ----------------------------------------------------

        entry_frame = tk.Frame(
            search_outer,
            bg=BORDER
        )

        entry_frame.pack(
            side="left"
        )

        self.search_entry = tk.Entry(
            entry_frame,
            font=("Arial", 10),
            bg=WHITE,
            fg=TEXT_DARK,
            insertbackground=PRIMARY,
            relief="flat",
            bd=0,
            width=38
        )

        self.search_entry.pack(
            padx=1,
            pady=1,
            ipady=7
        )

        # ----------------------------------------------------
        # SEARCH BUTTON
        # ----------------------------------------------------

        search_button = tk.Button(
            search_outer,
            text="Search",
            command=self.search_students,
            font=("Arial", 9, "bold"),
            bg=PRIMARY,
            fg=WHITE,
            activebackground=PRIMARY_DARK,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=16,
            pady=7
        )

        search_button.pack(
            side="left",
            padx=6
        )

        # ----------------------------------------------------
        # REFRESH BUTTON
        # ----------------------------------------------------

        refresh_button = tk.Button(
            search_outer,
            text="Refresh",
            command=self.refresh_students,
            font=("Arial", 9, "bold"),
            bg=WHITE,
            fg=TEXT_DARK,
            activebackground=PRIMARY_LIGHT,
            activeforeground=TEXT_DARK,
            relief="solid",
            bd=1,
            cursor="hand2",
            padx=16,
            pady=6
        )

        refresh_button.pack(
            side="left",
            padx=3
        )

        # ----------------------------------------------------
        # DELETE BUTTON
        # ----------------------------------------------------

        delete_button = tk.Button(
            search_outer,
            text="Delete Selected",
            command=self.delete_selected_student,
            font=("Arial", 9, "bold"),
            bg=DANGER,
            fg=WHITE,
            activebackground="#922B21",
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=16,
            pady=7
        )

        delete_button.pack(
            side="left",
            padx=6
        )

        # ----------------------------------------------------
        # ENTER KEY
        # ----------------------------------------------------

        self.search_entry.bind(
            "<Return>",
            lambda event: self.search_students()
        )

    # ========================================================
    # STUDENT TABLE
    # ========================================================

    def create_student_table(self):

        table_outer = tk.Frame(
            self.root,
            bg=WHITE,
            bd=1,
            relief="solid"
        )

        table_outer.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 25)
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
            "year",
            "email",
            "phone"
        )

        self.student_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        # ----------------------------------------------------
        # HEADINGS
        # ----------------------------------------------------

        self.student_table.heading(
            "id",
            text="ID"
        )

        self.student_table.heading(
            "roll_no",
            text="Roll No"
        )

        self.student_table.heading(
            "name",
            text="Student Name"
        )

        self.student_table.heading(
            "gender",
            text="Gender"
        )

        self.student_table.heading(
            "course",
            text="Course"
        )

        self.student_table.heading(
            "year",
            text="Year"
        )

        self.student_table.heading(
            "email",
            text="Email"
        )

        self.student_table.heading(
            "phone",
            text="Phone"
        )

        # ----------------------------------------------------
        # COLUMNS
        # ----------------------------------------------------

        self.student_table.column(
            "id",
            width=55,
            anchor="center"
        )

        self.student_table.column(
            "roll_no",
            width=115,
            anchor="center"
        )

        self.student_table.column(
            "name",
            width=190,
            anchor="w"
        )

        self.student_table.column(
            "gender",
            width=85,
            anchor="center"
        )

        self.student_table.column(
            "course",
            width=190,
            anchor="w"
        )

        self.student_table.column(
            "year",
            width=70,
            anchor="center"
        )

        self.student_table.column(
            "email",
            width=230,
            anchor="w"
        )

        self.student_table.column(
            "phone",
            width=130,
            anchor="center"
        )

        # ----------------------------------------------------
        # SCROLLBARS
        # ----------------------------------------------------

        vertical_scroll = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.student_table.yview
        )

        horizontal_scroll = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.student_table.xview
        )

        self.student_table.configure(
            yscrollcommand=vertical_scroll.set,
            xscrollcommand=horizontal_scroll.set
        )

        self.student_table.pack(
            side="left",
            fill="both",
            expand=True
        )

        vertical_scroll.pack(
            side="right",
            fill="y"
        )

        horizontal_scroll.pack(
            side="bottom",
            fill="x"
        )

        # ----------------------------------------------------
        # DOUBLE CLICK = EDIT
        # ----------------------------------------------------

        self.student_table.bind(
            "<Double-1>",
            self.edit_selected_student
        )

    # ========================================================
    # LOAD STUDENTS
    # ========================================================

    def load_students(
        self,
        search_text=""
    ):

        for item in self.student_table.get_children():

            self.student_table.delete(
                item
            )

        connection = create_connection()

        if connection is None:

            messagebox.showerror(
                "Database Error",
                "Could not connect to database."
            )

            return

        cursor = None

        try:

            cursor = connection.cursor()

            if search_text:

                query = """
                    SELECT
                        s.id,
                        s.roll_no,
                        s.name,
                        s.gender,
                        c.course_name,
                        s.year,
                        s.email,
                        s.phone
                    FROM students s
                    LEFT JOIN courses c
                        ON s.course_id = c.id
                    WHERE
                        s.roll_no LIKE %s
                        OR s.name LIKE %s
                        OR s.email LIKE %s
                        OR s.phone LIKE %s
                    ORDER BY s.id DESC
                """

                value = "%" + search_text + "%"

                cursor.execute(
                    query,
                    (
                        value,
                        value,
                        value,
                        value
                    )
                )

            else:

                query = """
                    SELECT
                        s.id,
                        s.roll_no,
                        s.name,
                        s.gender,
                        c.course_name,
                        s.year,
                        s.email,
                        s.phone
                    FROM students s
                    LEFT JOIN courses c
                        ON s.course_id = c.id
                    ORDER BY s.id DESC
                """

                cursor.execute(
                    query
                )

            students = cursor.fetchall()

            for student in students:

                self.student_table.insert(
                    "",
                    "end",
                    values=student
                )

            if search_text and not students:

                messagebox.showinfo(
                    "Search Result",
                    "No students found matching your search."
                )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Could not load students:\n{e}"
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

    # ========================================================
    # SEARCH
    # ========================================================

    def search_students(self):

        search_text = (
            self.search_entry
            .get()
            .strip()
        )

        self.load_students(
            search_text
        )

    # ========================================================
    # REFRESH
    # ========================================================

    def refresh_students(self):

        self.search_entry.delete(
            0,
            tk.END
        )

        self.load_students()

        self.load_statistics()

    # ========================================================
    # ADD STUDENT
    # ========================================================

    def open_add_student(self):

        self.selected_student_id = None

        self.open_student_form(
            title="Add Student"
        )

    # ========================================================
    # STUDENT FORM
    # ========================================================

    def open_student_form(
        self,
        title="Add Student"
    ):

        form_window = tk.Toplevel(
            self.root
        )

        form_window.title(
            title
        )

        form_window.geometry(
            "680x720"
        )

        form_window.resizable(
            False,
            False
        )

        form_window.configure(
            bg=BACKGROUND
        )

        form_window.transient(
            self.root
        )

        form_window.grab_set()

        # ----------------------------------------------------
        # FORM HEADER
        # ----------------------------------------------------

        form_header = tk.Frame(
            form_window,
            bg=PRIMARY,
            height=75
        )

        form_header.pack(
            fill="x"
        )

        form_header.pack_propagate(
            False
        )

        form_title = tk.Label(
            form_header,
            text=title,
            font=("Arial", 20, "bold"),
            bg=PRIMARY,
            fg=WHITE
        )

        form_title.pack(
            side="left",
            padx=25
        )

        # ----------------------------------------------------
        # FORM CONTAINER
        # ----------------------------------------------------

        form_frame = tk.Frame(
            form_window,
            bg=WHITE
        )

        form_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        # ----------------------------------------------------
        # VARIABLES
        # ----------------------------------------------------

        self.roll_no_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.gender_var = tk.StringVar()
        self.dob_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.course_var = tk.StringVar()
        self.year_var = tk.StringVar()
        self.admission_date_var = tk.StringVar()

        # ----------------------------------------------------
        # FORM HELPER
        # ----------------------------------------------------

        def create_label_entry(
            row,
            label_text,
            variable
        ):

            label = tk.Label(
                form_frame,
                text=label_text,
                font=("Arial", 9, "bold"),
                bg=WHITE,
                fg=TEXT_DARK
            )

            label.grid(
                row=row,
                column=0,
                padx=(20, 15),
                pady=7,
                sticky="w"
            )

            entry_frame = tk.Frame(
                form_frame,
                bg=BORDER
            )

            entry_frame.grid(
                row=row,
                column=1,
                padx=(0, 20),
                pady=7,
                sticky="ew"
            )

            entry = tk.Entry(
                entry_frame,
                textvariable=variable,
                font=("Arial", 10),
                bg=WHITE,
                fg=TEXT_DARK,
                insertbackground=PRIMARY,
                relief="flat",
                bd=0
            )

            entry.pack(
                fill="x",
                padx=1,
                pady=1,
                ipady=5
            )

            return entry

        form_frame.columnconfigure(
            1,
            weight=1
        )

        # ----------------------------------------------------
        # ROLL NUMBER
        # ----------------------------------------------------

        create_label_entry(
            0,
            "Roll Number *",
            self.roll_no_var
        )

        # ----------------------------------------------------
        # NAME
        # ----------------------------------------------------

        create_label_entry(
            1,
            "Student Name *",
            self.name_var
        )

        # ----------------------------------------------------
        # GENDER
        # ----------------------------------------------------

        tk.Label(
            form_frame,
            text="Gender",
            font=("Arial", 9, "bold"),
            bg=WHITE,
            fg=TEXT_DARK
        ).grid(
            row=2,
            column=0,
            padx=(20, 15),
            pady=7,
            sticky="w"
        )

        gender_combo = ttk.Combobox(
            form_frame,
            textvariable=self.gender_var,
            values=[
                "Male",
                "Female",
                "Other"
            ],
            state="readonly",
            width=35
        )

        gender_combo.grid(
            row=2,
            column=1,
            padx=(0, 20),
            pady=7,
            sticky="ew"
        )

        # ----------------------------------------------------
        # DATE OF BIRTH
        # ----------------------------------------------------

        create_label_entry(
            3,
            "Date of Birth",
            self.dob_var
        )

        # ----------------------------------------------------
        # EMAIL
        # ----------------------------------------------------

        create_label_entry(
            4,
            "Email",
            self.email_var
        )

        # ----------------------------------------------------
        # PHONE
        # ----------------------------------------------------

        create_label_entry(
            5,
            "Phone",
            self.phone_var
        )

        # ----------------------------------------------------
        # ADDRESS
        # ----------------------------------------------------

        create_label_entry(
            6,
            "Address",
            self.address_var
        )

        # ----------------------------------------------------
        # COURSE
        # ----------------------------------------------------

        tk.Label(
            form_frame,
            text="Course",
            font=("Arial", 9, "bold"),
            bg=WHITE,
            fg=TEXT_DARK
        ).grid(
            row=7,
            column=0,
            padx=(20, 15),
            pady=7,
            sticky="w"
        )

        course_combo = ttk.Combobox(
            form_frame,
            textvariable=self.course_var,
            state="readonly",
            width=35
        )

        course_combo.grid(
            row=7,
            column=1,
            padx=(0, 20),
            pady=7,
            sticky="ew"
        )

        self.load_courses(
            course_combo
        )

        # ----------------------------------------------------
        # YEAR
        # ----------------------------------------------------

        tk.Label(
            form_frame,
            text="Year",
            font=("Arial", 9, "bold"),
            bg=WHITE,
            fg=TEXT_DARK
        ).grid(
            row=8,
            column=0,
            padx=(20, 15),
            pady=7,
            sticky="w"
        )

        year_combo = ttk.Combobox(
            form_frame,
            textvariable=self.year_var,
            values=[
                "1",
                "2",
                "3",
                "4"
            ],
            state="readonly",
            width=35
        )

        year_combo.grid(
            row=8,
            column=1,
            padx=(0, 20),
            pady=7,
            sticky="ew"
        )

        # ----------------------------------------------------
        # ADMISSION DATE
        # ----------------------------------------------------

        create_label_entry(
            9,
            "Admission Date",
            self.admission_date_var
        )

        # ----------------------------------------------------
        # DATE FORMAT INFO
        # ----------------------------------------------------

        date_info = tk.Label(
            form_frame,
            text="Date format: YYYY-MM-DD",
            font=("Arial", 8),
            bg=WHITE,
            fg=TEXT_LIGHT
        )

        date_info.grid(
            row=10,
            column=1,
            padx=(0, 20),
            sticky="w"
        )

        # ----------------------------------------------------
        # BUTTON FRAME
        # ----------------------------------------------------

        button_frame = tk.Frame(
            form_window,
            bg=BACKGROUND
        )

        button_frame.pack(
            fill="x",
            padx=25,
            pady=(0, 20)
        )

        # ----------------------------------------------------
        # SAVE
        # ----------------------------------------------------

        save_button = tk.Button(
            button_frame,
            text="Save Student",
            command=lambda: self.save_student(
                form_window
            ),
            font=("Arial", 10, "bold"),
            bg=PRIMARY,
            fg=WHITE,
            activebackground=PRIMARY_DARK,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=25,
            pady=9
        )

        save_button.pack(
            side="right",
            padx=5
        )

        # ----------------------------------------------------
        # CANCEL
        # ----------------------------------------------------

        cancel_button = tk.Button(
            button_frame,
            text="Cancel",
            command=form_window.destroy,
            font=("Arial", 10, "bold"),
            bg=WHITE,
            fg=TEXT_DARK,
            activebackground=PRIMARY_LIGHT,
            activeforeground=TEXT_DARK,
            relief="solid",
            bd=1,
            cursor="hand2",
            padx=25,
            pady=8
        )

        cancel_button.pack(
            side="right",
            padx=5
        )

    # ========================================================
    # LOAD COURSES
    # ========================================================

    def load_courses(
        self,
        combo
    ):

        connection = create_connection()

        if connection is None:
            return

        cursor = None

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT course_name
                FROM courses
                ORDER BY course_name
                """
            )

            courses = cursor.fetchall()

            combo["values"] = [
                course[0]
                for course in courses
            ]

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Could not load courses:\n{e}"
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

    # ========================================================
    # VALIDATE STUDENT FORM
    # ========================================================

    def validate_student_form(
        self,
        roll_no,
        name,
        dob,
        email,
        phone,
        year,
        admission_date
    ):

        # ----------------------------------------------------
        # ROLL NUMBER
        # ----------------------------------------------------

        valid, message = validate_required(
            roll_no,
            "Roll Number"
        )

        if not valid:
            return False, message

        valid, message = validate_roll_no(
            roll_no
        )

        if not valid:
            return False, message

        # ----------------------------------------------------
        # NAME
        # ----------------------------------------------------

        valid, message = validate_required(
            name,
            "Student Name"
        )

        if not valid:
            return False, message

        valid, message = validate_name(
            name
        )

        if not valid:
            return False, message

        # ----------------------------------------------------
        # DATE OF BIRTH
        # ----------------------------------------------------

        valid, message = validate_date(
            dob,
            "Date of Birth"
        )

        if not valid:
            return False, message

        # ----------------------------------------------------
        # EMAIL
        # ----------------------------------------------------

        valid, message = validate_email(
            email
        )

        if not valid:
            return False, message

        # ----------------------------------------------------
        # PHONE
        # ----------------------------------------------------

        valid, message = validate_phone(
            phone
        )

        if not valid:
            return False, message

        # ----------------------------------------------------
        # YEAR
        # ----------------------------------------------------

        valid, message = validate_year(
            year
        )

        if not valid:
            return False, message

        # ----------------------------------------------------
        # ADMISSION DATE
        # ----------------------------------------------------

        valid, message = validate_date(
            admission_date,
            "Admission Date"
        )

        if not valid:
            return False, message

        return True, ""

    # ========================================================
    # CHECK DUPLICATE ROLL NUMBER
    # ========================================================

    def roll_number_exists(
        self,
        cursor,
        roll_no
    ):

        if self.selected_student_id is None:

            cursor.execute(
                """
                SELECT id
                FROM students
                WHERE roll_no = %s
                """,
                (roll_no,)
            )

        else:

            cursor.execute(
                """
                SELECT id
                FROM students
                WHERE roll_no = %s
                AND id != %s
                """,
                (
                    roll_no,
                    self.selected_student_id
                )
            )

        result = cursor.fetchone()

        return result is not None

    # ========================================================
    # SAVE STUDENT
    # ========================================================

    def save_student(
        self,
        form_window
    ):

        roll_no = (
            self.roll_no_var
            .get()
            .strip()
        )

        name = (
            self.name_var
            .get()
            .strip()
        )

        gender = (
            self.gender_var
            .get()
            .strip()
        )

        dob = (
            self.dob_var
            .get()
            .strip()
        )

        email = (
            self.email_var
            .get()
            .strip()
        )

        phone = (
            self.phone_var
            .get()
            .strip()
        )

        address = (
            self.address_var
            .get()
            .strip()
        )

        course = (
            self.course_var
            .get()
            .strip()
        )

        year = (
            self.year_var
            .get()
            .strip()
        )

        admission_date = (
            self.admission_date_var
            .get()
            .strip()
        )

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        valid, message = self.validate_student_form(
            roll_no,
            name,
            dob,
            email,
            phone,
            year,
            admission_date
        )

        if not valid:

            messagebox.showwarning(
                "Validation Error",
                message
            )

            return

        # ----------------------------------------------------
        # DATABASE
        # ----------------------------------------------------

        connection = create_connection()

        if connection is None:

            messagebox.showerror(
                "Database Error",
                "Could not connect to database."
            )

            return

        cursor = None

        try:

            cursor = connection.cursor()

            # ------------------------------------------------
            # DUPLICATE ROLL NUMBER
            # ------------------------------------------------

            if self.roll_number_exists(
                cursor,
                roll_no
            ):

                messagebox.showwarning(
                    "Duplicate Roll Number",
                    f"Roll number '{roll_no}' already exists.\n\n"
                    "Please enter a different roll number."
                )

                return

            # ------------------------------------------------
            # GET COURSE ID
            # ------------------------------------------------

            course_id = None

            if course:

                cursor.execute(
                    """
                    SELECT id
                    FROM courses
                    WHERE course_name = %s
                    """,
                    (course,)
                )

                result = cursor.fetchone()

                if result:

                    course_id = result[0]

            # ------------------------------------------------
            # INSERT
            # ------------------------------------------------

            if self.selected_student_id is None:

                query = """
                    INSERT INTO students
                    (
                        roll_no,
                        name,
                        gender,
                        date_of_birth,
                        email,
                        phone,
                        address,
                        course_id,
                        year,
                        admission_date
                    )
                    VALUES
                    (
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s
                    )
                """

                values = (
                    roll_no,
                    name,
                    gender or None,
                    dob or None,
                    email or None,
                    phone or None,
                    address or None,
                    course_id,
                    int(year),
                    admission_date or None
                )

                cursor.execute(
                    query,
                    values
                )

                success_message = (
                    "Student added successfully."
                )

            # ------------------------------------------------
            # UPDATE
            # ------------------------------------------------

            else:

                query = """
                    UPDATE students
                    SET
                        roll_no = %s,
                        name = %s,
                        gender = %s,
                        date_of_birth = %s,
                        email = %s,
                        phone = %s,
                        address = %s,
                        course_id = %s,
                        year = %s,
                        admission_date = %s
                    WHERE id = %s
                """

                values = (
                    roll_no,
                    name,
                    gender or None,
                    dob or None,
                    email or None,
                    phone or None,
                    address or None,
                    course_id,
                    int(year),
                    admission_date or None,
                    self.selected_student_id
                )

                cursor.execute(
                    query,
                    values
                )

                success_message = (
                    "Student updated successfully."
                )

            # ------------------------------------------------
            # COMMIT
            # ------------------------------------------------

            connection.commit()

            messagebox.showinfo(
                "Success",
                success_message
            )

            form_window.destroy()

            self.selected_student_id = None

            self.load_students()

            self.load_statistics()

        except Exception as e:

            try:
                connection.rollback()
            except Exception:
                pass

            messagebox.showerror(
                "Database Error",
                f"Could not save student:\n{e}"
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

    # ========================================================
    # EDIT SELECTED STUDENT
    # ========================================================

    def edit_selected_student(
        self,
        event=None
    ):

        selected = (
            self.student_table
            .selection()
        )

        if not selected:
            return

        item = self.student_table.item(
            selected[0]
        )

        values = item["values"]

        if not values:
            return

        student_id = values[0]

        self.selected_student_id = student_id

        self.open_edit_form(
            student_id
        )

    # ========================================================
    # EDIT FORM
    # ========================================================

    def open_edit_form(
        self,
        student_id
    ):

        connection = create_connection()

        if connection is None:

            messagebox.showerror(
                "Database Error",
                "Could not connect to database."
            )

            return

        cursor = None

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    s.roll_no,
                    s.name,
                    s.gender,
                    s.date_of_birth,
                    s.email,
                    s.phone,
                    s.address,
                    c.course_name,
                    s.year,
                    s.admission_date
                FROM students s
                LEFT JOIN courses c
                    ON s.course_id = c.id
                WHERE s.id = %s
                """,
                (student_id,)
            )

            student = cursor.fetchone()

            if not student:

                messagebox.showerror(
                    "Error",
                    "Student not found."
                )

                return

            self.open_student_form(
                title="Edit Student"
            )

            self.roll_no_var.set(
                student[0] or ""
            )

            self.name_var.set(
                student[1] or ""
            )

            self.gender_var.set(
                student[2] or ""
            )

            self.dob_var.set(
                str(student[3])
                if student[3]
                else ""
            )

            self.email_var.set(
                student[4] or ""
            )

            self.phone_var.set(
                student[5] or ""
            )

            self.address_var.set(
                student[6] or ""
            )

            self.course_var.set(
                student[7] or ""
            )

            self.year_var.set(
                str(student[8])
                if student[8]
                else ""
            )

            self.admission_date_var.set(
                str(student[9])
                if student[9]
                else ""
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Could not load student:\n{e}"
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

    # ========================================================
    # DELETE STUDENT
    # ========================================================

    def delete_selected_student(self):

        selected = (
            self.student_table
            .selection()
        )

        if not selected:

            messagebox.showwarning(
                "Select Student",
                "Please select a student first."
            )

            return

        item = self.student_table.item(
            selected[0]
        )

        values = item["values"]

        if not values:
            return

        student_id = values[0]
        student_name = values[2]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete\n"
            f"{student_name}?"
        )

        if not confirm:
            return

        connection = create_connection()

        if connection is None:

            messagebox.showerror(
                "Database Error",
                "Could not connect to database."
            )

            return

        cursor = None

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                DELETE FROM students
                WHERE id = %s
                """,
                (student_id,)
            )

            connection.commit()

            messagebox.showinfo(
                "Deleted",
                "Student deleted successfully."
            )

            self.load_students()

            self.load_statistics()

        except Exception as e:

            try:
                connection.rollback()
            except Exception:
                pass

            messagebox.showerror(
                "Error",
                f"Could not delete student:\n{e}"
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

    app = StudentManagement(
        root
    )

    root.mainloop()