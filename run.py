from flask import Flask, render_template, request, redirect, url_for
from forms import SignupForm, PostForm, LoginForm
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from models import ObjetoSimple, User
from models import users, get_user
from werkzeug.urls import url_parse

app = Flask(__name__)
app.config['SECRET_KEY'] = '.,.,.,.MY_Secret_Key.,.,.,.'

login_manager = LoginManager(app)
login_manager.login_view = "login"

# posts = [ObjetoSimple('Soy el post numero 1'), ObjetoSimple('Soy el post numero 2'), ObjetoSimple('Soy el post numero n')]
posts = []

@app.route("/")
def index():
    return render_template("index.html", posts=posts)



@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        # Creamos el usuario y lo guardamos
        user = User(len(users) + 1, name, email, password)
        users.append(user)
        # Dejamos al usuario logueado
        login_user(user, remember=True)
        next_page = request.args.get('next', None)
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template("signup_form.html", form=form)

@app.route("/p/<string:slug>/")
def show_post(slug):
    post = {'title': 'No registrado', 'title_slug': 'sin slug', 'content': 'sin contenido'}
    for oPost in posts:
        if oPost['title_slug'] == slug:
            post = oPost
    return render_template("post_view.html", post=post)

@app.route("/cadetech/<string:slug>/")
def show_post2(slug):
    slug = {'mensaje':'el mensaje es'+slug}
    return slug


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template('login_form.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/admin/post/", methods=['GET', 'POST'], defaults={'post_id': None})
@app.route("/admin/post/<int:post_id>/", methods=['GET', 'POST'])
@login_required
def post_form(post_id):
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        title_slug = form.title_slug.data
        content = form.content.data
        post = {'title': title, 'title_slug': title_slug, 'content': content}
        posts.append(post)
        return redirect(url_for('index'))
    return render_template("admin/post_form.html", form=form)

@login_manager.user_loader
def load_user(user_id):
    for user in users:
        if user.id == int(user_id):
            return user
    return None

app.run(host='0.0.0.0', port=5426, debug=True)