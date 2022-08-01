from calendar import MONDAY
from datetime import datetime
from random import choices
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, DateField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Email, EqualTo
    
class patientSignUpForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    DOB = DateField('Date of Birth', validators=[InputRequired()])
    emailAddress = StringField('Email', validators=[InputRequired(), Email()])
    username = StringField('Username', validators=[InputRequired()])
    #patientId = StringField('patientId', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])

class doctorSignUpForm(FlaskForm):
    #doctorId = StringField('doctorId', validators=[InputRequired()])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    specialty = SelectField('Specialty', choices=['Internal Medicine', 'Physician', 'Orthopaedic', 'Family Practice', 'Cardiology', 'Opthalmology', 'General Practise', 'Physical Therapist'])
    title = SelectField('Title', choices=['MD', 'Physician', 'Surgeon'])
    phoneNumber = StringField('Phone Number', validators=[InputRequired()])
    emailAddress = StringField('Email', validators=[InputRequired(), Email()])
    companyName = StringField('Company Name', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])

class patientLoginForm(FlaskForm):
    emailAddress = StringField('Email', validators=[InputRequired(), Email()])
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
   
class doctorLoginForm(FlaskForm):
    emailAddress = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class makeAppointment(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    emailAddress = StringField('Email', validators=[InputRequired(), Email()])
    phoneNumber = StringField('Phone Number', validators=[InputRequired()])
    date = DateField('Date', format='%m/%d/%Y')
    reason = TextAreaField('Reason for visit', validators=[InputRequired()])
    
class UploadForm(FlaskForm):
    image = FileField('Image', validators = [FileRequired(), FileAllowed(['jpg','png', 'pdf','Images only!'])])
    