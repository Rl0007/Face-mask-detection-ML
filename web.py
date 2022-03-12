from os import name
from flask import *
from flask_sqlalchemy import SQLAlchemy
import datetime
from datetime import datetime, timedelta
from sqlalchemy import func


web = Flask(__name__)
web.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
web.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
web.config['SQLALCHEMY_BINDS'] = {
    'wearmask':      'sqlite:///wearmask.db'}
db = SQLAlchemy(web)


class wearmask(db.Model):
    __bind_key__ = 'wearmask'
    sno = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.DateTime, default=datetime.now)

    mask = db.Column(db.String(10))


class user(db.Model):

    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    email1 = db.Column(db.String(80), unique=True)


@web.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        name = request.form['id1']
        password = request.form['password']
        if bool(user.query.filter_by(name=name, email1=password).first()):
            return redirect('/display')
        else:
            print("user does not exist")

    print("hello")
    return render_template("login.html")


@web.route("/display")
def display():
    # sub = subject
    value = wearmask.query.all()
    # allattendance = sub.query.all()
    return render_template("display.html", wearmask=value, )


@web.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['firstname']
        password1 = request.form['password1']
        password2 = request.form['password2']

        ant = user.__table__.columns.keys()
        print(ant)

        a = bool(user.query.filter_by(email1=password1).first())
        if a == 1:
            print("exists")
        else:
            print("not exist")
            if password1 == password2:
                print("registered")
                uid = user(name=name,  email1=password1)
                db.session.add(uid)
                db.session.commit()
            else:
                return render_template("register.html")
            return render_template("login.html")

    # a=bool(user.query.filter_by(name=id).first())

    return render_template("register.html")


@web.route("/delete/<int:sno>")
def delete(sno):
    # allbooks = book.query.all()
    delete_entry = wearmask.query.filter_by(sno=sno).first()

    db.session.delete(delete_entry)
    db.session.commit()
    return redirect('/display')


if __name__ == "__main__":
    web.run(debug=True)
