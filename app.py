from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 自动识别 Railway 路径或本地路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'data', 'data.csv')
USER_FILE = os.path.join(BASE_DIR, 'data', 'users.csv')


# 登录页（GET展示登录表单，POST提交验证）
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_input = request.form['email']
        password_input = request.form['password']
        
        try:
            users_df = pd.read_csv(USER_FILE)
            user = users_df[(users_df['email'] == email_input) & (users_df['password'] == password_input)]
        except Exception as e:
            return f"读取用户信息失败：{e}"

        if not user.empty:
            session['email'] = email_input
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='❌ 邮箱或密码错误，请重试')

    return render_template('login.html')


# 注销
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# 主查询面板
@app.route('/', methods=['GET'])
@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'email' not in session:
        return redirect(url_for('login'))

    try:
        df = pd.read_csv(DATA_FILE)
    except Exception as e:
        return f"读取清关数据失败：{e}"

    email = session['email']
    filtered_df = df[df['login_email'].str.lower() == email.lower()] if 'login_email' in df.columns else df

    data = filtered_df.to_dict(orient='records')
    columns = filtered_df.columns.tolist()
    return render_template('dashboard.html', data=data, columns=columns, email=email)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
