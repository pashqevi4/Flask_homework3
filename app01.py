# Создать форму для регистрации пользователей на сайте.
# Форма должна содержать поля "Имя", "Фамилия", "Email", "Пароль"
# и кнопку "Зарегистрироваться". При отправке формы данные должны
# сохраняться в базе данных, а пароль должен быть зашифрован.
from flask import Flask, request, render_template
from module import db, User

from forms import LoginForm
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SECRET_KEY'] = 'mysecretkey'
csrf = CSRFProtect(app)

db.init_app(app)


@app.cli.command("init-db")
def init_db():
    db.create_all()


@app.route('/')
def index():
    return 'Hello there!'


@app.cli.command("fill-db")
def fill_db():
    new_user = User(name='Paul', surname='Anderson', email='mymail@gmail.com', password='qweasdzxc')
    db.session.add(new_user)
    db.session.commit()


@app.route('/add/', methods=['GET', 'POST'])
def add_user():
    form = LoginForm()
    if request.method == 'POST':
        # name = form.name.data
        # surname = form.surname.data
        # email = form.email.data
        # password = form.password.data
        new_user = User(name=form.name.data, surname=form.surname.data, email=form.email.data, password=hash(form.password.data))
        db.session.add(new_user)
        db.session.commit()
    return render_template('user.html', form=form)
