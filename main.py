from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, SelectField, SelectMultipleField, BooleanField, SearchField
from wtforms.validators import DataRequired, Email, Length
from flask_bootstrap import Bootstrap5
from webscrapers.muzikantenbankeu import MuzikantenBankEU, instrument_options, province_options_netherlands
from webscrapers.muzikantenbanknet import MuzikantenBankNet
from webscrapers.poppuntgelderland import PopPuntGelderlandPrikbord
from dict_to_text import DictToText
import datetime


today = datetime.datetime.now()


# flask:
app = Flask(__name__)
app.secret_key = 'idk'
Bootstrap = Bootstrap5(app=app)


class SearchForm(FlaskForm):

    looking_for = RadioField(label='Ik zoek een:', choices=[
                             'band', 'muzikant'])
    instrument = SelectField(
        label='Wat voor muzikant? ', choices=instrument_options)
    # country = RadioField(label='Land', choices=['Nederland', 'België'])
    province = SelectField(
        label='Provincie', choices=province_options_netherlands)
    muzbankeu = BooleanField(
        label='muzikantenbank.eu', )
    muzbanknet = BooleanField(
        label='muzikantenbank.net', )
    poppunt = BooleanField(label='Poppunt Gelderland')
    submit = SubmitField('Zoeken.')


# class SearchBar(FlaskForm):
#     search_bar = SearchField()
#     submit = SubmitField('Search')


@app.route('/', methods=['POST', 'GET'])
def home_page():
    search_form = SearchForm()
    # search_bar = SearchBar()

    # if search_bar.validate_on_submit():
    #     print(search_bar.search_bar.data)

    if search_form.validate_on_submit():
        looking_for = search_form.looking_for.data
        if looking_for == 'muzikant':
            looking_for = 'musician'
        instrument = search_form.instrument.data
        # country = search_form.country
        province = search_form.province.data

# TODO catch valueerror and unbounderror and other bugs
        all_results = []
        if search_form.muzbankeu.data:
            muzikantenbank_eu = MuzikantenBankEU(looking_for=looking_for, instrument=instrument,
                                                 province=province)
            for result in muzikantenbank_eu.results:
                all_results.append(result)
        if search_form.muzbanknet.data:
            muzikantenbank_net = MuzikantenBankNet(
                f'{instrument} {province}')
            for result in muzikantenbank_net.results:
                all_results.append(result)

        if search_form.poppunt.data:
            poppunt_gelderland = PopPuntGelderlandPrikbord()
            for result in poppunt_gelderland.results:
                all_results.append(result)

        return show_results(articles=all_results, )
    else:

        return render_template('index.html', search_form=search_form)


@app.route('/results')
def show_results(articles):
    return render_template('results.html', articles=articles)


if __name__ == '__main__':
    app.run(debug=True)


# with open('muzikantenbank_eu_results.txt', 'a') as muzbanktxt:
#     muzbanktxt.write(f'Muzikantenbank.eu results of {today}\n')
#     for result in muzikantenbank_eu.results:
#         dict_to_text = DictToText(result)
#         muzbanktxt.write(f'{dict_to_text.return_advertisement()}\n')

# with open('muzikantenbank_net_results.txt', 'a') as muzbanktxt:
#     muzbanktxt.write(f'Muzikantenbank.net results of {today}\n')
#     for result in muzikantenbank_net.results:
#         dict_to_text = DictToText(result)
#         muzbanktxt.write(f'{dict_to_text.return_advertisement()}\n')

# with open('poppuntgelderland_resulst.txt', 'a') as poppunttxt:
#     poppunttxt.write(f'Poppuntgelderland results of {today}\n')
#     for result in poppunt_gelderland.results:
#         dict_to_text = DictToText(result)
#         poppunttxt.write(f'{dict_to_text.return_advertisement()}\n')
