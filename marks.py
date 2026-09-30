import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

from database import create_connection

from validation import (
    validate_required,
    validate_marks,
    validate_subject
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
    configure_window
)


class MarksManagement:

    def __init__(self, root):

        self.root = root

        # ====================================================
        # WINDOW
        # ====================================================

        configure_window(
            self.root,
            "Student Management System - Marks & Results"
        )

        self.root.geometry("1250x720")
        self.root.minsize(1100, 650)

        # ====================================================
        # VARIABLES
        # ====================================================

        self.selected_id = None

        # ====================================================
        # CREATE UI
        # ====================================================

        self.create_styles()
        self.create_header()
        self.create_statistics()
        self.create_marks_form()
        self.create_search_area()
        self.create_marks_table()

        # ====================================================
        # LOAD DATA
        # ====================================================

        self.load_students()
        self.load_marks()
        self.load_statistics()

    # ========================================================
    # STYLES
    # ========================================================

    def create_styles(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "Marks.Treeview",
            background=WHITE,
            foreground=TEXT_DARK,
            rowheight=36,
            fieldbackground=WHITE,
            font=("Arial", 10),
            borderwidth=0
        )

        style.configure(
            "Marks.Treeview.Heading",
            background=PRIMARY,
            foreground=WHITE,
            font=("Arial", 10, "bold"),
            padding=9,
            relief="flat"
        )

        style.map(
            "Marks.Treeview",
            background=[
                ("selected", PRIMARY_LIGHT)
            ],
            foreground=[
                ("selected", TEXT_DARK)
            ]
        )

        style.configure(
            "Marks.TCombobox",
            font=("Arial", 10),
            padding=6
        )

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

        header.pack_propagate(
            False
        )

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

        # ----------------------------------------------------
        # LOGO
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        title_frame = tk.Frame(
            left_frame,
            bg=WHITE
        )

        title_frame.pack(
            side="left"
        )

        title = tk.Label(
            title_frame,
            text="Marks & Results Management",
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
            text="Manage student marks and academic results",
            font=("Arial", 9),
            bg=WHITE,
            fg=TEXT_LIGHT
        )

        subtitle.pack(
            anchor="w"
        )

        # ----------------------------------------------------
        # RIGHT SIDE
        # ----------------------------------------------------

        info_label = tk.Label(
            header,
            text="Academic Performance Records",
            font=("Arial", 10),
            bg=WHITE,
            fg=TEXT_LIGHT
        )

        info_label.pack(
            side="right",
            padx=25
        )

    # ========================================================
    # STATISTICS
    # ========================================================

    def create_statistics(self):

        stats_frame = tk.Frame(
            self.root,
            bg=BACKGROUND
        )

        stats_frame.pack(
            fill="x",
            padx=25,
            pady=(18, 10)
        )

        self.total_records_label = (
            self.create_stat_card(
                stats_frame,
                "TOTAL RECORDS",
                "0",
                PRIMARY
            )
        )

        self.students_marks_label = (
            self.create_stat_card(
                stats_frame,
                "STUDENTS WITH MARKS",
                "0",
                SUCCESS
            )
        )

        self.average_marks_label = (
            self.create_stat_card(
                stats_frame,
                "AVERAGE PERCENTAGE",
                "0%",
                "#2E86C1"
            )
        )

        self.subjects_label = (
            self.create_stat_card(
                stats_frame,
                "SUBJECTS",
                "0",
                "#8E44AD"
            )
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
            pady=6
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
    # MARKS FORM
    # ========================================================

    def create_marks_form(self):

        form_outer = tk.Frame(
            self.root,
            bg=WHITE,
            bd=1,
            relief="solid"
        )

        form_outer.pack(
            fill="x",
            padx=25,
            pady=(5, 12)
        )

        # ----------------------------------------------------
        # FORM TITLE
        # ----------------------------------------------------

        form_title = tk.Label(
            form_outer,
            text="Enter Marks Details",
            font=("Arial", 12, "bold"),
            bg=WHITE,
            fg=TEXT_DARK
        )

        form_title.grid(
            row=0,
            column=0,
            columnspan=8,
            padx=20,
            pady=(14, 8),
            sticky="w"
        )

        # ----------------------------------------------------
        # STUDENT
        # ----------------------------------------------------

        student_label = tk.Label(
            form_outer,
            text="Student *",
            font=("Arial", 9, "bold"),
            bg=WHITE,
            fg=TEXT_DARK
        )

        student_label.grid(
            row=1,
            column=0,
            padx=(20, 8),
            pady=(0, 5),
            sticky="w"
        )

        self.student_var = tk.StringVar()

        self.student_combo = ttk.Combobox(
            form_outer,
            textvariable=self.student_var,
            width=29,
            state="readonly",
            font=("Arial", 10)
        )

        self.student_combo.grid(
            row=2,
            column=0,
            padx=(20, 8),
            pady=(0, 15)
        )

        # ----------------------------------------------------
        # SUBJECT
        # ----------------------------------------------------

        subject_label = tk.Label(
            form_outer,
            text="Subject *",
            font=("Arial", 9, "bold"),
            bg=WHITE,
            fg=TEXT_DARK
        )

        subject_label.grid(
            row=1,
            column=1,
            padx=8,
            pady=(0, 5),
            sticky="w"
        )

        subject_frame = tk.Frame(
            form_outer,
            bg=BORDER
        )

        subject_frame.grid(
            row=2,
            column=1,
            padx=8,
            pady=(0, 15)
        )

        self.subject_var = tk.StringVar()

        self.subject_entry = tk.Entry(
            subject_frame,
            textvariable=self.subject_var,
            font=("Arial", 10),
            bg=WHITE,
            fg=TEXT_DARK,
            insertbackground=PRIMARY,
            relief="flat",
            bd=0,
            width=24
        )

        self.subject_entry.pack(
            padx=1,
            pady=1,
            ipady=6
        )

        # ----------------------------------------------------
        # MARKS
        # ----------------------------------------------------

        marks_label = tk.Label(
            form_outer,
            text="Marks Obtained *",
            font=("Arial", 9, "bold"),
            bg=WHITE,
            fg=TEXT_DARK
        )

        marks_label.grid(
            row=1,
            column=2,
            padx=8,
            pady=(0, 5),
            sticky="w"
        )

        marks_frame = tk.Frame(
            form_outer,
            bg=BORDER
        )

        marks_frame.grid(
            row=2,
            column=2,
            padx=8,
            pady=(0, 15)
        )

        self.marks_var = tk.StringVar()

        self.marks_entry = tk.Entry(
            marks_frame,
            textvariable=self.marks_var,
            font=("Arial", 10),
            bg=WHITE,
            fg=TEXT_DARK,
            insertbackground=PRIMARY,
            relief="flat",
            bd=0,
            width=15
        )

        self.marks_entry.pack(
            padx=1,
            pady=1,
            ipady=6
        )

        # ----------------------------------------------------
        # MAX MARKS
        # ----------------------------------------------------

        max_marks_label = tk.Label(
            form_outer,
            text="Maximum Marks *",
            font=("Arial", 9, "bold"),
            bg=WHITE,
            fg=TEXT_DARK
        )

        max_marks_label.grid(
            row=1,
            column=3,
            padx=8,
            pady=(0, 5),
            sticky="w"
        )

        max_marks_frame = tk.Frame(
            form_outer,
            bg=BORDER
        )

        max_marks_frame.grid(
            row=2,
            column=3,
            padx=8,
            pady=(0, 15)
        )

        self.max_marks_var = tk.StringVar(
            value="100"
        )

        self.max_marks_entry = tk.Entry(
            max_marks_frame,
            textvariable=self.max_marks_var,
            font=("Arial", 10),
            bg=WHITE,
            fg=TEXT_DARK,
            insertbackground=PRIMARY,
            relief="flat",
            bd=0,
            width=15
        )

        self.max_marks_entry.pack(
            padx=1,
            pady=1,
            ipady=6
        )

        # ----------------------------------------------------
        # SAVE / UPDATE
        # ----------------------------------------------------

        self.save_button = tk.Button(
            form_outer,
            text="Save Marks",
            command=self.save_marks,
            font=("Arial", 9, "bold"),
            bg=PRIMARY,
            fg=WHITE,
            activebackground=PRIMARY_DARK,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=18,
            pady=8
        )

        self.save_button.grid(
            row=2,
            column=4,
            padx=(15, 5),
            pady=(0, 15)
        )

        # ----------------------------------------------------
        # CLEAR
        # ----------------------------------------------------

        clear_button = tk.Button(
            form_outer,
            text="Clear",
            command=self.clear_form,
            font=("Arial", 9, "bold"),
            bg=WHITE,
            fg=TEXT_DARK,
            activebackground=PRIMARY_LIGHT,
            activeforeground=TEXT_DARK,
            relief="solid",
            bd=1,
            cursor="hand2",
            padx=18,
            pady=7
        )

        clear_button.grid(
            row=2,
            column=5,
            padx=5,
            pady=(0, 15)
        )

        # ----------------------------------------------------
        # INFO
        # ----------------------------------------------------

        info_label = tk.Label(
            form_outer,
            text="Double-click a record below to edit",
            font=("Arial", 8),
            bg=WHITE,
            fg=TEXT_LIGHT
        )

        info_label.grid(
            row=3,
            column=0,
            columnspan=6,
            padx=20,
            pady=(0, 10),
            sticky="w"
        )

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
            pady=(0, 10)
        )

        # ----------------------------------------------------
        # LABEL
        # ----------------------------------------------------

        search_label = tk.Label(
            search_outer,
            text="Search Marks",
            font=("Arial", 12, "bold"),
            bg=BACKGROUND,
            fg=TEXT_DARK
        )

        search_label.pack(
            side="left",
            padx=(0, 12)
        )

        # ----------------------------------------------------
        # ENTRY
        # ----------------------------------------------------

        search_frame = tk.Frame(
            search_outer,
            bg=BORDER
        )

        search_frame.pack(
            side="left"
        )

        self.search_var = tk.StringVar()

        self.search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Arial", 10),
            bg=WHITE,
            fg=TEXT_DARK,
            insertbackground=PRIMARY,
            relief="flat",
            bd=0,
            width=35
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
            command=self.search_marks,
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
        # REFRESH
        # ----------------------------------------------------

        refresh_button = tk.Button(
            search_outer,
            text="Refresh",
            command=self.refresh_marks,
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
        # DELETE
        # ----------------------------------------------------

        delete_button = tk.Button(
            search_outer,
            text="Delete Selected",
            command=self.delete_marks,
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
            side="right"
        )

        # ----------------------------------------------------
        # ENTER KEY
        # ----------------------------------------------------

        self.search_entry.bind(
            "<Return>",
            lambda event: self.search_marks()
        )

    # ========================================================
    # TABLE
    # ========================================================

    def create_marks_table(self):

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
            "subject",
            "marks",
            "max_marks",
            "percentage",
            "grade"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
            style="Marks.Treeview"
        )

        headings = {
            "id": "ID",
            "roll_no": "Roll No",
            "name": "Student Name",
            "subject": "Subject",
            "marks": "Marks",
            "max_marks": "Max Marks",
            "percentage": "Percentage",
            "grade": "Grade"
        }

        widths = {
            "id": 55,
            "roll_no": 125,
            "name": 210,
            "subject": 180,
            "marks": 100,
            "max_marks": 110,
            "percentage": 120,
            "grade": 90
        }

        for column in columns:

            self.tree.heading(
                column,
                text=headings[column]
            )

            self.tree.column(
                column,
                width=widths[column],
                anchor="center"
            )

        self.tree.column(
            "name",
            anchor="w"
        )

        self.tree.column(
            "subject",
            anchor="w"
        )

        # ----------------------------------------------------
        # SCROLLBAR
        # ----------------------------------------------------

        vertical_scroll = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=vertical_scroll.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        vertical_scroll.pack(
            side="right",
            fill="y"
        )

        # ----------------------------------------------------
        # DOUBLE CLICK EDIT
        # ----------------------------------------------------

        self.tree.bind(
            "<Double-1>",
            self.edit_marks
        )

    # ========================================================
    # LOAD STUDENTS
    # ========================================================

    def load_students(self):

        connection = None
        cursor = None

        try:

            connection = create_connection()

            if not connection:

                messagebox.showerror(
                    "Database Error",
                    "Unable to connect to database."
                )

                return

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    roll_no,
                    name
                FROM students
                ORDER BY roll_no
                """
            )

            students = cursor.fetchall()

            values = []

            for student_id, roll_no, name in students:

                values.append(
                    f"{student_id} | {roll_no} | {name}"
                )

            self.student_combo["values"] = values

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load students.\n\n{e}"
            )

        finally:

            if cursor:

                try:
                    cursor.close()
                except Exception:
                    pass

            if connection:

                try:
                    connection.close()
                except Exception:
                    pass

    # ========================================================
    # VALIDATE FORM
    # ========================================================

    def validate_form(self):

        student = (
            self.student_var
            .get()
            .strip()
        )

        subject = (
            self.subject_var
            .get()
            .strip()
        )

        marks = (
            self.marks_var
            .get()
            .strip()
        )

        max_marks = (
            self.max_marks_var
            .get()
            .strip()
        )

        # ----------------------------------------------------
        # STUDENT
        # ----------------------------------------------------

        valid, message = validate_required(
            student,
            "Student"
        )

        if not valid:

            messagebox.showwarning(
                "Validation Error",
                message
            )

            return False

        # ----------------------------------------------------
        # SUBJECT
        # ----------------------------------------------------

        valid, message = validate_subject(
            subject
        )

        if not valid:

            messagebox.showwarning(
                "Validation Error",
                message
            )

            self.subject_entry.focus()

            return False

        # ----------------------------------------------------
        # MARKS
        # ----------------------------------------------------

        valid, message = validate_marks(
            marks,
            max_marks
        )

        if not valid:

            messagebox.showwarning(
                "Validation Error",
                message
            )

            self.marks_entry.focus()

            return False

        return True

    # ========================================================
    # GET STUDENT ID
    # ========================================================

    def get_student_id(self):

        student_text = (
            self.student_var
            .get()
            .strip()
        )

        if not student_text:
            return None

        try:

            return int(
                student_text
                .split("|")[0]
                .strip()
            )

        except (
            ValueError,
            IndexError
        ):

            return None

    # ========================================================
    # DUPLICATE CHECK
    # ========================================================

    def duplicate_exists(
        self,
        student_id,
        subject,
        exclude_id=None
    ):

        connection = None
        cursor = None

        try:

            connection = create_connection()

            if not connection:
                return False

            cursor = connection.cursor()

            if exclude_id:

                cursor.execute(
                    """
                    SELECT id
                    FROM marks
                    WHERE student_id = %s
                    AND LOWER(TRIM(subject))
                        = LOWER(TRIM(%s))
                    AND id != %s
                    """,
                    (
                        student_id,
                        subject,
                        exclude_id
                    )
                )

            else:

                cursor.execute(
                    """
                    SELECT id
                    FROM marks
                    WHERE student_id = %s
                    AND LOWER(TRIM(subject))
                        = LOWER(TRIM(%s))
                    """,
                    (
                        student_id,
                        subject
                    )
                )

            result = cursor.fetchone()

            return result is not None

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to check duplicate marks.\n\n{e}"
            )

            return False

        finally:

            if cursor:

                try:
                    cursor.close()
                except Exception:
                    pass

            if connection:

                try:
                    connection.close()
                except Exception:
                    pass

    # ========================================================
    # SAVE / UPDATE MARKS
    # ========================================================

    def save_marks(self):

        if not self.validate_form():
            return

        student_id = self.get_student_id()

        if not student_id:

            messagebox.showwarning(
                "Validation Error",
                "Invalid student selection."
            )

            return

        subject = (
            self.subject_var
            .get()
            .strip()
        )

        marks = (
            self.marks_var
            .get()
            .strip()
        )

        max_marks = (
            self.max_marks_var
            .get()
            .strip()
        )

        # ----------------------------------------------------
        # DUPLICATE
        # ----------------------------------------------------

        if self.duplicate_exists(
            student_id,
            subject,
            self.selected_id
        ):

            messagebox.showwarning(
                "Duplicate Record",
                "Marks for this student and subject "
                "already exist."
            )

            return

        connection = None
        cursor = None

        try:

            connection = create_connection()

            if not connection:

                messagebox.showerror(
                    "Database Error",
                    "Unable to connect to database."
                )

                return

            cursor = connection.cursor()

            if self.selected_id:

                cursor.execute(
                    """
                    UPDATE marks
                    SET
                        student_id = %s,
                        subject = %s,
                        marks = %s,
                        max_marks = %s
                    WHERE id = %s
                    """,
                    (
                        student_id,
                        subject,
                        float(marks),
                        float(max_marks),
                        self.selected_id
                    )
                )

                success_message = (
                    "Marks updated successfully."
                )

            else:

                cursor.execute(
                    """
                    INSERT INTO marks
                    (
                        student_id,
                        subject,
                        marks,
                        max_marks
                    )
                    VALUES
                    (
                        %s,
                        %s,
                        %s,
                        %s
                    )
                    """,
                    (
                        student_id,
                        subject,
                        float(marks),
                        float(max_marks)
                    )
                )

                success_message = (
                    "Marks saved successfully."
                )

            connection.commit()

            messagebox.showinfo(
                "Success",
                success_message
            )

            self.clear_form()
            self.load_marks()
            self.load_statistics()

        except Exception as e:

            if connection:

                try:
                    connection.rollback()
                except Exception:
                    pass

            messagebox.showerror(
                "Database Error",
                f"Unable to save marks.\n\n{e}"
            )

        finally:

            if cursor:

                try:
                    cursor.close()
                except Exception:
                    pass

            if connection:

                try:
                    connection.close()
                except Exception:
                    pass

    # ========================================================
    # LOAD MARKS
    # ========================================================

    def load_marks(
        self,
        search_text=""
    ):

        connection = None
        cursor = None

        try:

            connection = create_connection()

            if not connection:

                messagebox.showerror(
                    "Database Error",
                    "Unable to connect to database."
                )

                return

            cursor = connection.cursor()

            if search_text:

                search_pattern = (
                    f"%{search_text}%"
                )

                cursor.execute(
                    """
                    SELECT
                        m.id,
                        s.roll_no,
                        s.name,
                        m.subject,
                        m.marks,
                        m.max_marks
                    FROM marks m
                    INNER JOIN students s
                        ON m.student_id = s.id
                    WHERE
                        s.roll_no LIKE %s
                        OR s.name LIKE %s
                        OR m.subject LIKE %s
                    ORDER BY
                        m.id DESC
                    """,
                    (
                        search_pattern,
                        search_pattern,
                        search_pattern
                    )
                )

            else:

                cursor.execute(
                    """
                    SELECT
                        m.id,
                        s.roll_no,
                        s.name,
                        m.subject,
                        m.marks,
                        m.max_marks
                    FROM marks m
                    INNER JOIN students s
                        ON m.student_id = s.id
                    ORDER BY
                        m.id DESC
                    """
                )

            records = cursor.fetchall()

            # ------------------------------------------------
            # CLEAR TABLE
            # ------------------------------------------------

            for item in self.tree.get_children():

                self.tree.delete(
                    item
                )

            # ------------------------------------------------
            # INSERT RECORDS
            # ------------------------------------------------

            for record in records:

                (
                    record_id,
                    roll_no,
                    name,
                    subject,
                    marks,
                    max_marks
                ) = record

                max_marks_value = float(
                    max_marks
                )

                marks_value = float(
                    marks
                )

                if max_marks_value > 0:

                    percentage = (
                        marks_value /
                        max_marks_value
                    ) * 100

                else:

                    percentage = 0

                grade = self.calculate_grade(
                    percentage
                )

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        record_id,
                        roll_no,
                        name,
                        subject,
                        f"{marks_value:.2f}",
                        f"{max_marks_value:.2f}",
                        f"{percentage:.2f}%",
                        grade
                    )
                )

            if search_text and not records:

                messagebox.showinfo(
                    "Search Result",
                    "No marks records found."
                )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load marks.\n\n{e}"
            )

        finally:

            if cursor:

                try:
                    cursor.close()
                except Exception:
                    pass

            if connection:

                try:
                    connection.close()
                except Exception:
                    pass

    # ========================================================
    # SEARCH
    # ========================================================

    def search_marks(self):

        search_text = (
            self.search_var
            .get()
            .strip()
        )

        self.load_marks(
            search_text
        )

    # ========================================================
    # REFRESH
    # ========================================================

    def refresh_marks(self):

        self.search_var.set("")

        self.clear_form()

        self.load_students()
        self.load_marks()
        self.load_statistics()

    # ========================================================
    # CALCULATE GRADE
    # ========================================================

    def calculate_grade(
        self,
        percentage
    ):

        if percentage >= 90:
            return "A+"

        elif percentage >= 80:
            return "A"

        elif percentage >= 70:
            return "B"

        elif percentage >= 60:
            return "C"

        elif percentage >= 50:
            return "D"

        else:
            return "F"

    # ========================================================
    # EDIT MARKS
    # ========================================================

    def edit_marks(
        self,
        event=None
    ):

        selected = (
            self.tree.selection()
        )

        if not selected:
            return

        item = self.tree.item(
            selected[0]
        )

        values = item.get(
            "values",
            []
        )

        if not values:
            return

        self.selected_id = values[0]

        roll_no = values[1]
        name = values[2]
        subject = values[3]
        marks = values[4]
        max_marks = values[5]

        # ----------------------------------------------------
        # SELECT STUDENT
        # ----------------------------------------------------

        for value in (
            self.student_combo["values"]
        ):

            parts = value.split("|")

            if len(parts) >= 3:

                stored_roll = (
                    parts[1].strip()
                )

                stored_name = (
                    parts[2].strip()
                )

                if (
                    stored_roll == str(roll_no)
                    and stored_name == str(name)
                ):

                    self.student_var.set(
                        value
                    )

                    break

        # ----------------------------------------------------
        # LOAD FORM VALUES
        # ----------------------------------------------------

        self.subject_var.set(
            subject
        )

        self.marks_var.set(
            str(marks)
        )

        self.max_marks_var.set(
            str(max_marks)
        )

        self.save_button.config(
            text="Update Marks"
        )

        self.subject_entry.focus()

    # ========================================================
    # DELETE MARKS
    # ========================================================

    def delete_marks(self):

        selected = (
            self.tree.selection()
        )

        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select a marks record to delete."
            )

            return

        item = self.tree.item(
            selected[0]
        )

        values = item.get(
            "values",
            []
        )

        if not values:
            return

        record_id = values[0]

        student_name = values[2]
        subject = values[3]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this marks record?\n\n"
            f"Student: {student_name}\n"
            f"Subject: {subject}"
        )

        if not confirm:
            return

        connection = None
        cursor = None

        try:

            connection = create_connection()

            if not connection:

                messagebox.showerror(
                    "Database Error",
                    "Unable to connect to database."
                )

                return

            cursor = connection.cursor()

            cursor.execute(
                """
                DELETE FROM marks
                WHERE id = %s
                """,
                (record_id,)
            )

            if cursor.rowcount == 0:

                messagebox.showwarning(
                    "Not Found",
                    "The selected marks record "
                    "no longer exists."
                )

                return

            connection.commit()

            messagebox.showinfo(
                "Deleted",
                "Marks record deleted successfully."
            )

            self.clear_form()
            self.load_marks()
            self.load_statistics()

        except Exception as e:

            if connection:

                try:
                    connection.rollback()
                except Exception:
                    pass

            messagebox.showerror(
                "Database Error",
                f"Unable to delete marks record.\n\n{e}"
            )

        finally:

            if cursor:

                try:
                    cursor.close()
                except Exception:
                    pass

            if connection:

                try:
                    connection.close()
                except Exception:
                    pass

    # ========================================================
    # CLEAR FORM
    # ========================================================

    def clear_form(self):

        self.selected_id = None

        self.student_var.set("")

        self.subject_var.set("")

        self.marks_var.set("")

        self.max_marks_var.set(
            "100"
        )

        self.save_button.config(
            text="Save Marks"
        )

        for item in self.tree.selection():

            self.tree.selection_remove(
                item
            )

    # ========================================================
    # LOAD STATISTICS
    # ========================================================

    def load_statistics(self):

        connection = None
        cursor = None

        try:

            connection = create_connection()

            if not connection:
                return

            cursor = connection.cursor()

            # ------------------------------------------------
            # TOTAL RECORDS
            # ------------------------------------------------

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM marks
                """
            )

            total_records = (
                cursor.fetchone()[0]
            )

            # ------------------------------------------------
            # STUDENTS WITH MARKS
            # ------------------------------------------------

            cursor.execute(
                """
                SELECT COUNT(DISTINCT student_id)
                FROM marks
                """
            )

            students_with_marks = (
                cursor.fetchone()[0]
            )

            # ------------------------------------------------
            # AVERAGE PERCENTAGE
            # ------------------------------------------------

            cursor.execute(
                """
                SELECT
                    AVG(
                        (marks / max_marks) * 100
                    )
                FROM marks
                WHERE max_marks > 0
                """
            )

            average_result = (
                cursor.fetchone()[0]
            )

            if average_result is None:

                average_marks = "0.00%"

            else:

                average_marks = (
                    f"{float(average_result):.2f}%"
                )

            # ------------------------------------------------
            # SUBJECTS
            # ------------------------------------------------

            cursor.execute(
                """
                SELECT COUNT(DISTINCT subject)
                FROM marks
                """
            )

            subjects = (
                cursor.fetchone()[0]
            )

            # ------------------------------------------------
            # UPDATE CARDS
            # ------------------------------------------------

            self.total_records_label.config(
                text=str(
                    total_records
                )
            )

            self.students_marks_label.config(
                text=str(
                    students_with_marks
                )
            )

            self.average_marks_label.config(
                text=average_marks
            )

            self.subjects_label.config(
                text=str(
                    subjects
                )
            )

        except Exception as e:

            messagebox.showerror(
                "Statistics Error",
                f"Unable to load statistics.\n\n{e}"
            )

        finally:

            if cursor:

                try:
                    cursor.close()
                except Exception:
                    pass

            if connection:

                try:
                    connection.close()
                except Exception:
                    pass


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = MarksManagement(
        root
    )

    root.mainloop()