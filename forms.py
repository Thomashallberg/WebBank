from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators, ValidationError
from wtforms.fields import IntegerField, SelectField, DateField, DecimalField, SubmitField

def emailContains(form, field):
    if not field.data.endswith('.se'):
        raise ValidationError('Måste sluta på .se dummer')


class NewCustomerForm(FlaskForm):
    GivenName = StringField('Given name', validators=[validators.DataRequired(), validators.Length(max=50)])
    Surname = StringField('Surname', validators=[validators.DataRequired(), validators.Length(max=50)])
    Streetaddress = StringField('Streetaddress', validators=[validators.DataRequired(), validators.Length(max=50)])
    City = StringField('City', validators=[validators.DataRequired(), validators.Length(max=50)])
    Zipcode = StringField('Zipcode', validators=[validators.DataRequired(), validators.Length(max=50)])
    Country = StringField('Country', validators=[validators.DataRequired(), validators.Length(max=50)])
    CountryCode = SelectField('countryCode',choices=[('SE','SWE'),('NO','NOR'),('FI','FIN')])
    Birthday = DateField('Birthday', validators=[validators.DataRequired()])
    NationalId = StringField('NationalId', validators=[validators.DataRequired(), validators.Length(max=50)])
    TelephoneCountryCode = IntegerField('Phone country code', validators=[validators.DataRequired()])
    Telephone = StringField('Phone', validators=[validators.DataRequired(), validators.Length(max=50)])
    EmailAddress = StringField('E-Mail', validators=[validators.DataRequired(), validators.Email()])
    
class DepositForm(FlaskForm):
    Amount = IntegerField('Amount', validators=[validators.DataRequired()])
    
class WithdrawForm(FlaskForm):
    Amount = IntegerField('Amount', validators=[validators.DataRequired(),validators.NumberRange(min=1,max=20000)])
    
class TransferForm(FlaskForm):
    Receiver = IntegerField('Account-id', validators=[validators.DataRequired()])
    Amount = IntegerField('Amount', validators=[validators.DataRequired(),validators.NumberRange(min=1,max=5000)])
    
class ResetRequestForm(FlaskForm):
    email = StringField(label="E-mail", validators=[validators.DataRequired(), validators.Length(max=50)])
    password = PasswordField(label="Password", validators=[validators.DataRequired(), validators.Length(max=50)])