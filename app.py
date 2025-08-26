from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 假设我们手动写入一个简单的用户表（你可以后续连接数据库）
users = {
    'opfba18@163.com': '123456',
    'test@example.com': 'password123'
}

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        email = request.form.get('email').strip().lower()
        password = request.form.get('password').strip()

        # 登录验证
        if email in users and users[email] == password:
            session['email'] = email
            return redirect(url_for('dashboard'))
        else:
            error = '邮箱或密码错误，请重试。'

    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    email = session.get('email')
    if not email:
        return redirect(url_for('login'))

    df = pd.read_csv('data/data.csv', encoding='utf-8')
    df.columns = df.columns.str.strip()
    filtered_df = df[df['login_email'].str.lower() == email.lower()]
    return render_template('dashboard.html', tables=filtered_df.to_dict(orient='records'), headers=filtered_df.columns)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
