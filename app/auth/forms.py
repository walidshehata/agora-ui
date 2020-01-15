from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    firstname = StringField('First Name',
                            validators=[DataRequired(message='First name is a required field'),
                                        Length(min=2, max=28, message='First name must be between 2-28 chars'),
                                        Regexp('^[a-zA-Z ]*$', message='Only [a-z], [A-Z] allowed')])

    lastname = StringField('Last Name',
                           validators=[DataRequired(message='Last name is a required field'),
                                       Length(min=2, max=28, message='Last name must between 2-28 chars'),
                                       Regexp('^[a-zA-Z ]*$', message='Only [a-z], [A-Z] allowed')])
    mail = StringField('Email',
                       validators=[DataRequired(message='Email is a required field'),
                                   Email(message='Please use a valid email address')])
    company = StringField('Company',
                          validators=[DataRequired(message='Company name is required'),
                                      Length(min=2, max=50, message='Company name must be between 2-50 chars'),
                                      Regexp('^[a-zA-Z0-9 ]*$]', message='Only [a-z], [A-Z], [0-9] allowed')])
    mobile = StringField('Mobile',
                         validators=[DataRequired(message='Mobile number is required'),
                                     Length(min=4, max=40),
                                     Regexp('^[()-+0-9 ]*$', message='Enter a valid mobile number')])
    username = StringField('Username',
                           validators=[DataRequired(message='Username is required'),
                                       Length(min=4, max=30, message='Username must be between 4-30 chars'),
                                       Regexp('^[a-zA-Z0-9._-]*$', message='Allowed [a-z], [A-Z], . - _')])
    password = PasswordField('Password',
                             validators=[DataRequired(message='Password field is required'),
                                         Length(min=8, max=40, message='Password minimum length is 8 chars'),
                                         EqualTo('password_confirm', message='Passwords must match')])
    password_confirm = PasswordField('Repeat Password',
                                     validators=[DataRequired(message='Enter the password again')])
    submit = SubmitField('Create')
