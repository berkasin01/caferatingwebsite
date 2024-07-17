from flask import Flask, request, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, String, Integer, Float, Table, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, TimeField, SelectField, BooleanField, IntegerField, FloatField
from wtforms.validators import DataRequired
import sqlite3

app = Flask(__name__)
bootstrap = Bootstrap5(app)


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
db.init_app(app=app)
app.config['SECRET_KEY'] = 'secretkey'


class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location_url = URLField('Location Google Maps Link', validators=[DataRequired()])
    img_url = URLField('Image URL', validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    has_sockets = BooleanField(label="Has Sockets")
    has_toilet = BooleanField(label="Has Toilet")
    has_wifi = BooleanField(label="Has Wi-Fi")
    can_take_calls = BooleanField(label="Can take Calls")
    num_seats = IntegerField(label="Amount of Seats", validators=[DataRequired()])
    coffee_price = StringField(label="Coffe Price", validators=[DataRequired()])
    submit = SubmitField("Add a new Cafe")


@app.route("/")
def home_page():
    all_cafes = db.session.execute(db.select(Cafe).order_by(Cafe.id)).scalars().all()
    return render_template("index.html", all_data=all_cafes)


@app.route('/add', methods=["POST", "GET"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        if form.has_wifi.data:
            has_wifi = 1
        else:
            has_wifi = 0

        if form.has_sockets.data:
            has_sockets = 1
        else:
            has_sockets = 0

        if form.has_toilet.data:
            has_toilet = 1
        else:
            has_toilet = 0

        if form.can_take_calls.data:
            can_take_calls = 1
        else:
            can_take_calls = 0
        new_cafe = Cafe(
            name=form.cafe.data,
            map_url=form.location_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            seats=form.num_seats.data,
            has_toilet=has_toilet,
            has_wifi=has_wifi,
            has_sockets=has_sockets,
            can_take_calls=can_take_calls,
            coffee_price=form.coffee_price.data

        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home_page'))
    return render_template('add.html', form=form)


if __name__ == "__main__":
    app.run()
