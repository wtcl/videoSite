import os
import random
from flask import Flask, request, render_template, session, make_response, \
    url_for, redirect
import pandas as pd
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = 'AKSKDJWI2IIIEIDK4'
app._static_folder = './static/'
app.add_template_global = './templates/css/'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test')
def test_load():
    return render_template('test.html')


@app.route('/video')
def video():
    files = os.listdir('./static/video/')
    # print(files)
    files = random.sample(files, 1)
    print(files)
    return render_template('mp4player.html', movies=files)


@app.route('/vip')
def vip():
    if 'name' in session:
        vip_file = os.listdir('./static/VIP/')
        file = random.sample(vip_file, 1)
        print(file)
        return render_template('new_test.html', movies=file)
        # return render_template('vip.html',movies=file)
    else:
        return render_template('login.html')


@app.route('/admin')
def admin():
    if 'name' not in session:
        return render_template('login.html')
    return render_template('admin.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        name = request.form['name']  # 接受登录的用户名
        psd = request.form['password']  # 接受登录的用户密码
        print(name, psd)
        db = {'VIP': '123456'}
        if name in db and db[name] == psd:
            resp = make_response()
            resp.set_cookie('name', 'i am cookie', max_age=100)
            key = str(os.urandom(24))
            session.get(key, '默认值')
            session['name'] = name
            return (render_template('success.html', to='\\vip'))
        else:
            return render_template('fail.html')
    if request.method == 'GET':
        if 'name' not in session:
            return render_template('login.html')
        else:
            return redirect(url_for('index'), code=301)


@app.route('/loginout', methods=['POST', 'GET'])
def loginout():
    resp = make_response()
    resp.delete_cookie('name')
    session.clear()
    # 清除所有的session，确保真正退出
    session.pop('name', None)
    return ('退出成功！')


@app.route('/picture')
def picture():
    files = os.listdir('./static/picture/')
    # print(files)
    files = random.sample(files, 100)
    print(files)
    return render_template('pic.html', pictures=files)


@app.route("/<name>")
def hello(name):
    return render_template('hello.html', name=name)
    # return f"Hello, {escape(name)}!"


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['the_file']
        file.save(f"/uploads/{secure_filename(file.filename)}")
    else:
        return 'None'


@app.route('/data')
def data():
    data = pd.read_csv(open("data_1.csv", 'r', encoding='utf-8'), sep=',',
                       usecols=['id', 'G', 'B'])
    return f"""
    <html>
        <body>
            <h1>信息表</h1>
            <div>{data.to_html()}</div>
        </body>
    </html>
    """


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
