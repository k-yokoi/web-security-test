from flask import *
from util2 import *
import hashlib
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        id = valid_login(request.form['username'], request.form['password'])
        if id is not None:
            if request.form['username'] == 'admin':
                redirect_to_index = redirect('/admin')
                response = current_app.make_response(redirect_to_index)
                sid = hashlib.md5("admin".encode()).hexdigest()
                response.set_cookie('WST_ADMIN_COOKIE', sid)
                return response
            else:
                redirect_to_index = redirect(url_for('user', id=id))
                response = current_app.make_response(redirect_to_index)
                sid = hashlib.md5(os.urandom(16)).hexdigest()
                save_sid(id, sid)
                dic = { 'UID': id, 'SID': sid }
                response.set_cookie('WST_USER_COOKIE', value = json.dumps(dic), max_age=60*30)
                return response
        else:
            return abort(401)
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    redirect_to_index = redirect('/')
    response = current_app.make_response(redirect_to_index)
    response.set_cookie('WST_USER_COOKIE', "", max_age=0)
    return response


@app.route('/regist', methods=['GET', 'POST'])
def regist():
    error = None
    if request.method == 'POST':
        if request.form['username'] != "" and not contain_user(request.form['username']):
            regist_user(request.form['username'],
                        request.form['password'])
            return redirect(url_for('index'))
        else:
            message = "このユーザ名では登録できません。"
            return render_template('regist.html', message=message)
    else:
        return render_template('regist.html')


@app.route('/delete')
def delete():
    sid = request.args.get('sid', '')
    if sid == hashlib.md5("admin".encode()).hexdigest():
        return render_template('delete.html', users=get_users())
    else:
        return abort(401)

@app.route('/edit_info')
def edit_info():
    cookie = request.cookies.get('WST_USER_COOKIE', None)
    if cookie is None:
        return abort(401)
    
    dic = json.loads(cookie)    
    if dic['SID'] == get_sid(int(dic['UID'])):
        return render_template('edit_info.html', name=get_username(int(dic['UID'])))
    else:
        return abort(401)


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/user/<int:id>')
def user(id=None):
    if id is None:
        return abort(400)
    else:
        name = get_username(id)
        return render_template('user.html', name=name)


@app.route('/list')
def list():
    users = get_users()
    return render_template('list.html', users=users)


@app.route('/users')
def users():
    users = get_users()
    return json.dumps(users)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)