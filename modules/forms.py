from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, SelectField, SelectMultipleField, BooleanField, SearchField
from modules.webscrapers.muzikantenbankeu import instrument_options, province_options_netherlands


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


class SearchBar(FlaskForm):
    search_field = SearchField('')
    submit = SubmitField('Zoeken')
