from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators, ValidationError
from wtforms.fields import IntegerField, SelectField, DateField, DecimalField, SubmitField

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
    CountryCode = SelectField('countryCode',choices=[('SE','SWE'),('NO','NOR'),('FI','FIN')])
    Birthday = DateField('Birthday', validators=[validators.DataRequired()])
    NationalId = StringField('NationalId', validators=[validators.DataRequired()])
    TelephoneCountryCode = IntegerField('Phone country code', validators=[validators.DataRequired()])
    Telephone = StringField('Phone', validators=[validators.DataRequired()])
    EmailAddress = StringField('E-Mail', validators=[validators.DataRequired()])
    
class DepositForm(FlaskForm):
    Amount = IntegerField('Amount', validators=[validators.DataRequired()])
    
class WithdrawForm(FlaskForm):
    Amount = IntegerField('Amount', validators=[validators.DataRequired()])
    
class TransferForm(FlaskForm):
    Receiver = IntegerField('Account-id', validators=[validators.DataRequired()])
    Amount = IntegerField('Amount', validators=[validators.DataRequired()])
    
class ResetRequestForm(FlaskForm):
    email = StringField(label="E-mail", validators=[validators.DataRequired()])
    password = PasswordField(label="Password", validators=[validators.DataRequired()])