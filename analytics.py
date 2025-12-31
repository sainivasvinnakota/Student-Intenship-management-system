from database import get_connection
from utils import export_to_csv, print_table, print_header

def applications_per_internship(export_csv=False):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT i.title, c.name, COUNT(a.id) as total_applications
        FROM internships i
        JOIN companies c ON i.company_id = c.id
        LEFT JOIN applications a ON i.id = a.internship_id
        GROUP BY i.id
    """)
    data = cursor.fetchall()
    print_header("\n--- Applications per Internship ---")
    print_table(data, ["Title", "Company", "Total Applications"])
    if export_csv:
        export_to_csv("applications_per_internship.csv", ["Title", "Company", "Total Applications"], data)
    conn.close()

def top_companies_by_applicants(export_csv=False):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.name, COUNT(a.id) as total_applicants
        FROM companies c
        JOIN internships i ON i.company_id = c.id
        LEFT JOIN applications a ON i.id = a.internship_id
        GROUP BY c.id
        ORDER BY total_applicants DESC
        LIMIT 5
    """)
    data = cursor.fetchall()
    print_header("\n--- Top Companies by Applicants ---")
    print_table(data, ["Company", "Total Applicants"])
    if export_csv:
        export_to_csv("top_companies_by_applicants.csv", ["Company", "Total Applicants"], data)
    conn.close()

def application_status_summary(export_csv=False):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT status, COUNT(*) FROM applications GROUP BY status")
    data = cursor.fetchall()
    print_header("\n--- Application Status Summary ---")
    print_table(data, ["Status", "Count"])
    if export_csv:
        export_to_csv("application_status_summary.csv", ["Status", "Count"], data)
    conn.close()