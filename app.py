"""
Backend script to handle frontend request to database and return to frontend UI
"""
from typing import Text
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
import xml.etree.ElementTree as et
from sendEmail import send_email
from sqlalchemy.sql import func

# Get the credential from credentials.xml
creds = et.parse('credentials.xml').getroot()
dbname = creds[0].text
user = creds[1].text
pwd = creds[2].text
connstring = f"postgresql://{user}:{pwd}@localhost/{dbname}"

# Create flask object
app = Flask(__name__)
# Create flask db using sqlalchemy 
app.config['SQLALCHEMY_DATABASE_URI']=connstring
db = SQLAlchemy(app)

# Create Data class for the input object to store in db
class Data(db.Model):
    __tablename__="data"
    id = db.Column(db.Integer, primary_key=True) 
    email_ = db.Column(db.String(120), unique=True)
    height_ = db.Column(db.Integer)

    def __init__(self, email, height):
        self.email_ = email
        self.height_ = height

# command for rounting the website pages
@app.route("/")
def index():
    # clear the sample email, just for testing
    # TODO: delete this in prod
    try:
        db.session.query(Data).delete()
        db.session.commit()
    except:
        db.session.rollback()    
    return render_template("index.html")

@app.route("/success", methods=['POST'])
def success():
    if request.method=='POST': 
        email = request.form["email"]
        height = request.form["height"]
        if db.session.query(Data).filter(Data.email_==email).count() == 0:
            data = Data(email,height)
            db.session.add(data)
            db.session.commit()
            # Calculate average height
            ave_height = db.session.query(func.avg(Data.height_)).scalar()
            ave_height = round(ave_height,1)
            tot_users = db.session.query(Data).count()
            print(ave_height, tot_users)
            send_email(email, height, ave_height, tot_users)
            return render_template("success.html")

    return render_template("index.html", text="Email already exists.")         

if __name__=="__main__":
    db.create_all()
    app.run(debug=True)
