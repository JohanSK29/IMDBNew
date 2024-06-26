from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, FloatField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange
import re
from GreenGroceries.queries import get_user_by_user_name, get_farmer_by_pk, get_customer_by_pk
from GreenGroceries.utils.choices import ProduceItemChoices, ProduceCategoryChoices, UserTypeChoices, \
    ProduceVarietyChoices, ProduceUnitChoices


class UserLoginForm(FlaskForm):
    user_name = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=50)],
                            render_kw=dict(placeholder='Username'))
    password = PasswordField('Password',
                             validators=[DataRequired()],
                             render_kw=dict(placeholder='Password'))
    submit = SubmitField('Login')

    def validate_password(self, field):
        user = get_user_by_user_name(self.user_name.data)
        if user is None:
            raise ValidationError(f'User name "{self.user_name.data}" does not exist.')
        if user.password != self.password.data:
            raise ValidationError(f'User name or password are incorrect.')


class UserSignupForm(FlaskForm):
    full_name = StringField('Full name',
                            validators=[DataRequired(), Length(min=2, max=50)],
                            render_kw=dict(placeholder='Full name'))
    user_name = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=50)],
                            render_kw=dict(placeholder='Username'))
    password = PasswordField('Password',
                             validators=[DataRequired()],
                             render_kw=dict(placeholder='Password'))
    password_repeat = PasswordField('Repeat Password',
                                    validators=[DataRequired()],
                                    render_kw=dict(placeholder='Password'))
    user_type = SelectField('Do you farm movies or consume them?',
                            validators=[DataRequired()],
                            choices=UserTypeChoices.choices())
    submit = SubmitField('Sign up')

    def validate_user_name(self, field):
        user = get_user_by_user_name(self.user_name.data)
        if user:
            raise ValidationError(f'User name "{self.user_name.data}" already in use.')

    def validate_password_repeat(self, field):
        if not self.password.data == self.password_repeat.data:
            raise ValidationError(f'Provided passwords do not match.')
            #REGEX DOWN UNDER
        if not re.match('^1234$', self.password.data):
            raise ValidationError(f'Provided Password is not 1234.')


class FilterProduceForm(FlaskForm):
    Genre = SelectField('Genre',
                           choices=ProduceCategoryChoices.choices())
    Moviename = SelectField('Movie name (Best to keep empty)',
                        choices=[('', '')] + ProduceItemChoices.choices())
    MainActor = SelectField('Actor',
                          choices=ProduceVarietyChoices.choices())
    sold_by = StringField('Keep this box empty!!!')
    BrainRotScore = FloatField('Brain-rot score (0-10) (Less than or equal to)',
                       validators=[NumberRange(min=0, max=100)])

    submit = SubmitField('Filter')


class AddProduceForm(FlaskForm):
    category = SelectField('Category',
                           validators=[DataRequired()],
                           choices=ProduceCategoryChoices.choices())
    item = SelectField('Item (Subcategory)',
                       validators=[DataRequired()],
                       choices=ProduceItemChoices.choices())
    variety = SelectField('Variety',
                          validators=[DataRequired()],
                          choices=ProduceVarietyChoices.choices())
    unit = SelectField('Unit',
                       validators=[DataRequired()],
                       choices=ProduceUnitChoices.choices())
    price = IntegerField('Price',
                         validators=[DataRequired(), NumberRange(min=0, max=100)])
    farmer_pk = IntegerField('Farmer',
                             validators=[DataRequired()],
                             render_kw=dict(disabled='disabled'))
    submit = SubmitField('Add produce')

    def validate_price(self, field):
        farmer = get_farmer_by_pk(self.farmer_pk.data)
        if farmer is None:
            raise ValidationError("You need to be a farmer to sell produce!")


class BuyProduceForm(FlaskForm):
    submit = SubmitField('Yes, buy it')

    def validate_submit(self, field):
        customer = get_customer_by_pk(current_user.pk)
        if not customer:
            raise ValidationError("You must be a customer in order to create orders.")


class RestockProduceForm(FlaskForm):
    submit = SubmitField('Yes, restock it')
