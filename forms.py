from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators, ValidationError
from wtforms.fields import IntegerField, SelectField, DateField

def emailContains(form, field):
    if not field.data.endswith('.se'):
        raise ValidationError('Måste sluta på .se dummer')


class NewCustomerForm(FlaskForm):
    GivenName = StringField('Given name', validators=[validators.DataRequired()])
    Surname = StringField('Surname', validators=[validators.DataRequired()])
    Streetaddress = StringField('Streetaddress', validators=[validators.DataRequired()])
    City = StringField('City', validators=[validators.DataRequired()])
    Zipcode = StringField('Zipcode', validators=[validators.DataRequired()])
    Country = StringField('Country', validators=[validators.DataRequired()])
    CountryCode = SelectField('countryCode',choices=[('SE','+46'),('NO','+41'),('FI','+42')])
    Birthday = DateField('Birthday', validators=[validators.DataRequired()])
    NationalId = StringField('NationalId', validators=[validators.DataRequired()])
    TelephoneCountryCode = StringField('Phone country code', validators=[validators.DataRequired()])
    Telephone = StringField('Phone', validators=[validators.DataRequired()])
    EmailAddress = StringField('E-Mail', validators=[validators.DataRequired()])
    
    