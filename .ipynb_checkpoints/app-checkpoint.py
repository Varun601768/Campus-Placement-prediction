from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import numpy as np
import pickle
from visualization import generate_salary_visualization

app = Flask(__name__)
app.secret_key = "your_secret_key_here"
model = pickle.load(open('model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))

# In-memory storage for demo purposes
users = {}

@app.route('/')
def home():
    # Check if user is logged in by testing session for user_data
    is_logged_in = True if session.get("user_data") else False
    # Also, pass user_data to pre-fill form (if available)
    user_data = session.get("user_data", {})
    return render_template('index.html', user_data=user_data, is_logged_in=is_logged_in)

@app.route('/placement')
def placement():
    return render_template('placement.html')

@app.route('/visualization')
def visualization():
    # Generate the visualization image
    generate_salary_visualization()  # Generates the image in the static folder
    return render_template('visualization.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Very simple authentication for demonstration
        user = users.get(username)
        if user and user.get("password") == password:
            # Save user data in session to pre-fill the form on index.html and enable it
            session["user_data"] = user
            return redirect(url_for('home'))
        else:
            return render_template('login.html', message="Invalid credentials. Please try again.")
    return render_template('login.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # Save user info (for demo purposes, we're storing it in a dictionary)
        users[username] = {
            "username": username,
            "email": email,
            "password": password,
            # You can include additional fields that should pre-fill the index form
            "gender": "1",  # default value e.g., Male
            "ssc_p": "90",  # example default values
            "hsc_p": "85",
            # add any other fields as needed...
        }
        # Optionally, auto log in the user after registration:
        session["user_data"] = users[username]
        return redirect(url_for('home'))
    return render_template('register.html')



@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        gender = int(request.form['gender'])
        ssc_p = float(request.form['ssc_p'])
        ssc_b_Central = int(request.form['ssc_b'])
        hsc_p = float(request.form['hsc_p'])
        hsc_b_Central = int(request.form['hsc_b'])
        hsc_s = request.form['hsc_s']
        if hsc_s == "Commerce":
            commerce = 1
            science = 0
        elif hsc_s == "Science":
            commerce = 0
            science = 1
        else:
            commerce = 0
            science = 0
        degree_p = float(request.form['degree_p'])
        degree_t = request.form['degree_t']
        if degree_t == "Sci&Tech":
            other = 0
            scitech = 1
        elif degree_t == "Comm&Mgmt":
            other = 0
            scitech = 0
        else:
            other = 1
            scitech = 0
        workex = int(request.form['workex'])
        etest_p = float(request.form['etest_p'])
        specialisation = int(request.form['specialisation'])
        mba_p = float(request.form['mba_p'])
        status = int(request.form['status'])

        scaled = scaler.transform(np.array([commerce, science, other, scitech, gender, ssc_p, hsc_p, degree_p, workex, etest_p, mba_p, status, ssc_b_Central, hsc_b_Central, specialisation]).reshape(1, -1))
        prediction = round(model.predict(scaled)[0], 2)
        if prediction < 0:
            prediction = 0

    return render_template('prediction.html', result=prediction)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
