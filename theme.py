import tkinter as tk
from tkinter import ttk


# ============================================================
# APPLICATION COLORS
# ============================================================

PRIMARY = "#1F4E78"
PRIMARY_DARK = "#163A5C"
PRIMARY_LIGHT = "#DCEAF7"

SECONDARY = "#2E86C1"

SUCCESS = "#27AE60"
SUCCESS_DARK = "#1E8449"

DANGER = "#C0392B"
DANGER_DARK = "#922B21"

WARNING = "#F39C12"

INFO = "#3498DB"

BACKGROUND = "#F4F6F9"
WHITE = "#FFFFFF"

TEXT_DARK = "#1F2937"
TEXT = "#374151"
TEXT_LIGHT = "#6B7280"

BORDER = "#D1D5DB"

TABLE_HEADER = "#1F4E78"
TABLE_SELECTED = "#DCEAF7"


# ============================================================
# FONTS
# ============================================================

FONT_TITLE = ("Arial", 24, "bold")
FONT_HEADER = ("Arial", 18, "bold")
FONT_SUBTITLE = ("Arial", 11)
FONT_NORMAL = ("Arial", 10)
FONT_BOLD = ("Arial", 10, "bold")
FONT_SMALL = ("Arial", 9)
FONT_CARD_TITLE = ("Arial", 10)
FONT_CARD_VALUE = ("Arial", 20, "bold")


# ============================================================
# GENERAL WINDOW SETTINGS
# ============================================================

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700

MIN_WIDTH = 1000
MIN_HEIGHT = 600


# ============================================================
# APPLY TTK THEME
# ============================================================

def configure_styles(root):

    style = ttk.Style(root)

    # --------------------------------------------------------
    # Try modern theme
    # --------------------------------------------------------

    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    # --------------------------------------------------------
    # General Frame
    # --------------------------------------------------------

    style.configure(
        "TFrame",
        background=BACKGROUND
    )

    # --------------------------------------------------------
    # Label
    # --------------------------------------------------------

    style.configure(
        "TLabel",
        background=BACKGROUND,
        foreground=TEXT_DARK,
        font=FONT_NORMAL
    )

    # --------------------------------------------------------
    # Entry
    # --------------------------------------------------------

    style.configure(
        "TEntry",
        padding=7,
        font=FONT_NORMAL
    )

    # --------------------------------------------------------
    # Combobox
    # --------------------------------------------------------

    style.configure(
        "TCombobox",
        padding=6,
        font=FONT_NORMAL
    )

    # --------------------------------------------------------
    # Buttons
    # --------------------------------------------------------

    style.configure(
        "TButton",
        padding=(12, 7),
        font=FONT_BOLD
    )

    style.map(
        "TButton",
        background=[
            ("active", PRIMARY_LIGHT)
        ]
    )

    # --------------------------------------------------------
    # Treeview
    # --------------------------------------------------------

    style.configure(
        "Treeview",
        background=WHITE,
        foreground=TEXT_DARK,
        fieldbackground=WHITE,
        font=FONT_NORMAL,
        rowheight=32,
        borderwidth=0
    )

    style.configure(
        "Treeview.Heading",
        background=TABLE_HEADER,
        foreground=WHITE,
        font=FONT_BOLD,
        padding=8
    )

    style.map(
        "Treeview",
        background=[
            ("selected", TABLE_SELECTED)
        ],
        foreground=[
            ("selected", PRIMARY_DARK)
        ]
    )

    # --------------------------------------------------------
    # Scrollbar
    # --------------------------------------------------------

    style.configure(
        "Vertical.TScrollbar",
        width=12
    )

    style.configure(
        "Horizontal.TScrollbar",
        height=12
    )


# ============================================================
# APPLY ROOT WINDOW SETTINGS
# ============================================================

def configure_window(root, title="Student Management System"):

    root.title(title)

    root.geometry(
        f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
    )

    root.minsize(
        MIN_WIDTH,
        MIN_HEIGHT
    )

    root.configure(
        bg=BACKGROUND
    )

    configure_styles(root)


# ============================================================
# PROFESSIONAL BUTTON CREATOR
# ============================================================

def create_button(
    parent,
    text,
    command,
    bg=PRIMARY,
    fg=WHITE,
    width=12
):

    button = tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg,
        fg=fg,
        activebackground=PRIMARY_DARK,
        activeforeground=WHITE,
        font=FONT_BOLD,
        width=width,
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=8,
        pady=7
    )

    return button


# ============================================================
# CARD CREATOR
# ============================================================

def create_stat_card(
    parent,
    title,
    value="0"
):

    card = tk.Frame(
        parent,
        bg=WHITE,
        bd=1,
        relief="solid"
    )

    title_label = tk.Label(
        card,
        text=title,
        font=FONT_CARD_TITLE,
        bg=WHITE,
        fg=TEXT_LIGHT
    )

    title_label.pack(
        pady=(12, 3)
    )

    value_label = tk.Label(
        card,
        text=value,
        font=FONT_CARD_VALUE,
        bg=WHITE,
        fg=PRIMARY
    )

    value_label.pack(
        pady=(0, 12)
    )

    return card, value_label


# ============================================================
# HEADER CREATOR
# ============================================================

def create_header(
    parent,
    title,
    subtitle=""
):

    header = tk.Frame(
        parent,
        bg=PRIMARY,
        height=75
    )

    header.pack(
        fill="x"
    )

    header.pack_propagate(
        False
    )

    title_label = tk.Label(
        header,
        text=title,
        font=FONT_TITLE,
        bg=PRIMARY,
        fg=WHITE
    )

    title_label.pack(
        side="left",
        padx=30
    )

    if subtitle:

        subtitle_label = tk.Label(
            header,
            text=subtitle,
            font=FONT_SUBTITLE,
            bg=PRIMARY,
            fg="#D9EAF7"
        )

        subtitle_label.pack(
            side="right",
            padx=30
        )

    return header


# ============================================================
# SECTION TITLE
# ============================================================

def create_section_title(
    parent,
    text
):

    label = tk.Label(
        parent,
        text=text,
        font=FONT_HEADER,
        bg=BACKGROUND,
        fg=PRIMARY
    )

    return label


# ============================================================
# SIDEBAR BUTTON
# ============================================================

def create_sidebar_button(
    parent,
    text,
    command
):

    button = tk.Button(
        parent,
        text=text,
        command=command,
        bg=PRIMARY_DARK,
        fg=WHITE,
        activebackground=PRIMARY,
        activeforeground=WHITE,
        font=("Arial", 11, "bold"),
        anchor="w",
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=20,
        pady=12
    )

    return button


# ============================================================
# MESSAGE COLORS
# ============================================================

MESSAGE_SUCCESS = SUCCESS
MESSAGE_ERROR = DANGER
MESSAGE_WARNING = WARNING
MESSAGE_INFO = INFO


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    configure_window(
        root,
        "Student Management System - Theme Test"
    )

    # Header
    create_header(
        root,
        "Student Management System",
        "Professional UI Theme"
    )

    # Main
    main_frame = tk.Frame(
        root,
        bg=BACKGROUND
    )

    main_frame.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=30
    )

    # Section title
    title = create_section_title(
        main_frame,
        "Dashboard Preview"
    )

    title.pack(
        anchor="w",
        pady=(0, 15)
    )

    # Cards
    cards_frame = tk.Frame(
        main_frame,
        bg=BACKGROUND
    )

    cards_frame.pack(
        fill="x"
    )

    cards = [
        ("Total Students", "125"),
        ("Courses", "8"),
        ("Departments", "4"),
        ("Attendance", "92%")
    ]

    for title_text, value in cards:

        card, value_label = create_stat_card(
            cards_frame,
            title_text,
            value
        )

        card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5
        )

    # Buttons
    button_frame = tk.Frame(
        main_frame,
        bg=BACKGROUND
    )

    button_frame.pack(
        pady=30
    )

    create_button(
        button_frame,
        "Primary",
        lambda: None
    ).pack(
        side="left",
        padx=5
    )

    create_button(
        button_frame,
        "Success",
        lambda: None,
        bg=SUCCESS
    ).pack(
        side="left",
        padx=5
    )

    create_button(
        button_frame,
        "Delete",
        lambda: None,
        bg=DANGER
    ).pack(
        side="left",
        padx=5
    )

    root.mainloop()