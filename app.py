from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import numpy as np
import pickle
from visualization import generate_salary_visualization

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# Load trained model and scaler
model = pickle.load(open('model1.pkl', 'rb'))
scaler = pickle.load(open('scaler1.pkl', 'rb'))

# In-memory storage for demo purposes
users = {}

@app.route('/')
def home():
    is_logged_in = True if session.get("user_data") else False
    user_data = session.get("user_data", {})
    return render_template('index.html', user_data=user_data, is_logged_in=is_logged_in)

@app.route('/placement')
def placement():
    return render_template('placement.html')

@app.route('/visualization')
def visualization():
    generate_salary_visualization()  # Generates the image in the static folder
    return render_template('visualization.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and user.get("password") == password:
            session["user_data"] = user
            return redirect(url_for('home'))
        else:
            return render_template('login.html', message="Invalid credentials. Please try again.")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Save user info in memory (for demo purposes)
        users[username] = {
            "username": username,
            "email": email,
            "password": password,
            "gender": "1",
            "ssc_p": "90",
            "hsc_p": "85",
        }
        session["user_data"] = users[username]
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop("user_data", None)
    return redirect(url_for('home'))

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        gender = int(request.form['gender'])
        ssc_p = float(request.form['ssc_p'])
        ssc_b_Central = int(request.form['ssc_b'])
        hsc_p = float(request.form['hsc_p'])
        hsc_b_Central = int(request.form['hsc_b'])
        hsc_s = request.form['hsc_s']
        commerce = 1 if hsc_s == "Commerce" else 0
        science = 1 if hsc_s == "Science" else 0

        degree_p = float(request.form['degree_p'])
        degree_t = request.form['degree_t']
        other = 1 if degree_t == "Other" else 0
        scitech = 1 if degree_t == "Sci&Tech" else 0

        workex = int(request.form['workex'])
        etest_p = float(request.form['etest_p'])
        specialisation = request.form['specialisation']
        mca_p = float(request.form['mca_p'])
        status = int(request.form['status'])

        # Features for prediction
        features = np.array([
            commerce, science, other, scitech, gender, ssc_p, hsc_p, degree_p,
            workex, etest_p, mca_p, status, ssc_b_Central, hsc_b_Central, specialisation
        ]).reshape(1, -1)

        scaled = scaler.transform(features)
        prediction = round(model.predict(scaled)[0], 2)
        if prediction < 0:
            prediction = 0

        # Suggested roles based on salary prediction
        suggested_roles = []
        if prediction < 5000000:
            suggested_roles = [
                {"company": "TCS", "role": "Junior Developer", "salary": 400000},
                {"company": "Wipro", "role": "Support Engineer", "salary": 450000}
            ]
        elif prediction < 2500000:
            suggested_roles = [
                {"company": "Infosys", "role": "Software Engineer", "salary": 600000},
                {"company": "Accenture", "role": "Systems Analyst", "salary": 650000}
            ]
        else:
            suggested_roles = [
                {"company": "Amazon", "role": "Senior Developer", "salary": 900000},
                {"company": "Google", "role": "Lead Engineer", "salary": 1000000}
            ]

        return render_template('prediction.html', result=prediction, job_roles=suggested_roles)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)


