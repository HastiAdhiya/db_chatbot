# # database_setup.py

# import sqlite3
# import csv


# # Define the path to save the database
# db_path = 'C:\Hasti\db_chatbot\database_file.db'

# # Connect to the SQLite database (or create it if it doesn't exist)
# conn = sqlite3.connect(db_path)
# cursor = conn.cursor()

# # Create the table (if not exists)
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS users (
#     user_id INTEGER PRIMARY KEY,
#     first_name TEXT NOT NULL,
#     last_name TEXT NOT NULL,
#     email TEXT NOT NULL,
#     phone TEXT,
#     department TEXT,
#     role TEXT NOT NULL,
#     salary REAL
# )
# """)

# # Path to the CSV file (fixed typo)
# csv_file_path = 'C:\Hasti\db_chatbot\sample_data.csv'
# # Open the CSV file and read its contents
# with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
#     csvreader = csv.DictReader(csvfile)
#     for row in csvreader:
#         try:
#             # Convert salary to float, default to None if empty/invalid
#             salary = float(row['salary']) if row['salary'] else None
#             cursor.execute("""
#             INSERT OR IGNORE INTO users (user_id, first_name, last_name, email, phone, department, role, salary)
#             VALUES (?, ?, ?, ?, ?, ?, ?, ?)
#             """, (
#                 int(row['user_id']),  # Ensure integer
#                 row['first_name'] or 'Unknown',
#                 row['last_name'] or 'Unknown',
#                 row['email'] or 'unknown@example.com',
#                 row['phone'],
#                 row['department'],
#                 row['role'] or 'Unknown',
#                 salary
#             ))
#         except (ValueError, KeyError) as e:
#             print(f"Skipping row due to error: {row} - {e}")
#             continue

# # Commit the changes
# conn.commit()

# # Verify by querying the table and printing the rows
# cursor.execute("SELECT * FROM users")
# rows = cursor.fetchall()

# # Print the rows
# for row in rows:
#     print(row)

# # Close the connection
# conn.close()


# database_setup.py

import sqlite3
import csv

def setup_database(db_path, csv_file_path):
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the users table if it does not exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT,
        department TEXT,
        role TEXT NOT NULL,
        salary REAL
    )
    """)

    # Open the CSV file and insert data into the database
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            try:
                # Convert salary to float, default to None if empty/invalid
                salary = float(row['salary']) if row['salary'] else None
                cursor.execute("""
                INSERT OR IGNORE INTO users (user_id, first_name, last_name, email, phone, department, role, salary)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    int(row['user_id']),  # Ensure integer
                    row['first_name'] or 'Unknown',
                    row['last_name'] or 'Unknown',
                    row['email'] or 'unknown@example.com',
                    row['phone'],
                    row['department'],
                    row['role'] or 'Unknown',
                    salary
                ))
            except (ValueError, KeyError) as e:
                print(f"Skipping row due to error: {row} - {e}")
                continue

    # Commit the changes
    conn.commit()

    # Verify by querying the table and printing the rows
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    # Print the rows
    for row in rows:
        print(row)

    # Close the connection
    conn.close()

# Example usage:
if __name__ == "__main__":
    db_path = 'C:\Hasti\db_chatbot\database_file.db'  
    csv_file_path = 'C:\Hasti\db_chatbot\sample_data.csv' 
    setup_database(db_path, csv_file_path)