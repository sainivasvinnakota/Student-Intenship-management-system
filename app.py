import os
from flask import Flask, render_template, request, redirect, url_for
from database import get_connection, create_tables
from seed_data import seed_data
from flask import send_from_directory


app = Flask(__name__)

# Initialize DB and seed data
create_tables()
seed_data()

# ---------- ROUTES ---------- #

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/students")
def students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return render_template("students.html", students=students)

@app.route("/companies")
def companies():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM companies")
    companies = cursor.fetchall()
    conn.close()
    return render_template("companies.html", companies=companies)

@app.route("/internships")
def internships():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT i.id, i.title, i.description, i.duration, i.stipend, c.name
        FROM internships i
        JOIN companies c ON i.company_id = c.id
    """)
    internships = cursor.fetchall()
    conn.close()
    return render_template("internships.html", internships=internships)

@app.route("/applications")
def applications():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.id, s.name, i.title, c.name, a.status, a.resume
        FROM applications a
        JOIN students s ON a.student_id = s.id
        JOIN internships i ON a.internship_id = i.id
        JOIN companies c ON i.company_id = c.id
    """)
    applications = cursor.fetchall()
    conn.close()
    return render_template("applications.html", applications=applications)

# @app.route("/apply", methods=["GET", "POST"])
# def apply():
#     if request.method == "POST":
#         student_id = request.form["student_id"]
#         internship_id = request.form["internship_id"]

#         conn = get_connection()
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO applications (student_id, internship_id) VALUES (?, ?)",
#                        (student_id, internship_id))
#         conn.commit()
#         conn.close()

#         return render_template("apply.html", message="Application submitted successfully!")

#     return render_template("apply.html")

# @app.route("/search", methods=["GET", "POST"])
# def search():
#     results = []
#     query = ""
#     if request.method == "POST":
#         query = request.form["query"].strip()
#         conn = get_connection()
#         cursor = conn.cursor()
#         cursor.execute("""
#             SELECT 'Student' as type, name, email, department 
#             FROM students WHERE name LIKE ?
#             UNION
#             SELECT 'Company' as type, name, location, industry 
#             FROM companies WHERE name LIKE ?
#         """, (f"%{query}%", f"%{query}%"))
#         results = cursor.fetchall()
#         conn.close()
#     return render_template("search.html", results=results, query=query)


@app.route("/search", methods=["GET", "POST"])
def search():
    results = []
    columns = []
    message = ""
    category = ""

    if request.method == "POST":
        query = request.form["query"].strip()
        category = request.form["category"]

        conn = get_connection()
        cursor = conn.cursor()

        if category == "students":
            cursor.execute("SELECT id, name, email, department FROM students WHERE name LIKE ? OR email LIKE ? OR department LIKE ?", 
                           (f"%{query}%", f"%{query}%", f"%{query}%"))
            results = cursor.fetchall()
            columns = ["ID", "Name", "Email", "Department"]

        elif category == "companies":
            cursor.execute("SELECT id, name, location, industry FROM companies WHERE name LIKE ? OR location LIKE ? OR industry LIKE ?", 
                           (f"%{query}%", f"%{query}%", f"%{query}%"))
            results = cursor.fetchall()
            columns = ["ID", "Name", "Location", "Industry"]

        elif category == "internships":
            cursor.execute("""
                SELECT i.id, i.title, i.description, i.duration, i.stipend, c.name 
                FROM internships i
                JOIN companies c ON i.company_id = c.id
                WHERE i.title LIKE ? OR i.description LIKE ? OR c.name LIKE ?
            """, (f"%{query}%", f"%{query}%", f"%{query}%"))
            results = cursor.fetchall()
            columns = ["ID", "Title", "Description", "Duration", "Stipend", "Company"]

        conn.close()

        if not results:
            message = f"No results found for '{query}' in {category}."

    return render_template("search.html", results=results, columns=columns, message=message, category=category)

@app.route("/analytics")
def analytics():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT i.title, COUNT(a.id) 
        FROM applications a
        JOIN internships i ON a.internship_id = i.id
        GROUP BY i.id
    """)
    internship_counts = cursor.fetchall()

    cursor.execute("""
        SELECT c.name, COUNT(a.id)
        FROM applications a
        JOIN internships i ON a.internship_id = i.id
        JOIN companies c ON i.company_id = c.id
        GROUP BY c.id
    """)
    company_counts = cursor.fetchall()

    cursor.execute("""
        SELECT status, COUNT(*) FROM applications GROUP BY status
    """)
    status_summary = cursor.fetchall()

    conn.close()

    return render_template("analytics.html",
                           internship_counts=internship_counts,
                           company_counts=company_counts,
                           status_summary=status_summary)

# ---------- MAIN ---------- #

app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'static/uploads'  # folder to store resumes
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/apply', methods=['GET', 'POST'])
def apply():
    conn = get_connection()
    cursor = conn.cursor()

    # Fetch internships for dropdown
    cursor.execute("SELECT id, title FROM internships")
    internships = cursor.fetchall()

    if request.method == 'POST':
        student_name = request.form['student_name']
        email = request.form['email']
        department = request.form['department']
        internship_id = request.form['internship_id']
        resume = request.files['resume']

        # Check if student already exists
        cursor.execute("SELECT id FROM students WHERE name = ? AND email = ?", (student_name, email))
        student = cursor.fetchone()

        if student:
            student_id = student[0]
        else:
            # Add new student to database
            cursor.execute(
                "INSERT INTO students (name, email, department) VALUES (?, ?, ?)",
                (student_name, email, department)
            )
            student_id = cursor.lastrowid

        # Save the uploaded resume
        resume_filename = None
        if resume:
            resume_filename = f"{student_name.replace(' ', '_')}_{resume.filename}"
            resume.save(os.path.join(app.config['UPLOAD_FOLDER'], resume_filename))

        # Insert into applications table
        # Insert into applications table (including resume)
        cursor.execute("""
            INSERT INTO applications (student_id, internship_id, status, resume)
            VALUES (?, ?, ?, ?)
        """, (student_id, internship_id, 'Pending', resume_filename))

        conn.commit()
        conn.close()

        message = f"✅ Application submitted successfully for {student_name}!"
        return render_template('apply.html', message=message, internships=internships)

    conn.close()
    return render_template("apply.html", internships=internships)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True)