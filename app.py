from flask import *
from util import *
import hashlib

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
                return redirect(url_for('user', id=id))
        else:
            return abort(401)
    else:
        return render_template('login.html')


@app.route('/regist', methods=['GET', 'POST'])
def regist():
    error = None
    if request.method == 'POST':
        regist_user(request.form['username'],
                       request.form['password'])
        return redirect(url_for('index'))
    else:
        return render_template('regist.html')


@app.route('/delete')
def delete():
    sid = request.args.get('sid', '')
    if sid == hashlib.md5("admin".encode()).hexdigest():
        return render_template('delete.html', users=get_users())
    else:
        return abort(401)



@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/user/<int:id>')
def user(id=None):
    if id is None:
        return render_template('user.html')
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
    app.run(host='0.0.0.0', debug=False)