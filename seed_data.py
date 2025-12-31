from database import get_connection

def seed_data():
    conn = get_connection()
    cursor = conn.cursor()

    # Seed Students
    cursor.execute("SELECT COUNT(*) FROM students")
    if cursor.fetchone()[0] == 0:
        students = [
            ("Alice", "alice@example.com", "1234567890", "CSE"),
            ("Bob", "bob@example.com", "9876543210", "ECE")
        ]
        cursor.executemany("INSERT INTO students (name, email, phone, department) VALUES (?, ?, ?, ?)", students)

    # Seed Companies
    cursor.execute("SELECT COUNT(*) FROM companies")
    if cursor.fetchone()[0] == 0:
        companies = [
            ("TechCorp", "New York", "IT"),
            ("InnoSoft", "San Francisco", "Software")
        ]
        cursor.executemany("INSERT INTO companies (name, location, industry) VALUES (?, ?, ?)", companies)

    # Seed Internships
    cursor.execute("SELECT COUNT(*) FROM internships")
    if cursor.fetchone()[0] == 0:
        internships = [
    ("Python Developer", "Work on Python projects", "3 months", 1000, 1),
    ("Data Analyst", "Analyze datasets", "2 months", 800, 2),
    ("Web Developer Intern", "Assist in frontend and backend development using Flask and React", "3 months", 1200, 1),
    ("Machine Learning Intern", "Build ML models for predictive analytics", "4 months", 1500, 2),
    ("UI/UX Designer Intern", "Design user interfaces and improve user experience", "2 months", 900, 1),
    ("Cloud Computing Intern", "Deploy and manage cloud resources on AWS", "3 months", 1400, 2),
    ("Cybersecurity Intern", "Work on vulnerability testing and network monitoring", "3 months", 1000, 1),
    ("Mobile App Developer Intern", "Build Android apps using Flutter", "4 months", 1300, 2),
    ("DevOps Intern", "Automate workflows and CI/CD pipelines", "3 months", 1100, 1),
    ("AI Research Intern", "Explore applications of AI in automation", "5 months", 1600, 2)
]
        cursor.executemany("INSERT INTO internships (title, description, duration, stipend, company_id) VALUES (?, ?, ?, ?, ?)", internships)

    conn.commit()
    conn.close()
    print("Sample data seeded successfully!")