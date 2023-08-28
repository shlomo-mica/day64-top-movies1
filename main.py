import wtforms
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, RadioField, BooleanField
from wtforms.validators import DataRequired, InputRequired, Length
from sqlalchemy import update
import requests

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///best_films.db"
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
db.init_app(app)
Bootstrap5(app)


class Update_rate(FlaskForm):
    rate_value = StringField('Rating_value', validators=[InputRequired(),
                                                         Length(min=1, max=100)])
    impression = StringField('Impression',
                             validators=[InputRequired(),
                                         Length(min=1, max=200)])
    price = IntegerField('Price', validators=[InputRequired()])
    level = RadioField('Level',
                       choices=['Beginner', 'Intermediate', 'Advanced'],
                       validators=[InputRequired()])
    available = BooleanField('Available', default='checked')
    change_value = SubmitField(label='Change')


# create table
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=True)
    img_url = db.Column(db.String(250), nullable=False)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


with app.app_context():
    db.create_all()

with app.app_context():
    result = db.session.execute(db.select(Book).order_by(Book.title))
    all_books = result.scalars()
    print(all_books.first().title)

#   FLASK TRANSFER TO HTML PAGE
with app.app_context():
    movie1 = db.session.execute((db.select(Movie).where(Movie.title == "Avatar The Way of Water"))).scalar()
    movie2 = db.session.execute((db.select(Movie).where(Movie.title == "Phone Boot"))).scalar()
    book1 = db.session.execute(db.select(Book).where(Book.title == "Harry Potter")).scalar()


# UPDATE ONE OBJECT ROW(MOVIE) <class '__main__.Movie'>
@app.route('/db-rate-update/<float:rate_val>')
def rate_db(rate_val):
    with app.app_context():
        film = db.session.query(Movie).filter_by(title='Avatar The Way of Water').first()
        print(film.rating, film.id)
        print(rate_val)
        film.rating = rate_val  # change rating
        db.session.commit()
    return "DBASE DONE"


@app.route("/")
def home():
    films = db.session.execute(db.select(Movie).order_by(Movie.title)).scalars()
    var_id = films.all()[0].id
    print("test", var_id)
    for item in films.all():
        print(item.title)
        # print(films.all()[0])

    return render_template("index.html", movies=movie1, films=films, id=var_id)


@app.route('/update_rate/<b_name>')
def change_rate(b_name):
    # a=request.form.get("")
    # print(a.title())
    # print(id_now)
    impression = Update_rate.impression
    rate = Update_rate.rate_value
    form = Update_rate()
    movie_id = Movie.id
    print(b_name)

    return render_template("edit.html", form=form, rate=rate, impression=impression, id=movie_id)


if __name__ == '__main__':
    app.run(debug=True)

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''
# new_movie = Movie(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )

# second_movie = Movie(
#     title="Avatar The Way of Water",
#     year=2022,
#     description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
#     rating=7.3,
#     ranking=9,
#     review="I liked the water.",
#     img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
# )


# with app.app_context():
#     new_book = Book(id=1, title="Harry Potter", author="J. K. Rowling", rating=9.3)
#     db.session.add(new_book)
#     db.session.commit()
# with app.app_context():
#     result = db.session.execute(db.select(Movie).where(Movie.title))
#     all_data = result.scalars()
