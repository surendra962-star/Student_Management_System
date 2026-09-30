import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from PIL import Image, ImageTk
import os

from database import create_connection

from validation import (
    validate_required,
    validate_date,
    validate_attendance_status
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


class AttendanceManagement:

    def __init__(self, root):

        self.root = root

        # ====================================================
        # WINDOW
        # ====================================================

        configure_window(
            self.root,
            "Student Management System - Attendance"
        )

        self.root.geometry("1250x720")
        self.root.minsize(1100, 650)

        # ====================================================
        # VARIABLES
        # ====================================================

        self.student_map = {}

        # ====================================================
        # CREATE UI
        # ====================================================

        self.create_styles()
        self.create_header()
        self.create_statistics()
        self.create_attendance_form()
        self.create_search_area()
        self.create_attendance_table()

        # ====================================================
        # LOAD DATA
        # ====================================================

        self.load_students()
        self.load_statistics()
        self.load_attendance()

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
            "Attendance.Treeview",
            background=WHITE,
            foreground=TEXT_DARK,
            rowheight=36,
            fieldbackground=WHITE,
            font=("Arial", 10),
            borderwidth=0
        )

        style.configure(
            "Attendance.Treeview.Heading",
            background=PRIMARY,
            foreground=WHITE,
            font=("Arial", 10, "bold"),
            padding=9,
            relief="flat"
        )

        style.map(
            "Attendance.Treeview",
            background=[
                ("selected", PRIMARY_LIGHT)
            ],
            foreground=[
                ("selected", TEXT_DARK)
            ]
        )

        style.configure(
            "Attendance.TCombobox",
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
            text="Attendance Management",
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
            text="Track and manage student attendance",
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
            text="Daily Attendance Records",
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

        self.total_card = self.create_stat_card(
            stats_frame,
            "TOTAL RECORDS",
            "0",
            PRIMARY
        )

        self.present_card = self.create_stat_card(
            stats_frame,
            "PRESENT",
            "0",
            SUCCESS
        )

        self.absent_card = self.create_stat_card(
            stats_frame,
            "ABSENT",
            "0",
            DANGER
        )

        self.percentage_card = self.create_stat_card(
            stats_frame,
            "ATTENDANCE %",
            "0%",
            "#2E86C1"
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
    # ATTENDANCE FORM
    # ========================================================

    def create_attendance_form(self):

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
            text="Record Attendance",
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
            text="Student",
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

        self.student_combo = ttk.Combobox(
            form_outer,
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
        # DATE
        # ----------------------------------------------------

        date_label = tk.Label(
            form_outer,
            text="Attendance Date",
            font=("Arial", 9, "bold"),
            bg=WHITE,
            fg=TEXT_DARK
        )

        date_label.grid(
            row=1,
            column=1,
            padx=8,
            pady=(0, 5),
            sticky="w"
        )

        date_frame = tk.Frame(
            form_outer,
            bg=BORDER
        )

        date_frame.grid(
            row=2,
            column=1,
            padx=8,
            pady=(0, 15)
        )

        self.date_entry = tk.Entry(
            date_frame,
            font=("Arial", 10),
            bg=WHITE,
            fg=TEXT_DARK,
            insertbackground=PRIMARY,
            relief="flat",
            bd=0,
            width=18
        )

        self.date_entry.pack(
            padx=1,
            pady=1,
            ipady=6
        )

        self.date_entry.insert(
            0,
            datetime.now().strftime(
                "%Y-%m-%d"
            )
        )

        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        status_label = tk.Label(
            form_outer,
            text="Status",
            font=("Arial", 9, "bold"),
            bg=WHITE,
            fg=TEXT_DARK
        )

        status_label.grid(
            row=1,
            column=2,
            padx=8,
            pady=(0, 5),
            sticky="w"
        )

        self.status_combo = ttk.Combobox(
            form_outer,
            values=[
                "Present",
                "Absent"
            ],
            width=15,
            state="readonly",
            font=("Arial", 10)
        )

        self.status_combo.grid(
            row=2,
            column=2,
            padx=8,
            pady=(0, 15)
        )

        self.status_combo.set(
            "Present"
        )

        # ----------------------------------------------------
        # SAVE BUTTON
        # ----------------------------------------------------

        save_button = tk.Button(
            form_outer,
            text="Save Attendance",
            command=self.save_attendance,
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

        save_button.grid(
            row=2,
            column=3,
            padx=(15, 5),
            pady=(0, 15)
        )

        # ----------------------------------------------------
        # CLEAR BUTTON
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
            column=4,
            padx=5,
            pady=(0, 15)
        )

        # ----------------------------------------------------
        # DATE FORMAT
        # ----------------------------------------------------

        date_info = tk.Label(
            form_outer,
            text="Format: YYYY-MM-DD",
            font=("Arial", 8),
            bg=WHITE,
            fg=TEXT_LIGHT
        )

        date_info.grid(
            row=3,
            column=1,
            padx=8,
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
        # SEARCH LABEL
        # ----------------------------------------------------

        search_label = tk.Label(
            search_outer,
            text="Search Attendance",
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

        search_frame = tk.Frame(
            search_outer,
            bg=BORDER
        )

        search_frame.pack(
            side="left"
        )

        self.search_entry = tk.Entry(
            search_frame,
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
            command=self.search_attendance,
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
            command=self.refresh_attendance,
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
            command=self.delete_attendance,
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
            lambda event: self.search_attendance()
        )

    # ========================================================
    # ATTENDANCE TABLE
    # ========================================================

    def create_attendance_table(self):

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
            "student_name",
            "date",
            "status"
        )

        self.attendance_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
            style="Attendance.Treeview"
        )

        # ----------------------------------------------------
        # HEADINGS
        # ----------------------------------------------------

        self.attendance_table.heading(
            "id",
            text="ID"
        )

        self.attendance_table.heading(
            "roll_no",
            text="Roll No"
        )

        self.attendance_table.heading(
            "student_name",
            text="Student Name"
        )

        self.attendance_table.heading(
            "date",
            text="Attendance Date"
        )

        self.attendance_table.heading(
            "status",
            text="Status"
        )

        # ----------------------------------------------------
        # COLUMNS
        # ----------------------------------------------------

        self.attendance_table.column(
            "id",
            width=60,
            anchor="center"
        )

        self.attendance_table.column(
            "roll_no",
            width=150,
            anchor="center"
        )

        self.attendance_table.column(
            "student_name",
            width=280,
            anchor="w"
        )

        self.attendance_table.column(
            "date",
            width=200,
            anchor="center"
        )

        self.attendance_table.column(
            "status",
            width=160,
            anchor="center"
        )

        # ----------------------------------------------------
        # SCROLLBAR
        # ----------------------------------------------------

        vertical_scroll = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.attendance_table.yview
        )

        self.attendance_table.configure(
            yscrollcommand=vertical_scroll.set
        )

        self.attendance_table.pack(
            side="left",
            fill="both",
            expand=True
        )

        vertical_scroll.pack(
            side="right",
            fill="y"
        )

    # ========================================================
    # LOAD STUDENTS
    # ========================================================

    def load_students(self):

        connection = create_connection()

        if connection is None:

            messagebox.showerror(
                "Database Error",
                "Could not connect to database while loading students."
            )

            return

        cursor = None

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    roll_no,
                    name
                FROM students
                ORDER BY name
                """
            )

            students = cursor.fetchall()

            self.student_map.clear()

            student_values = []

            for student_id, roll_no, name in students:

                display_value = (
                    f"{roll_no} - {name}"
                )

                student_values.append(
                    display_value
                )

                self.student_map[
                    display_value
                ] = student_id

            self.student_combo["values"] = (
                student_values
            )

            if not students:

                self.student_combo.set("")

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Could not load students.\n\n{e}"
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
    # SAVE ATTENDANCE
    # ========================================================

    def save_attendance(self):

        student = (
            self.student_combo
            .get()
            .strip()
        )

        attendance_date = (
            self.date_entry
            .get()
            .strip()
        )

        status = (
            self.status_combo
            .get()
            .strip()
        )

        # ----------------------------------------------------
        # STUDENT VALIDATION
        # ----------------------------------------------------

        valid, error_message = validate_required(
            student,
            "Student"
        )

        if not valid:

            messagebox.showwarning(
                "Validation Error",
                error_message
            )

            return

        # ----------------------------------------------------
        # DATE REQUIRED
        # ----------------------------------------------------

        valid, error_message = validate_required(
            attendance_date,
            "Attendance Date"
        )

        if not valid:

            messagebox.showwarning(
                "Validation Error",
                error_message
            )

            return

        # ----------------------------------------------------
        # DATE FORMAT
        # ----------------------------------------------------

        valid, error_message = validate_date(
            attendance_date,
            "Attendance Date"
        )

        if not valid:

            messagebox.showerror(
                "Invalid Date",
                error_message
            )

            return

        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        valid, error_message = validate_attendance_status(
            status
        )

        if not valid:

            messagebox.showwarning(
                "Invalid Status",
                error_message
            )

            return

        # ----------------------------------------------------
        # STUDENT ID
        # ----------------------------------------------------

        student_id = self.student_map.get(
            student
        )

        if student_id is None:

            messagebox.showerror(
                "Validation Error",
                "The selected student is invalid.\n\n"
                "Please refresh the student list and select again."
            )

            return

        # ----------------------------------------------------
        # DATABASE CONNECTION
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
            # DUPLICATE CHECK
            # ------------------------------------------------

            cursor.execute(
                """
                SELECT id
                FROM attendance
                WHERE student_id = %s
                AND attendance_date = %s
                """,
                (
                    student_id,
                    attendance_date
                )
            )

            existing = cursor.fetchone()

            if existing:

                messagebox.showwarning(
                    "Duplicate Attendance",
                    "Attendance for this student on this date "
                    "already exists."
                )

                return

            # ------------------------------------------------
            # INSERT
            # ------------------------------------------------

            cursor.execute(
                """
                INSERT INTO attendance
                (
                    student_id,
                    attendance_date,
                    status
                )
                VALUES
                (
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    student_id,
                    attendance_date,
                    status
                )
            )

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Attendance saved successfully."
            )

            self.clear_form()
            self.load_statistics()
            self.load_attendance()

        except Exception as e:

            try:
                connection.rollback()
            except Exception:
                pass

            messagebox.showerror(
                "Database Error",
                f"Could not save attendance.\n\n{e}"
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
    # LOAD ATTENDANCE
    # ========================================================

    def load_attendance(self):

        # ----------------------------------------------------
        # CLEAR TABLE
        # ----------------------------------------------------

        for item in (
            self.attendance_table
            .get_children()
        ):

            self.attendance_table.delete(
                item
            )

        connection = create_connection()

        if connection is None:

            messagebox.showerror(
                "Database Error",
                "Could not connect to database while loading attendance."
            )

            return

        cursor = None

        try:

            cursor = connection.cursor()

            query = """
                SELECT
                    a.id,
                    s.roll_no,
                    s.name,
                    a.attendance_date,
                    a.status
                FROM attendance a
                INNER JOIN students s
                    ON a.student_id = s.id
                ORDER BY
                    a.attendance_date DESC,
                    a.id DESC
            """

            cursor.execute(
                query
            )

            records = cursor.fetchall()

            for record in records:

                self.attendance_table.insert(
                    "",
                    "end",
                    values=record
                )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Could not load attendance.\n\n{e}"
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
    # SEARCH ATTENDANCE
    # ========================================================

    def search_attendance(self):

        search_text = (
            self.search_entry
            .get()
            .strip()
        )

        if not search_text:

            self.load_attendance()

            return

        # ----------------------------------------------------
        # CLEAR TABLE
        # ----------------------------------------------------

        for item in (
            self.attendance_table
            .get_children()
        ):

            self.attendance_table.delete(
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

            query = """
                SELECT
                    a.id,
                    s.roll_no,
                    s.name,
                    a.attendance_date,
                    a.status
                FROM attendance a
                INNER JOIN students s
                    ON a.student_id = s.id
                WHERE
                    s.roll_no LIKE %s
                    OR s.name LIKE %s
                    OR a.status LIKE %s
                    OR DATE_FORMAT(
                        a.attendance_date,
                        '%Y-%m-%d'
                    ) LIKE %s
                ORDER BY
                    a.attendance_date DESC,
                    a.id DESC
            """

            search_value = (
                f"%{search_text}%"
            )

            cursor.execute(
                query,
                (
                    search_value,
                    search_value,
                    search_value,
                    search_value
                )
            )

            records = cursor.fetchall()

            for record in records:

                self.attendance_table.insert(
                    "",
                    "end",
                    values=record
                )

            if not records:

                messagebox.showinfo(
                    "No Results",
                    "No attendance records found for:\n\n"
                    f"{search_text}"
                )

        except Exception as e:

            messagebox.showerror(
                "Search Error",
                f"Could not search attendance.\n\n{e}"
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
    # DELETE ATTENDANCE
    # ========================================================

    def delete_attendance(self):

        selected = (
            self.attendance_table
            .selection()
        )

        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select an attendance record."
            )

            return

        selected_item = (
            self.attendance_table.item(
                selected[0]
            )
        )

        values = selected_item[
            "values"
        ]

        if not values:

            messagebox.showerror(
                "Error",
                "Could not identify the selected attendance record."
            )

            return

        attendance_id = values[0]
        student_name = values[2]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete attendance for\n"
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
                DELETE FROM attendance
                WHERE id = %s
                """,
                (attendance_id,)
            )

            if cursor.rowcount == 0:

                messagebox.showwarning(
                    "Not Found",
                    "The selected attendance record "
                    "no longer exists."
                )

                return

            connection.commit()

            messagebox.showinfo(
                "Deleted",
                "Attendance record deleted successfully."
            )

            self.load_statistics()
            self.load_attendance()

        except Exception as e:

            try:
                connection.rollback()
            except Exception:
                pass

            messagebox.showerror(
                "Delete Error",
                f"Could not delete attendance.\n\n{e}"
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
    # LOAD STATISTICS
    # ========================================================

    def load_statistics(self):

        connection = create_connection()

        if connection is None:
            return

        cursor = None

        try:

            cursor = connection.cursor()

            # ------------------------------------------------
            # TOTAL
            # ------------------------------------------------

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM attendance
                """
            )

            total = cursor.fetchone()[0]

            # ------------------------------------------------
            # PRESENT
            # ------------------------------------------------

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM attendance
                WHERE status = 'Present'
                """
            )

            present = cursor.fetchone()[0]

            # ------------------------------------------------
            # ABSENT
            # ------------------------------------------------

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM attendance
                WHERE status = 'Absent'
                """
            )

            absent = cursor.fetchone()[0]

            # ------------------------------------------------
            # PERCENTAGE
            # ------------------------------------------------

            if total > 0:

                percentage = (
                    present / total
                ) * 100

            else:

                percentage = 0

            # ------------------------------------------------
            # UPDATE CARDS
            # ------------------------------------------------

            self.total_card.config(
                text=str(total)
            )

            self.present_card.config(
                text=str(present)
            )

            self.absent_card.config(
                text=str(absent)
            )

            self.percentage_card.config(
                text=f"{percentage:.2f}%"
            )

        except Exception as e:

            messagebox.showerror(
                "Statistics Error",
                f"Could not load attendance statistics.\n\n{e}"
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
    # CLEAR FORM
    # ========================================================

    def clear_form(self):

        self.student_combo.set(
            ""
        )

        self.date_entry.delete(
            0,
            tk.END
        )

        self.date_entry.insert(
            0,
            datetime.now().strftime(
                "%Y-%m-%d"
            )
        )

        self.status_combo.set(
            "Present"
        )

    # ========================================================
    # REFRESH
    # ========================================================

    def refresh_attendance(self):

        self.search_entry.delete(
            0,
            tk.END
        )

        self.clear_form()

        self.load_students()
        self.load_statistics()
        self.load_attendance()


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = AttendanceManagement(
        root
    )

    root.mainloop()