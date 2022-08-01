import email
from pydoc import doc
from . import db
from werkzeug.security import generate_password_hash
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base

patient_list = db.Table(
        "patient_list",
        db.Column("doc_id", db.Integer, db.ForeignKey("doctor_profiles.id"), primary_key=True),
        db.Column("pat_id", db.Integer, db.ForeignKey("patient_profiles.id"), primary_key=True),
)

"""doctor = Table(
        "attendsTo",
        Column("id", db.Integer, db.ForeignKey("id"), primary_key=True),
        Column("id", db.Integer, db.ForeignKey("id"), primary_key=True),
)
"""
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

    # one doctor to many appointments
    appointments=relationship("Appointment", backref="doctor_profiles", lazy="select")
    
    #many to many relationship between doctor and patients
    patients=relationship("PatientsProfile", secondary=patient_list, backref="assigned_patient") # backref is for preferred classname for the table that is required
    
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

    #one patient can have many appointment
    
    #many to many relationship between patient and doctor

    #one to one relationship between patient_records and patient
    record=db.relationship("PatientRecord", backref="my_patient", lazy="select", uselist=False)
    
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
    title = db.Column(db.String(255))
    date = db.Column(db.String(255))
    time = db.Column(db.String(255))
    url = db.Column(db.String(255))
    booked = db.Column(db.Boolean)

    #many appointments to one doctor
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor_profiles.id"))

    #many appointment to one patient
    patient_profile_id = db.Column(db.Integer, db.ForeignKey("patient_profiles.id"))
    assigned_patient = relationship("PatientsProfile", backref="appointments", lazy="select")
    def __init__(self, title, date, time, url, booked):
        self.title = title
        self.date = date
        self.time = time
        self.url = url
        self.booked = booked

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
        return '<Appointment %r>' % (self.id)

class AppointmentSchedule(db.Model):
    __tablename__ = 'appointment_schedule'
    id = db.Column(db.Integer, primary_key=True)
    doctor_name = db.Column(db.String(160))
    time = db.Column(db.String(60))
    date = db.Column(db.DateTime)

    #one to one relationship between doctor and appointment schedule

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
    patient_illness = db.Column(db.String(160))
    medication = db.Column(db.String(255))

    #one to one relationship between patient_record and patient
    patient_profile_id =db.Column(db.Integer, db.ForeignKey("patient_profiles.id"))

    #one patient_record to many patient_histories
    patient_histories=relationship("PatientHistory", backref="patient_record", lazy="select")

    def __init__(self, patient_illness, medication):
        self.patient_illness = patient_illness
        self.medication = medication

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
        return '<PatientRecord %r>' % (self.id)

class PatientHistory(db.Model):
    __tablename__ = 'patient_history'
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    blood_pressure = db.Column(db.String(255))
    blood_sugar = db.Column(db.String(255))
    temperature = db.Column(db.Float)

   #many patient_histories to one patient_record
    patient_record_id= db.Column(db.Integer, db.ForeignKey("patient_record.id"))

def __init__(self, age, height, weight, blood_pressure, blood_sugar, temperature):
        self.age = age
        self.height = height
        self.weight = weight
        self.blood_pressure = blood_pressure
        self.blood_sugar = blood_sugar
        self.temperature = temperature


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
    return '<PatientHistory %r>' % (self.id)
 

