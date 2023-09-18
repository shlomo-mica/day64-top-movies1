import wtforms
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, RadioField, BooleanField
from wtforms.validators import DataRequired, InputRequired, Length
from sqlalchemy import update
import requests
from sqlalchemy.engine.result import ScalarResult

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


# create table define classes
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=True)
    img_url = db.Column(db.String(250), nullable=False)


jhon = Movie(title="jaws", year=2011,
             description='When a killer shark unleashes chaos on a beach community off Cape Cod',
             # it's up to a local sheriff, a marine biologist,
             #  and an old seafarer to hunt the beast down')
             rating=9, ranking='4 stars', review='very good',
             img_url="https://th.bing.com/th/id/OIP.Uqbg8JOaiDfQeNgpUA2hyQAAAA?pid=ImgDet&w=440&h=660&rs=1")


# with app.app_context():
# db.session.add(jhon  ?.MNV 342356789#
# db.session.commit

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
    print(all_books.first().author)
    query = db.session.query(Movie)
    list_of_all_movies = query.all()  # home routh use this list
    # print(a[1].img_url)
    # for row in a:
    #     print(row)
#   FLASK TRANSFER TO HTML PAGE
with app.app_context():
    movie1 = db.session.execute((db.select(Movie).where(Movie.id == 1))).scalar()
    movie2 = db.session.execute((db.select(Movie).where(Movie.id == 2))).scalar()
    book1 = db.session.execute(db.select(Book).where(Book.title == "Harry Potter")).scalar()
    b = movie1.img_url
    print(b)
    moooov_exe = Movie.query.all()


def connect_to_data_base(m_name):
    url_query = f'https://api.themoviedb.org/3/search/movie?query={m_name}'
    # f'  # &callback=test' \

    url_jack = f'https://api.themoviedb.org/3/search/movie?query=Jack+Reacher&api_key=4c06ee924f273bf05a13ca12ada916a3'
    header_query = {"accept": "application/json",
                    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0YzA2ZWU5MjRmMjczYmYwNWExM2NhMTJhZGE5MTZhMyIsInN1YiI6IjY0ZjFlMDY4ZTBjYTdmMDBjYmU1MDZmNyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.S8_4wPKkGLL_YjRHIejiGxbXmqrl-n_DzVjg-4S5aYo"}
    response = requests.get(url_query, params={"api_key": '4c06ee924f273bf05a13ca12ada916a3', "query": 'shark'})
    data = response.json()["results"]
    multistories = requests.get(url_query, headers=header_query)
    list1 = (multistories.json())
    print(list1['results'])
    print('data', data)

    # for i in list1['results']:
    #     print(i['id'])
    #     print(i['original_title'])
    #     print(i['release_date'])
    #     print(i['overview'])
    #     # 'poster_path': '/la0eOA49YtQfffTwQFFFVIJCh5u.jpg'
    data_details = list1['results']

    return data_details


@app.route('/insert_favorite_to database/<title1>-<desc1>-<date1>-<rating1>-<vote_count1>')
def insert_db(title1, desc1, date1, rating1, vote_count1):
    rating_float = float(rating1)
    ranking = int(vote_count1)
    print(type(date1))
    print(date1)

    new_movie = Movie(title=title1,
                      description=desc1,
                      rating=rating_float,
                      ranking=ranking)
    # img_url=poster_path1)

    # print("poster_path,", poster_path1)

    # 'poster_path': '/2JhwA8uxxb5ZKjMH6eDHLuJLVUw.jpg'
    with app.app_context():
        db.session.add(new_movie)
        db.session.commit()

    print(title1)
    print("********************")
    print(date1)
    # print(desc1)

    return render_template("select.html")


@app.route('/add_movie', methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        data = request.form
        form_add_name = data.get("film_name")
        print(form_add_name)
        mov = (connect_to_data_base(form_add_name))
        return render_template("select.html", TMDB=mov)
    else:
        message = 'Movie not in our data base'
        print(message)
        return render_template("add.html", nofile=message)


@app.route('/delete')
def delete_now():
    # Fetch the row you want to delete
    user_to_delete = Movie.query.filter_by(id=13).first()

    # Check if the user exists
    if user_to_delete:
        # Delete the user
        db.session.delete(user_to_delete)
        db.session.commit()
        return "User deleted successfully."
    else:
        return "User not found."


# UPDATE ONE OBJECT ROW(MOVIE) <class '__main__.Movie'>
# /<float:rate_val>
@app.route('/db-rate-update', methods=['GET', 'POST'])
def rate_db():
    global rate_value, impression, b_name
    if request.method == 'POST':
        rate_value = request.form.get('rate_value')
        impression = request.form.get('impression')
        print('rate Value:', rate_value)
        print(('impression=', impression))

    with app.app_context():
        film = db.session.query(Movie).filter_by(id=3).first()
        print(film.rating, film.id)
        film.rating = rate_value  # change rating
        film.review = impression
        db.session.commit()

        print("DBASE DONE")
    return "OK"


@app.route("/")
def home():
    films = db.session.execute(db.select(Movie).order_by(Movie.title)).scalars()
    var_id = films.all()[2].rating
    print(var_id)
    movies = [movie1, movie2]
    # for item in films:
    #     print("title", item.title)
    return render_template("index.html", movies=list_of_all_movies, films=films, id=var_id)


@app.route('/update_rate/<b_name>')
def change_rate(b_name):
    # a=request.form.get("")
    # print(a.title())
    # print(id_now)
    # impression = Update_rate.impression
    # rate = Update_rate.rate_value
    # movie_id = Movie.id
    form = Update_rate()

    print("bname=", b_name)

    return render_template("edit.html", form=form, b_name=b_name)


@app.route('/divs')
def generate_divs():
    movie1 = db.session.execute((db.select(Movie).where(Movie.id == 1))).scalar()
    # Define a list of variables
    variables = ["Variable 1", "Variable 2", "Variable 3"]

    # Pass the variables list to the template
    return render_template('index.html', variables=variables)


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
