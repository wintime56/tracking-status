from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于 Session 登录安全验证

# 首页提示信息
@app.route('/')
def home():
    return "✅ 系统已成功部署！请访问 /login 登录"

# 登录页面：支持 GET 显示表单，POST 验证用户
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()

        # 用户验证：这里简单写死账户密码，后期你可以做成数据库验证
        if email == 'opfba18@163.com' and password == 'your_password':
            session['email'] = email
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='邮箱或密码错误')
    return render_template('login.html')

# 仪表板页面：需要登录后才能访问
@app.route('/dashboard')
def dashboard():
    email = session.get('email')
    if not email:
        return redirect(url_for('login'))

    try:
        df = pd.read_csv('data/data.csv', encoding='gbk')
        df.columns = df.columns.str.strip()
        filtered_df = df[df['login_email'].str.lower() == email.lower()]
    except Exception as e:
        return f"❌ 加载数据出错: {str(e)}"

    return render_template('dashboard.html', tables=filtered_df.to_dict(orient='records'), headers=filtered_df.columns)

# 退出登录
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# 启动程序（本地调试用）
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
