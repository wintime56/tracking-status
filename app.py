
from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip()
        session['email'] = email
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    email = session.get('email')
    if not email:
        return redirect(url_for('login'))
    df = pd.read_csv('data/data.csv', encoding='gbk')
    df.columns = df.columns.str.strip()
    filtered_df = df[df['login_email'].str.lower() == email.lower()]
    return render_template('dashboard.html', tables=filtered_df.to_dict(orient='records'), headers=filtered_df.columns)

if __name__ == '__main__':
    app.run(debug=True)
