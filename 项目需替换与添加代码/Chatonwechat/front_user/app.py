from flask import Flask,render_template
from flask import request,redirect
from flask import url_for
from flask import request
import requests
from model.check_login import is_existed_user,exist_user_user,is_null,get_permission
from model.regist_login import add_user_user

app = Flask(__name__)


def is_url_available(url, timeout=5):
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200
    except requests.RequestException:
        return False

def get_valid_url(urls):
    for url in urls:
        if is_url_available(url):
            return url
    return None

@app.route('/')
def index():
    return redirect(url_for('user_login'))


@app.route('/user_login',methods=['GET','POST'])
def user_login():
    if request.method=='POST':  # 注册发送的请求为POST请求
        username = request.form['username']
        password = request.form['password']
        if is_null(username,password):
            login_massage = "温馨提示：账号和密码是必填"
            return render_template('login_user.html', message=login_massage)
        elif is_existed_user(username, password):
            if get_permission(username):
                urls = ["http://10.242.224.109:8540", "http://10.242.224.109:8550", "http://10.242.224.109:8570"]
                valid_url = get_valid_url(urls)
                if valid_url:
                    return redirect(valid_url)
                else:
                    login_massage = "无法访问目标页面，请检查网络连接或稍后再试。"
                    return render_template('login_user.html', message=login_massage)
            else:
                urls = ["http://10.242.224.109:8520", "http://10.242.224.109:8560", "http://10.242.224.109:8580"]
                valid_url = get_valid_url(urls)
                if valid_url:
                    return redirect(valid_url)
                else:
                    login_massage = "无法访问目标页面，请检查网络连接或稍后再试。"
                    return render_template('login_user.html', message=login_massage)
        elif exist_user_user(username):
            login_massage = "温馨提示：密码错误，请输入正确密码"
            return render_template('login_user.html', message=login_massage)
        else:
            login_massage = "温馨提示：不存在该用户，请先注册"
            return render_template('login_user.html', message=login_massage)
    return render_template('login_user.html')


@app.route("/user_regitser",methods=["GET", 'POST'])
def register_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if is_null(username,password):
            login_massage = "温馨提示：账号和密码是必填"
            return render_template('register_user.html', message=login_massage)
        elif exist_user_user(username):
            login_massage = "温馨提示：用户已存在，请直接登录"
            # return redirect(url_for('user_login'))
            return render_template('register_user.html', message=login_massage)
        else:
            add_user_user(request.form['username'], request.form['password'] )
            return render_template('login_user.html', username=username)
    return render_template('register_user.html')


if __name__=="__main__":
    app.run(host= '0.0.0.0', port=8000)


