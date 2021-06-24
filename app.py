"""
Backend script to handle frontend request to database and return to frontend UI
"""
from typing import Text
from flask import Flask, render_template, request, flash, redirect
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
import xml.etree.ElementTree as et
from sendEmail import send_email
from sqlalchemy.sql import func
from werkzeug.utils import secure_filename
import os

# Get the credential from credentials.xml
#creds = et.parse('credentials.xml').getroot()
#dbname = creds[0].text
#user = creds[1].text
#pwd = creds[2].text
#connstring = f"postgresql://{user}:{pwd}@localhost/{dbname}"
connstring = 'postgresql://iqgitdvwvjwpvf:1805e57bd9906c45552cc802be4085f62b42a1157c8c1e7843409e5bbcdece1d@ec2-52-5-247-46.compute-1.amazonaws.com:5432/dbf11cvkutv4e2?sslmode=require'

# Create flask object
app = Flask(__name__)
# Create flask db using sqlalchemy 
app.config['SQLALCHEMY_DATABASE_URI']=connstring

db = SQLAlchemy(app)

class Data(db.Model):
    """ Create Data class to store data in database
    """
    __tablename__="data"
    id = db.Column(db.Integer, primary_key=True) 
    name_ = db.Column(db.String(150))
    email_ = db.Column(db.String(120), unique=True)
    dob_ = db.Column(db.Date)
    height_ = db.Column(db.Integer)
    upload_file_ = db.Column(db.String(5))

    def __init__(self, name, email,dob, height, upload_file):
        self.name_ = name
        self.email_ = email
        self.dob_ = dob
        self.height_ = height
        self.upload_file_ = upload_file

# command for rounting the website pages
@app.route("/")
def index():
    # clear the sample email, just for testing purposes
    try:
        # this email use for testing purposes
        db.session.query(Data).filter(Data.email_=="smartconan808@gmail.com").delete()
        db.session.commit()
    except:
        db.session.rollback()    
    return render_template("index.html")

@app.route("/success", methods=['POST','GET'])
def success():
    if request.method=='POST': 
        name = request.form["name"]
        email = request.form["email"]
        dob = request.form["dob"]
        height = request.form["height"]

        if db.session.query(Data).filter(Data.email_==email).count() == 0:
            if request.files["upload_file"].filename != '':
                file = request.files["upload_file"]
                # Save the uploaded file
                #uploadedFile = "uploaded_file_"+file.filename
                #parentPath = os.getcwd()
                # check whether the directory is exists
                #if os.path.isdir(os.path.join(parentPath, "uploaded_files", name)):
                #    file.save(os.path.join(parentPath, "uploaded_files", name, secure_filename(uploadedFile)))
                #else:
                #    os.mkdir(os.path.join(parentPath, "uploaded_files", name))
                #    file.save(os.path.join(parentPath, "uploaded_files", name, secure_filename(uploadedFile)))
                upload_file = "Yes"    
            else:
                upload_file = "No"

            # Create the data object
            data = Data(name, email, dob, height, upload_file)
            db.session.add(data)
            db.session.commit()

            # Calculate average height
            ave_height = db.session.query(func.avg(Data.height_)).scalar()
            ave_height = round(ave_height,1)
            tot_users = db.session.query(Data).count()
            send_email(name, email, height, ave_height, tot_users)
            return render_template("success.html")
    
    return render_template("index.html", text="Email already exists.")         

if __name__=="__main__":
    try:
        db.create_all()
    except:
        print("Error in database.")    
    app.run(debug=True)
