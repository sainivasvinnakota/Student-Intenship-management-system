import csv
from database import get_connection

# --- Colored text ---
def print_header(text):
    print(f"\033[1;34m{text}\033[0m")  # Blue bold text

def get_int_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("\033[1;31mInvalid input. Please enter a number.\033[0m")

def print_table(data, headers):
    row_format = "{:<5}" + "".join(["{:<20}" for _ in headers[1:]])
    print(row_format.format(*headers))
    print("-" * (5 + 20 * (len(headers) - 1)))
    for row in data:
        print(row_format.format(*row))

# --- Search helpers ---
def search_students_by_name(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE name LIKE ?", (f"%{name}%",))
    results = cursor.fetchall()
    conn.close()
    return results

def search_companies_by_name(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM companies WHERE name LIKE ?", (f"%{name}%",))
    results = cursor.fetchall()
    conn.close()
    return results

def search_internships_by_title(title):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT i.id, i.title, i.description, i.duration, i.stipend, c.name 
        FROM internships i
        JOIN companies c ON i.company_id = c.id
        WHERE i.title LIKE ?
    """, (f"%{title}%",))
    results = cursor.fetchall()
    conn.close()
    return results

# --- CSV Export ---
def export_to_csv(filename, headers, data):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)
    print(f"\033[1;32mData exported successfully to {filename}\033[0m")