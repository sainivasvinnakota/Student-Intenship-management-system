from database import get_connection, create_tables
from seed_data import seed_data
from analytics import applications_per_internship, top_companies_by_applicants, application_status_summary
from utils import get_int_input, print_table, search_students_by_name, search_companies_by_name, search_internships_by_title, print_header

# --- CRUD Functions ---
def view_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    print_header("\n--- Students ---")
    print_table(students, ["ID", "Name", "Email", "Phone", "Department"])
    conn.close()

def view_companies():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM companies")
    companies = cursor.fetchall()
    print_header("\n--- Companies ---")
    print_table(companies, ["ID", "Name", "Location", "Industry"])
    conn.close()

def view_internships():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT i.id, i.title, i.description, i.duration, i.stipend, c.name 
    FROM internships i 
    JOIN companies c ON i.company_id = c.id
    """)
    internships = cursor.fetchall()
    print_header("\n--- Internships ---")
    print_table(internships, ["ID", "Title", "Description", "Duration", "Stipend", "Company"])
    conn.close()

def apply_internship():
    student_id = get_int_input("Enter Student ID: ")
    internship_id = get_int_input("Enter Internship ID: ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO applications (student_id, internship_id) VALUES (?, ?)", (student_id, internship_id))
    conn.commit()
    conn.close()
    print("\033[1;32mApplication submitted successfully!\033[0m")

def view_applications():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT a.id, s.name, i.title, c.name, a.status 
    FROM applications a
    JOIN students s ON a.student_id = s.id
    JOIN internships i ON a.internship_id = i.id
    JOIN companies c ON i.company_id = c.id
    """)
    applications = cursor.fetchall()
    print_header("\n--- Applications ---")
    print_table(applications, ["ID", "Student", "Internship", "Company", "Status"])
    conn.close()

def update_application_status():
    app_id = get_int_input("Enter Application ID to update: ")
    new_status = input("Enter new status (Pending/Accepted/Rejected): ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE applications SET status = ? WHERE id = ?", (new_status, app_id))
    conn.commit()
    conn.close()
    print("\033[1;32mApplication status updated successfully!\033[0m")

# --- Analytics Menu ---
def analytics_menu():
    while True:
        print_header("\n--- Analytics Menu ---")
        print("1. Applications per Internship")
        print("2. Top Companies by Applicants")
        print("3. Application Status Summary")
        print("4. Back to Main Menu")
        choice = get_int_input("Enter your choice: ")
        if choice == 1:
            applications_per_internship(export_csv=True)
        elif choice == 2:
            top_companies_by_applicants(export_csv=True)
        elif choice == 3:
            application_status_summary(export_csv=True)
        elif choice == 4:
            break
        else:
            print("\033[1;31mInvalid choice. Try again.\033[0m")

# --- Search Menu ---
def search_menu():
    while True:
        print_header("\n--- Search Menu ---")
        print("1. Search Students by Name")
        print("2. Search Companies by Name")
        print("3. Search Internships by Title")
        print("4. Back to Main Menu")
        choice = get_int_input("Enter your choice: ")
        if choice == 1:
            name = input("Enter student name: ")
            results = search_students_by_name(name)
            if results:
                print_table(results, ["ID", "Name", "Email", "Phone", "Department"])
            else:
                print("\033[1;31mNo students found.\033[0m")
        elif choice == 2:
            name = input("Enter company name: ")
            results = search_companies_by_name(name)
            if results:
                print_table(results, ["ID", "Name", "Location", "Industry"])
            else:
                print("\033[1;31mNo companies found.\033[0m")
        elif choice == 3:
            title = input("Enter internship title: ")
            results = search_internships_by_title(title)
            if results:
                print_table(results, ["ID", "Title", "Description", "Duration", "Stipend", "Company"])
            else:
                print("\033[1;31mNo internships found.\033[0m")
        elif choice == 4:
            break
        else:
            print("\033[1;31mInvalid choice. Try again.\033[0m")

# --- Main Menu ---
def main_menu():
    create_tables()
    seed_data()
    
    while True:
        print_header("\n--- Student Internship Management ---")
        print("1. View Students")
        print("2. View Companies")
        print("3. View Internships")
        print("4. Apply for Internship")
        print("5. View Applications")
        print("6. Update Application Status")
        print("7. Analytics")
        print("8. Search")
        print("9. Exit")
        choice = get_int_input("Enter your choice: ")
        if choice == 1:
            view_students()
        elif choice == 2:
            view_companies()
        elif choice == 3:
            view_internships()
        elif choice == 4:
            apply_internship()
        elif choice == 5:
            view_applications()
        elif choice == 6:
            update_application_status()
        elif choice == 7:
            analytics_menu()
        elif choice == 8:
            search_menu()
        elif choice == 9:
            print("\033[1;34mExiting... Goodbye!\033[0m")
            break
        else:
            print("\033[1;31mInvalid choice. Try again.\033[0m")

if __name__ == "__main__":
    main_menu()