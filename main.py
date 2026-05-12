from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, PasswordField, SubmitField, RadioField, SelectField, SelectMultipleField, BooleanField, SearchField
from wtforms.validators import DataRequired, Email, Length
from flask_bootstrap import Bootstrap5

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, desc

from modules.webscrapers.muzikantenbankeu import MuzikantenBankEU, instrument_options, province_options_netherlands
from modules.webscrapers.muzikantenbanknet import MuzikantenBankNet
from modules.webscrapers.poppuntgelderland import PopPuntGelderlandPrikbord
from modules.date_converter import DateConverter

from modules.forms import SearchBar, SearchForm
from dotenv import load_dotenv
import os
import sys

load_dotenv()

# flask:
app = Flask(__name__)
app.secret_key = os.getenv('APP_SECRET_KEY')
Bootstrap = Bootstrap5(app=app)
csrf = CSRFProtect(app)
csrf.init_app(app)


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db.init_app(app)


class TemporaryAdvertisements(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    category: Mapped[str]
    message: Mapped[str]
    link: Mapped[str]
    date: Mapped[str]
    website: Mapped[str]


class FavouriteAdvertisements(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    category: Mapped[str]
    message: Mapped[str]
    link: Mapped[str]
    date: Mapped[str]
    website: Mapped[str]


class SearchAdvertisements(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    category: Mapped[str]
    message: Mapped[str]
    link: Mapped[str]
    date: Mapped[str]
    website: Mapped[str]


with app.app_context():
    db.create_all()


@app.route('/', methods=['POST', 'GET'])
def home_page():
    search_form = SearchForm()

    if search_form.validate_on_submit():
        looking_for = search_form.looking_for.data
        if looking_for == 'muzikant':
            looking_for = 'musician'
        instrument = search_form.instrument.data
        if instrument == '*':
            instrument = None
        # country = search_form.country
        province = search_form.province.data
        if province == '*':
            province = None

# TODO catch valueerror and unbounderror and other bugs
        if search_form.muzbankeu.data:
            muzikantenbank_eu = MuzikantenBankEU(looking_for=looking_for, instrument=instrument,
                                                 province=province)
            for result in muzikantenbank_eu.results:
                send_ad_to_database = TemporaryAdvertisements(title=result['title'],
                                                              category=result['category'],
                                                              message=result['message'],
                                                              link=result['link'],
                                                              date=result['date'],
                                                              website=result['website'],)
                db.session.add(send_ad_to_database)
                db.session.commit()

        if search_form.muzbanknet.data:
            if province == None and instrument == None:
                muzikantenbank_net = MuzikantenBankNet('', get_all_ads=True)
            elif province == None:
                muzikantenbank_net = MuzikantenBankNet(
                    f'{instrument}')
            elif instrument == None:
                muzikantenbank_net = MuzikantenBankNet(
                    f'{province}')
            else:
                muzikantenbank_net = MuzikantenBankNet(
                    f'{instrument} {province}')

            if muzikantenbank_net:
                print('if')
                for result in muzikantenbank_net.results:
                    send_ad_to_database = TemporaryAdvertisements(title=result['title'],
                                                                  category=result['category'],
                                                                  message=result['message'],
                                                                  link=result['link'],
                                                                  date=result['date'],
                                                                  website=result['website'],)
                    db.session.add(send_ad_to_database)
                    db.session.commit()

        if search_form.poppunt.data:
            poppunt_gelderland = PopPuntGelderlandPrikbord()
            for result in poppunt_gelderland.results:
                send_ad_to_database = TemporaryAdvertisements(title=result['title'],
                                                              category=result['category'],
                                                              message=result['message'],
                                                              link=result['link'],
                                                              date=result['date'],
                                                              website=result['website'],)
                db.session.add(send_ad_to_database)
                db.session.commit()

        return redirect(url_for('show_results'))
    else:
        db.session.query(TemporaryAdvertisements).delete()
        db.session.commit()

        return render_template('index.html', search_form=search_form)


@app.route('/results', methods=['GET', 'POST'])
def show_results():
    search_bar = SearchBar()
    all_results = db.session.execute(db.select(TemporaryAdvertisements).order_by(desc(
        TemporaryAdvertisements.date))).scalars().all()
    if search_bar.validate_on_submit():
        db.session.query(SearchAdvertisements).delete()
        db.session.commit()
        query = search_bar.search_field.data.lower()
        for result in all_results:
            if query in result.title.lower() or query in result.message.lower():
                add_advertisement = SearchAdvertisements(id=result.id,
                                                         title=result.title,
                                                         category=result.category,
                                                         message=result.message,
                                                         link=result.link,
                                                         date=result.date,
                                                         website=result.website)
                db.session.add(add_advertisement)
                db.session.commit()
        return redirect(url_for('get_search_results', query=query))
    return render_template('results.html', articles=all_results, search_bar=search_bar)


@app.route('/add/<id>')
def add_to_favourites(id):
    article = db.get_or_404(TemporaryAdvertisements, id)
    new_favourite = FavouriteAdvertisements(id=article.id,
                                            title=article.title,
                                            category=article.category,
                                            message=article.message,
                                            link=article.link,
                                            date=article.date,
                                            website=article.website)
    db.session.add(new_favourite)
    db.session.commit()
    return redirect(url_for('show_results'))


@app.route('/delete/<id>')
def remove_from_favourites(id):
    FavouriteAdvertisements.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('show_favourites'))


@app.route('/favourites')
def show_favourites():
    all_favourites = db.session.execute(db.select(FavouriteAdvertisements).order_by(desc(
        FavouriteAdvertisements.date))).scalars()
    return render_template('favourites.html', articles=all_favourites)


@app.route('/search/<query>')
def get_search_results(query):

    search_results = db.session.execute(db.select(SearchAdvertisements).order_by(desc(
        SearchAdvertisements.date))).scalars()
    return render_template('search.html', articles=search_results, query=query)


if __name__ == '__main__':
    app.run(debug=True)
