from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, SelectField
from wtforms.validators import DataRequired, Email, Length
from flask_bootstrap import Bootstrap5
from webscrapers.muzikantenbankeu import MuzikantenBankEU
from webscrapers.muzikantenbanknet import MuzikantenBankNet
from webscrapers.poppuntgelderland import PopPuntGelderlandPrikbord
from dict_to_text import DictToText
import datetime

# webscrapers:
muzikantenbank_eu = MuzikantenBankEU('musician', instrument='bassist',
                                     province='gelderland', )
muzikantenbank_net = MuzikantenBankNet('bassist gelderland')
poppunt_gelderland = PopPuntGelderlandPrikbord()
today = datetime.datetime.now()

all_results = muzikantenbank_eu.results + \
    muzikantenbank_net.results + poppunt_gelderland.results
with open('results.txt', 'w') as resultstxt:
    resultstxt.write(str(all_results))


# flask:
app = Flask(__name__)
app.secret_key = 'idk'
Bootstrap = Bootstrap5(app=app)


class SearchForm(FlaskForm):
    looking_for = RadioField(label='Ik zoek een:', choices=[
                             'band', 'muzikant'], validators=[DataRequired()])
    looking_for_specifically = SelectField(
        label='Wat voor muzikant? ', choices=['guitar', 'bass', 'drums'])
    country = RadioField(label='Land', choices=['Nederland', 'België'])
    province = SelectField(label='Provincie')


@app.route('/')
def home_page():
    search_form = SearchForm()
    return render_template('index.html', search_form=search_form)


# @app.route('/results')
# def show_results():
#     return render_template('results.html', articles=all_results)


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
