import email
from pydoc import doc
from . import db
from werkzeug.security import generate_password_hash
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base




class DoctorsProfile(db.Model):
    __tablename__ = 'doctor_profiles'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    specialty = db.Column(db.String(80))
    title = db.Column(db.String(80))
    phoneNumber = db.Column(db.String(80))
    emailAddress = db.Column(db.String(160), unique =True)
    companyName  = db.Column(db.String(80))
    password = db.Column(db.String(255))

    def __init__(self,first_name, last_name, specialty,
    title, phoneNumber, emailAddress, companyName, password):
        self.first_name = first_name
        self.last_name = last_name
        self.specialty = specialty
        self.title = title
        self.phoneNumber = phoneNumber
        self.emailAddress = emailAddress
        self.companyName = companyName
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return str(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return self.title + " " + self.last_name
        #return '<DoctorsProfile %r>' % (self.emailAddress)

class PatientsProfile(db.Model):
    # You can use this to change the table name. The default convention is to use
    # the class name. In this case a class name of PatientsProfile would create a
    # patient_profile (singular) table, but if we specify __tablename__ we can change it
    # to `user_profiles` (plural) or some other name.
    __tablename__ = 'patient_profiles'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    DOB = db.Column(db.DateTime)
    emailAddress = db.Column(db.String(160))
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255))

    def __init__(self, first_name, last_name, DOB, emailAddress, username, password):
        self.first_name = first_name
        self.last_name = last_name
        self.DOB = DOB
        self.emailAddress = emailAddress
        self.username = username
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return str(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return (self.username)
        #return '<PatientsProfile %r>' % (self.username)

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    emailAddress = db.Column(db.String(160))
    first_name = db.Column(db.String(160))
    last_name = db.Column(db.String(80))
    phoneNumber = db.Column(db.String(80))
    date = db.Column(db.DateTime)
    doctor = db.Column(db.String(80))
    reason = db.Column(db.String(255))
    link = db.Column(db.String(255))

    def __init__(self, emailAddress, first_name, last_name, phoneNumber, date, doctor, reason, link):
        self.emailAddress = emailAddress
        self.first_name = first_name
        self.last_name = last_name
        self.phoneNumber = phoneNumber
        self.date = date
        self.doctor = doctor
        self.reason = reason
        self.link = link

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return str(self.emailAddress)  # python 2 support
        except NameError:
            return str(self.emailAddress)  # python 3 support

    def __repr__(self):
        return '<Appointment %r>' % (self.emailAddress)

class AppointmentSchedule(db.Model):
    __tablename__ = 'appointment_schedule'
    id = db.Column(db.Integer, primary_key=True)
    doctor_name = db.Column(db.String(160))
    time = db.Column(db.String(60))
    date = db.Column(db.DateTime)

    def __init__(self, doctor_name, time, date, emailAddress): 
        self.doctor_name = doctor_name
        self.time = time
        self.date = date
        self.emailAddress = emailAddress

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return str(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<AppointmentSchedule %r>' % (self.doctor_name)

class PatientRecord(db.Model):
    __tablename__ = 'patient_record'
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(160))
    patient_illness = db.Column(db.String(160))
    patient_report = db.Column(db.String(255))
    medication = db.Column(db.String(255))
    phoneNumber = db.Column(db.String(255))

    def __init__(self, patientname, patient_illness, patient_report, medication, phoneNumber):
        self.patient_name = patientname
        self.patient_illness = patient_illness
        self.patient_report = patient_report
        self.medication = medication
        self.phoneNumber = phoneNumber

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return str(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<PatientRecord %r>' % (self.patient_name)

