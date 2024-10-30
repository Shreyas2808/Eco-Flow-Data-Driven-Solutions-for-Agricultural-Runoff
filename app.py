import pandas as pd
from flask import Flask, request, render_template, redirect, url_for, session

# Load the dataset
df = pd.read_csv('final_commercial_crops_karnataka.csv', encoding='latin-1')

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key for session management

# Dummy user data for demonstration (replace with a proper user database in production)
users = {
    'admin': 'admin',  # Example user: username: admin, password: password
}

# Function to recommend crops based on nutrient requirements
def recommend_crops(crop_name):
    if crop_name not in df['Crop Name'].values:
        return "Crop not found in the dataset."
    
    nutrient_levels = df.loc[df['Crop Name'] == crop_name, ['Nitrogen (N) (%)', 'Phosphorus (P) (%)', 'Potassium (K) (%)']].values[0]
    recommended_crops = df[
        (df['Nitrogen (N) (%)'] >= nutrient_levels[0]) & 
        (df['Phosphorus (P) (%)'] >= nutrient_levels[1]) & 
        (df['Potassium (K) (%)'] >= nutrient_levels[2])
    ]['Crop Name'].unique()

    recommended_crops = [crop for crop in recommended_crops if crop != crop_name]
    
    return recommended_crops if recommended_crops else "No suitable crops found."

@app.route('/')
def home():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users.get(username) == password:
            session['username'] = username
            return redirect(url_for('home'))
        return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/submit', methods=['POST'])
def submit():
    crop_name = request.form.get('crop_name')  # Get crop name from form
    recommended_crops = recommend_crops(crop_name)
    
    return render_template('index.html', username=session['username'], crop_name=crop_name, recommended_crops=recommended_crops)

if __name__ == '__main__':
    app.run(debug=True)