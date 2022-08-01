"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
https://www.youtube.com/watch?v=CiuC5PF4I-A
https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html
This file creates your application.
"""

import re
import uu
from app import app, db, login_manager
import os
from flask import render_template, request, redirect, url_for, flash, jsonify, session, abort
from flask_login import login_user, logout_user, current_user
from flask_login import login_required, LoginManager
from app.forms import patientSignUpForm, doctorSignUpForm, patientLoginForm, doctorLoginForm, makeAppointment
from app.models import *
from flask_wtf.csrf import generate_csrf
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import uuid
from .forms import UploadForm


isPatient=False


def define_db():
    db.drop_all()
    db.create_all()
    try:
        #create a doctor user
        doctor = DoctorsProfile(first_name = "Isaiah", last_name ="McIntyre", specialty = "Internal Medicine", title = "MD", phoneNumber = "876580-1512", emailAddress = "isaiahmcintyre@yahoo.com", companyName = "University Hospital of the West Indies", password="1234")
        #create a patient user
        patient = PatientsProfile(first_name="Dwayne", last_name="Johnson",DOB="07-04-1978", emailAddress="dwayne.johnson@gmail.com", username="Dwayne", password="1234")
        #creat an appointment
        appointment =Appointment( title = "Appointment1", date = "2022-09-09", time = "", url = "https://meet.google.com", booked = False)
        #create a patient record
        patient_record = PatientRecord( patient_illness="Diabetic", medication= "insulin")
        # create patient history
        patient_history1=PatientHistory(age=53, height=166, weight=210, blood_pressure="160/180", blood_sugar="200 mg/dl", temperature=98.6)
        #create a complaint
        complaints=Complaints(list_of_complaints=["Cough", "Headache", "Fever"])
        #create a symptom
        symptoms=Symptoms(list_of_symptoms=[["Yes","headache", "mild"], ["Yes", "Fever", "less than three days"]])
        #create possible causes
        possible_causes=PossibleCauses(possible_causes=[[0.57, "Common Cold"],[0.24, "COVID-19"]]) 
        #create diagnosis
        doctor_diagnosis=DoctorDiagnosis(diagnosis="Patient had Common Flu", prescription= ["DPH Elixir"], filenames=[])

        #add relationships---
        #one to many relationship
        doctor.appointments.append(appointment)
        patient_record.patient_histories.append(patient_history1)
        doctor.list_of_diagnosis.append(doctor_diagnosis)

        #one to one relationship
        patient.record=patient_record
        patient_history1.complaints=complaints
        patient_history1.symptoms=symptoms
        patient_history1.possible_causes=possible_causes
        patient_history1.doctor_diagnosis=doctor_diagnosis

        #many to many reltionship
        doctor.patients.append(patient)
        

        #many to one relationship
        appointment.assigned_patient=patient
        appointment.booked=True
        
        #add users and appointmnet to db----
        db.session.add(doctor)
        db.session.add(patient)
        db.session.add(appointment)
        db.session.add(patient_history1)
        db.session.add(patient_record)
        db.session.add(complaints)
        db.session.add(symptoms)
        db.session.add(possible_causes)
        db.session.add(doctor_diagnosis)
        # commit
        db.session.commit()
        print("Loading pre-defined data...")
        print("doctor's first_name is: ", doctor.first_name)
        print("doctor's first appointment is: ", doctor.appointments[0].date)
        print("doctor's first patient is: ", doctor.patients[0].first_name, " ", doctor.patients[0].last_name)
        print("Is the appointment booked? ", doctor.appointments[0].booked )
        print("Patient's illness is: ", patient.record.patient_illness)
        print("Patient's age is: ", patient.record.patient_histories[0].age)
        print("Appointment is booked by; ", appointment.assigned_patient.username)
        print(appointment.assigned_patient.username, " ID is ", appointment.patient_profile_id)
        print("Patient's complaints of: ", complaints.list_of_complaints)
        print("Symptoms include: ", symptoms.list_of_symptoms[1] )
        print("as well as: ", symptoms.list_of_symptoms[1][1], " ",symptoms.list_of_symptoms[1][2])
        print("The possible diagnosis is ", possible_causes.possible_causes)
        print("Patient Diagnosis from doctor: ",patient.record.patient_histories[0].doctor_diagnosis.diagnosis)
        print("Designated doctor was Dr. : ",patient.record.patient_histories[0].doctor_diagnosis.doctor_profiles.last_name)
    except Exception as exc:
        db.session.rollback()
        print(exc)

events = [
    {
        'title' : 'Appointment1',
        'start' : '2022-08-04',
        'end' : '',
        'url' : 'https://us04web.zoom.us/j/77327765484?pwd=xPWo9HCwMgCHw5AmCpPKcwdjxI6JUr.1'
    },
    {
        'title' : 'Appointment2',
        'start' : '2022-08-04',
        'end' : '2022-08-05',
        'url' : 'https://meet.google.com/yxh-sbub-wpj'
    },
]

#Helper functions
def genid():
    return uuid.uuid4().int

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html', title ='Home') 
       
@app.route('/db_create')
def db_create():
    define_db()
    return redirect(url_for('home'))

@app.route("/getMyHistory")
#@login_required
def getMyHistory():
    print(isPatient)
    if(isPatient):
        return render_template("getMyHistory.html", patient = current_user)
    return render_template('404.html'), 401 

@app.route('/calendar')
def calendar():
    return render_template('calendar.html', events=events)

@app.route('/setAppointment/<int:doctor_id>', methods = ["GET", "POST"])
def setAppointment(doctor_id):
    if not isPatient:
        return render_template('404.html')
    var=Appointment.query.filter_by(doctor_id=doctor_id, booked=False)
    print(var[0].title)
    appointments=[]
    for a in var:
        appointments.append(a)
    print(appointments)
    if request.method == 'POST':
        try:
            print("attempting to get index ")
            index=request.form["date"]
            index=int(index)
            print("index is: ", index)
            selected_appointment=appointments[index]
            print("selected appointment date was: ", selected_appointment.date)
            #add patient to appointment
            selected_appointment.assigned_patient=current_user
            selected_appointment.booked=True
            db.session.commit()
            flash("Appointment made successfully!", 'success')
            return redirect(url_for('patientpage'))
        except Exception as exc:
            print(exc)
            flash("Unable to book appointment please try again!", 'danger')
    return render_template('setAppointment.html', appointments=appointments, doctor_id=doctor_id)


@app.route('/bookAppointment', methods = ["GET", "POST"])
def bookAppointment():
    if request.method == "POST":
        title = request.form['title']
        start = request.form['start']
        end = request.form['end']
        url = request.form['url']
        if end == '':
            end=start
        events.append({
            'title' : title,
            'start' : start,
            'end' : end,
            'url' : url
        },
        )
        try:
            appointment =Appointment( title = title, date = start, time = end, url = url, booked = False)
            current_user.appointments.append(appointment)
            db.session.add(appointment)
            db.session.commit()
            flash("Appointment made", 'success')
            return redirect(url_for("docpage"))
        except Exception as exc:
            flash("Error unable to creaate appointment, please try again", 'danger')
    return render_template('bookAppointment.html', title='Book Appointments')

@app.route('/about/')
def about(): 
    """Render the website's about page."""
    return render_template('about.html', title ='About')

@app.route('/chat/')
def chat(): 
    """Render the website's chatbot page."""
    return render_template('patientpage.html', title ='Chat')

@app.route('/patientpage/')
def patientpage(): 
    """Render the website's DocBot page."""
    return render_template('patientpage.html', title ='DocBotVirtualDoctor')

@app.route('/patientSignUp', methods=["GET","POST"])
def patientSignUp():
    form = patientSignUpForm()
    if request.method == "POST" and form.validate_on_submit():
        emailAddress = form.emailAddress.data
        patient = PatientsProfile.query.filter_by(emailAddress = emailAddress).first()
        patient_info = PatientsProfile(first_name=form.first_name.data, last_name=form.last_name.data, 
        DOB=form.DOB.data, emailAddress=form.emailAddress.data, username=form.username.data, password=form.password.data)
        #patient_info.set_password(form.password.data)
        try:
            if patient is None:
                db.session.add(patient_info)
                db.session.commit()
                flash("Congratulations.... User successfully added", 'success')
                return render_template('home.html', form=form)
            while (patient is not None):
                flash("Error, email address already in use", 'danger')
                return render_template('patientSignUp.html', form=form)
        except Exception as exc: 
            db.session.rollback()
            print (exc)
            flash("Some Internal Error Occurred, Please Try Again",'danger')
            return render_template('patientSignUp.html', form=form)
    else:
        flash("Please check form information and try again")
    return render_template('patientSignUp.html', form=form)

@app.route('/doctorSignUp', methods=["GET", 'POST'])
def doctorSignUp():
    form = doctorSignUpForm()
    if request.method == "POST" and form.validate_on_submit():
        emailAddress = form.emailAddress.data
        doctor = DoctorsProfile.query.filter_by(emailAddress = emailAddress).first()
        doctor_info = DoctorsProfile(first_name = form.first_name.data, last_name = form.last_name.data, specialty = form.specialty.data,
        title = form.title.data, phoneNumber = form.phoneNumber.data, emailAddress = form.emailAddress.data, companyName = form.companyName.data, password=form.password.data)
        try:
            if doctor is None:
                db.session.add(doctor_info)
                db.session.commit()
                flash("Congratulations.... User successfully added", 'success')
                return render_template('home.html', form=form)
            while (doctor is not None):
                flash("Error, email address already in use", 'danger')
                return render_template('doctorSignUp.html', form=form)
        except Exception as exc: 
            db.session.rollback()
            print (exc)
            flash("Some Internal Error Occurred, Please Try Again",'danger')
            return render_template('doctorSignUp.html', form=form)
    else:
        flash("Please check form information and try again")
    return render_template('doctorSignUp.html', form=form)

@app.route("/doclogin", methods=["GET", "POST"])
def doclogin():
    global isPatient
    if current_user.is_authenticated:
        return render_template("loggedin.html",title = 'Already Logged In')
    form = doctorLoginForm()
    if request.method =='POST':
        emailAddress = form.emailAddress.data
        password = form.password.data
        doctor = DoctorsProfile.query.filter_by(emailAddress = emailAddress).first()
        if doctor is not None and check_password_hash(doctor.password, password):
            isPatient=False
            login_user(doctor)
            #print("is the patient logged in: ", session['isPatient'])
            flash("You have been logged in!", 'success')
            return render_template('docpage.html', Title = "Welcome Doctor")
        else:
            flash("Credentials does not match", 'danger')
    return render_template('doclogin.html', form=form)

@app.route("/patientlogin", methods=["GET", "POST"])
def patientlogin():
    global isPatient
    print("Step 1")
    if current_user.is_authenticated:
        print("Step 2")
        return render_template("loggedin.html",title = 'Already Logged In')
    form = patientLoginForm()
    print("Step 3")
    if request.method =='POST':
        print("Step 4")
        username = form.username.data
        emailAddress = form.emailAddress.data
        password = form.password.data
        patient = PatientsProfile.query.filter_by(username = username).first()
        if patient is not None and check_password_hash(patient.password, password):
            isPatient=True
            print("Step 5")
            login_user(patient)
            print("This patient is: ", current_user)
            print("is the patient logged in: ", isPatient)
            flash("You have been logged in!", 'success')
            return render_template('patientpage.html', Title = "Welcome patient")
        else:
            print("Step 6")
            flash("Credentials does not match", 'danger')
    print("Step 7")
    return render_template('patientlogin.html', form=form)

@app.route("/appointments", methods=["GET", "POST"])
def appointments():
    form = makeAppointment()
    if request.method == "GET":
        first_name = form.first_name.data
    return render_template('appointments.html', form=form)


@app.route("/logout")
@login_required
def logout():
    global isPatient
    logout_user()
    isPatient=False
    flash("You have been logged out!", 'success')
    return redirect(url_for('home'))

# Update database record for patient info.
# /<string:patientId>
@app.route("/update/<int:patientId>", methods=["GET", "POST"])
#@login_required
def update_patient_record(patientId=0):
    
    # Get a form ()
    form = patientSignUpForm()
    print(form)

    # Getting patient info from database
    form_field_to_update = PatientsProfile.query.filter_by(id = patientId).first()
    print("id:", patientId)
    print("form to update: ",form_field_to_update)
    
    
    if request.method == "POST":
        try:
            form_field_to_update.first_name = form.first_name.data
            form_field_to_update.last_name = form.last_name.data
            form_field_to_update.DOB = form.DOB.data
            form_field_to_update.emailAddress = form.emailAddress.data
            form_field_to_update.username = form.username.data
            #
            # form_field_to_update.password = form.password.data
        
            db.session.commit()
            flash("Patient's data was successfully updated.")
            return render_template("update.html", form=form, form_field_to_update=form_field_to_update, User=current_user) #
        
        except Exception as exc: 
            db.session.rollback()
            print (exc)
            flash("Sorry, patient doesn't exist",'danger')
            return render_template("update.html", form=form, form_field_to_update=form_field_to_update, User=current_user)
    else:
        return render_template("update.html", form=form, form_field_to_update=form_field_to_update, User=current_user)
   

@login_manager.user_loader
def load_user(id):
    if (isPatient):
        return PatientsProfile.query.filter_by(id=id).first()
    else:
        return DoctorsProfile.query.filter_by(id=id,).first()

###
# The functions below should be applicable to all Flask apps.
###

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if not session.get('logged_in'):
        abort(401)

    # Instantiate your form class
    imageForm = UploadForm()
    
    # Validate file upload on submit
    if request.method == 'POST':
        # Get file data and save to your uploads folder
        image = imageForm.image.data
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))

        flash('File Saved', 'success')
        return redirect(url_for('home'))

    return render_template('uploads.html') 


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
