import re
from datetime import datetime


# ============================================================
# REQUIRED FIELD VALIDATION
# ============================================================

def validate_required(value, field_name):
    """
    Checks whether a field contains a value.
    """

    if value is None:
        return False, f"{field_name} is required."

    value = str(value).strip()

    if value == "":
        return False, f"{field_name} is required."

    return True, ""


# ============================================================
# NAME VALIDATION
# ============================================================

def validate_name(name):
    """
    Allows letters, spaces, dots and apostrophes.
    """

    name = str(name).strip()

    if name == "":
        return False, "Name is required."

    if len(name) < 2:
        return False, "Name must contain at least 2 characters."

    if len(name) > 100:
        return False, "Name must not exceed 100 characters."

    pattern = r"^[A-Za-z .']+$"

    if not re.match(pattern, name):
        return False, "Name can contain only letters, spaces, dots and apostrophes."

    return True, ""


# ============================================================
# ROLL NUMBER VALIDATION
# ============================================================

def validate_roll_no(roll_no):
    """
    Validates student roll number.
    """

    roll_no = str(roll_no).strip()

    if roll_no == "":
        return False, "Roll number is required."

    if len(roll_no) > 30:
        return False, "Roll number must not exceed 30 characters."

    if " " in roll_no:
        return False, "Roll number must not contain spaces."

    return True, ""


# ============================================================
# EMAIL VALIDATION
# ============================================================

def validate_email(email):
    """
    Validates email address.
    """

    email = str(email).strip()

    if email == "":
        return True, ""

    if len(email) > 100:
        return False, "Email must not exceed 100 characters."

    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    if not re.match(pattern, email):
        return False, "Please enter a valid email address."

    return True, ""


# ============================================================
# PHONE VALIDATION
# ============================================================

def validate_phone(phone):
    """
    Validates phone number.
    """

    phone = str(phone).strip()

    if phone == "":
        return True, ""

    if not phone.isdigit():
        return False, "Phone number must contain only digits."

    if len(phone) != 10:
        return False, "Phone number must contain exactly 10 digits."

    return True, ""


# ============================================================
# DATE VALIDATION
# ============================================================

def validate_date(date_text, field_name="Date"):
    """
    Validates date in YYYY-MM-DD format.
    """

    date_text = str(date_text).strip()

    if date_text == "":
        return True, ""

    try:

        datetime.strptime(
            date_text,
            "%Y-%m-%d"
        )

        return True, ""

    except ValueError:

        return False, (
            f"{field_name} must be in YYYY-MM-DD format."
        )


# ============================================================
# YEAR VALIDATION
# ============================================================

def validate_year(year):
    """
    Validates academic year.
    """

    year = str(year).strip()

    if year == "":
        return False, "Academic year is required."

    try:

        year_number = int(year)

    except ValueError:

        return False, "Academic year must be a number."

    if year_number not in [1, 2, 3, 4]:

        return False, "Academic year must be between 1 and 4."

    return True, ""


# ============================================================
# MARKS VALIDATION
# ============================================================

def validate_marks(marks, max_marks):
    """
    Validates marks obtained and maximum marks.
    """

    marks = str(marks).strip()
    max_marks = str(max_marks).strip()

    if marks == "":
        return False, "Marks are required."

    if max_marks == "":
        return False, "Maximum marks are required."

    try:

        marks_value = float(marks)
        max_marks_value = float(max_marks)

    except ValueError:

        return False, "Marks must contain numeric values."

    if max_marks_value <= 0:
        return False, "Maximum marks must be greater than 0."

    if marks_value < 0:
        return False, "Marks cannot be negative."

    if marks_value > max_marks_value:
        return False, "Marks cannot be greater than maximum marks."

    return True, ""


# ============================================================
# SUBJECT VALIDATION
# ============================================================

def validate_subject(subject):
    """
    Validates subject name.
    """

    subject = str(subject).strip()

    if subject == "":
        return False, "Subject is required."

    if len(subject) > 100:
        return False, "Subject must not exceed 100 characters."

    return True, ""


# ============================================================
# ATTENDANCE STATUS VALIDATION
# ============================================================

def validate_attendance_status(status):
    """
    Validates attendance status.
    """

    status = str(status).strip()

    if status not in ["Present", "Absent"]:
        return False, "Attendance status must be Present or Absent."

    return True, ""


# ============================================================
# GENERAL VALIDATION TEST
# ============================================================

def run_validation_tests():

    print("=" * 60)
    print("VALIDATION MODULE TEST")
    print("=" * 60)

    # Name
    print("\nName Tests:")

    print(
        validate_name("Surendra Kumar")
    )

    print(
        validate_name("12345")
    )

    # Roll number
    print("\nRoll Number Tests:")

    print(
        validate_roll_no("239X1A0501")
    )

    print(
        validate_roll_no("")
    )

    # Email
    print("\nEmail Tests:")

    print(
        validate_email("student@gmail.com")
    )

    print(
        validate_email("wrong-email")
    )

    # Phone
    print("\nPhone Tests:")

    print(
        validate_phone("9876543210")
    )

    print(
        validate_phone("12345")
    )

    # Date
    print("\nDate Tests:")

    print(
        validate_date("2026-09-30")
    )

    print(
        validate_date("30-09-2026")
    )

    # Year
    print("\nYear Tests:")

    print(
        validate_year("3")
    )

    print(
        validate_year("5")
    )

    # Marks
    print("\nMarks Tests:")

    print(
        validate_marks("85", "100")
    )

    print(
        validate_marks("120", "100")
    )

    # Subject
    print("\nSubject Tests:")

    print(
        validate_subject("Data Structures")
    )

    print(
        validate_subject("")
    )

    # Attendance
    print("\nAttendance Tests:")

    print(
        validate_attendance_status("Present")
    )

    print(
        validate_attendance_status("Invalid")
    )

    print("\n" + "=" * 60)
    print("VALIDATION TEST COMPLETED")
    print("=" * 60)


# ============================================================
# RUN DIRECTLY
# ============================================================

if __name__ == "__main__":

    run_validation_tests()