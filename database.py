import os

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DB_HOST = os.getenv(
    "DB_HOST",
    "localhost"
)

DB_USER = os.getenv(
    "DB_USER",
    "root"
)

DB_PASSWORD = os.getenv(
    "DB_PASSWORD",
    "suji"
)

DB_NAME = os.getenv(
    "DB_NAME",
    "student_management"
)


# ============================================================
# CREATE DATABASE CONNECTION
# ============================================================

def create_connection():

    try:

        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        if connection.is_connected():

            print(
                "MySQL database connected successfully!"
            )

            return connection

    except Error as e:

        print(
            "Database connection error:",
            e
        )

    return None


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    connection = create_connection()

    if connection:

        connection.close()

        print(
            "Database connection closed."
        )