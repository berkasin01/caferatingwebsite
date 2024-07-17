from flask import Flask, request, render_template
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
    has_sockets = BooleanField(label="Has Sockets", validators=[DataRequired()])
    has_toilet = BooleanField(label="Has Toilet", validators=[DataRequired()])
    has_wifi = BooleanField(label="Has Wi-Fi", validators=[DataRequired()])
    can_take_calls = BooleanField(label="Can take Calls", validators=[DataRequired()])
    num_seats = IntegerField(label="Amount of Seats", validators=[DataRequired()])
    coffee_price = StringField(label="Coffe Price", validators=[DataRequired()])
    submit = SubmitField("Add a new Cafe")


@app.route("/")
def home_page():
    cafe_id = 1
    access = db.get_or_404(Cafe, cafe_id)

    return render_template("index.html", access=access.name)


@app.route('/add', methods=["POST", "GET"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.cafe.data,
            map_url=form.location_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            seats=form.num_seats.data,
            has_toilet=form.has_toilet.data,
            has_wifi=form.has_wifi.data,
            has_sockets=form.has_sockets,
            can_take_calls=form.can_take_calls,
            coffee_price=form.coffee_price

        )
        db.session.add(new_cafe)
        db.session.commit()
        return render_template("success.html")
    return render_template('add.html', form=form)


if __name__ == "__main__":
    app.run()
