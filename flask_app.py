from flask import Flask
from flask import send_from_directory
from flask import jsonify, render_template, request, redirect, url_for, make_response, abort
import os

app = Flask(__name__)
file_names = []
password = "admin"
@app.route('/')
def home():
    return send_from_directory(directory=app.static_folder, path='home.html')

@app.route('/benefits')
def benefits():
    return send_from_directory(directory=app.static_folder, path = 'benefits.html')

@app.route('/apply')
def apply():
    return render_template('apply.html')

@app.route('/login')
def login():
    return send_from_directory(directory=app.static_folder, path = 'login.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        job_interest = request.form['jobInterest']
        phone_number = request.form['phoneNumber']
        address = request.form['address']
        employment_type = request.form['employmentType']
        filename = os.path.join("static", f"{first_name}_{last_name}_application.html")
        pdf_name = f"{first_name}_{last_name}_pdf.pdf"
        pdf_path = os.path.join(app.static_folder, pdf_name)
        file_path = os.path.join(app.root_path, filename)
        with open(file_path, 'w') as file:
            new_page = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Job Application</title>
<style>
    body {{
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 20px;
        background-color: #f0f0f0;
    }}
    .container {{
        max-width: 600px;
        margin: 0 auto;
        background-color: #fff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }}
    h2 {{
        color: #333;
    }}
    strong {{
        font-weight: bold;
    }}
    p {{
        margin-bottom: 10px;
    }}
    a {{
        color: #007bff;
        text-decoration: none;
    }}
</style>
</head>
<body>
    <div class="container">
        <h2>Job Application</h2>
        <p><strong>First Name:</strong> {first_name}</p>
        <p><strong>Last Name:</strong> {last_name}</p>
        <p><strong>Job Interest:</strong> {job_interest}</p>
        <p><strong>Phone Number:</strong> {phone_number}</p>
        <p><strong>Address:</strong> {address}</p>
        <p><strong>Employment Type:</strong> {employment_type}</p>
        <p><strong><a href="/display_pdf/{pdf_name}" target="_blank">View Resume</a></p>
    </div>
</body>
</html>
"""
            file.write(new_page)
        if 'resume' in request.files:
            resume_file = request.files['resume']
            if resume_file:
                resume_file.save(pdf_path)
                # Read PDF content
                with open(pdf_path, 'rb') as pdf_file:
                    pdf_data = pdf_file.read()
                with open(pdf_path, 'wb') as pdf_file:
                    pdf_file.write(pdf_data)
    file_names.append(filename)
    return render_template('submitted.html', first_name=first_name, last_name=last_name)
@app.route('/display_pdf/<filename>')
def display_pdf(filename):
    pdf_path = url_for('static', filename=filename)
    return render_template('display_pdf.html', pdf_path=pdf_path)
@app.route('/render_html/<filename>')
def render_html(filename):
    try:
        return send_from_directory(directory=app.static_folder, path = filename)
    except Exception as e:
        return f"Error serving HTML file: {e}", 500

@app.route('/process_form', methods = ['POST'])
def process_form():
    submitted_password = request.form.get('password')
    is_password_correct = submitted_password == password
    if (is_password_correct):
        return render_template('selection.html', file_names = file_names)
    else:
        return send_from_directory(directory=app.static_folder, path = 'home.html')

@app.route('/selection', methods = ['POST'])
def selection():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    #example file name: Rene_Ramirez_application.html
    file_name = f"{first_name}_{last_name}_application.html"
    return redirect(url_for('render_html', filename = file_name))

app.run(debug=True, port=8080)