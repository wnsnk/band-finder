from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField, RadioField, SelectField, SelectMultipleField, BooleanField, SearchField
from wtforms.validators import DataRequired, Email, Length
from flask_bootstrap import Bootstrap5

from webscrapers.muzikantenbankeu import MuzikantenBankEU, instrument_options, province_options_netherlands
from webscrapers.muzikantenbanknet import MuzikantenBankNet
from webscrapers.poppuntgelderland import PopPuntGelderlandPrikbord
from webscrapers.date_converter import DateConverter


# flask:
app = Flask(__name__)
app.secret_key = 'idk'
Bootstrap = Bootstrap5(app=app)


class SearchForm(FlaskForm):

    looking_for = RadioField(label='Ik zoek een: *', choices=[
                             'band', 'muzikant'], default='band')
    instrument = SelectField(
        label='Wat voor muzikant? ', choices=['*'] + instrument_options)
    # country = RadioField(label='Land', choices=['Nederland', 'België'])
    province = SelectField(
        label='Provincie', choices=['*'] + province_options_netherlands)
    muzbankeu = BooleanField(
        label='muzikantenbank.eu', default=True)
    muzbanknet = BooleanField(
        label='muzikantenbank.net', default=True)
    poppunt = BooleanField(label='Poppunt Gelderland', default=True)
    submit = SubmitField('Zoeken.')


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
        all_results = []
        if search_form.muzbankeu.data:
            muzikantenbank_eu = MuzikantenBankEU(looking_for=looking_for, instrument=instrument,
                                                 province=province)
            for result in muzikantenbank_eu.results:
                all_results.append(result)
        if search_form.muzbanknet.data:
            if province == None and instrument == None:
                # TODO: MAKE THIS WORK
                muzikantenbank_net = None
                print('none and none')
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
                    all_results.append(result)

        if search_form.poppunt.data:
            poppunt_gelderland = PopPuntGelderlandPrikbord()
            for result in poppunt_gelderland.results:
                all_results.append(result)

        all_results.sort(key=lambda x: x['date'], reverse=True)
        for result in all_results:
            date_converter = DateConverter(result['date'])
            result['date'] = date_converter.convert_strftime()
        return show_results(articles=all_results, )
    else:

        return render_template('index.html', search_form=search_form)


@app.route('/results')
def show_results(articles):
    return render_template('results.html', articles=articles)


if __name__ == '__main__':
    app.run(debug=True)
