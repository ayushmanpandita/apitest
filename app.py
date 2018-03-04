from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request, url_for, redirect
from math import sin, cos, sqrt, atan2,radians
from django_earthdistance.models import EarthDistanceQuerySet
import sys, psycopg2

#import geopy.distance

app=Flask(__name__)

#Connecting with role : 'jimmy', with password : 'hello123'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://jimmy:hello123@localhost/jimmy'

db=SQLAlchemy(app)


class Record(db.Model):

    key=db.Column(db.String(20), primary_key=True, unique=True)
    place=db.Column(db.String(100), unique=False)
    admin_name1 = db.Column(db.String(100), unique=False)
    latitude = db.Column(db.Float, unique=False)
    longitude = db.Column(db.Float, unique=False)
    accuracy = db.Column(db.Integer, unique=False)

    objects = EarthDistanceQuerySet.as_manager()

    def __init__(self,key,place,admin_name1,latitude, longitude, accuracy):
        self.key=key
        self.place=place
        self.admin_name1=admin_name1
        self.latitude=latitude
        self.longitude=longitude
        self.accuracy=accuracy


#Homepage
@app.route("/")
def index():
    #one=Record.query.filter_by().first()
    return render_template('home.html')

#web-app for post_rec form
@app.route("/post_location")
def poster():
    #one=Record.query.filter_by().first()
    return render_template('add_rec.html')

# required POST API : post_rec | Interview Question 1
@app.route('/post_rec', methods=['POST'])
def post_user():
    print("post_rec entered...")
    rec=Record(request.form['key'],request.form['address'],request.form['city'], request.form['latitude'],request.form['longitude'],5) #extract post details from form

    myRecord=Record.query.all()

    ch=True

    try:
        for r in myRecord:

            # A try block used to handle cases where longitude and latitutde not present in the record
            try:
                print(r.latitude,r.longitude,abs(r.longitude-(float)(rec.longitude)),abs(r.latitude-(float)(rec.latitude)))

            except:
                continue

           # Checks if any point in the record lies within 3 KMs of the location posted
            if(abs(r.longitude-(float)(rec.longitude))<0.02 and abs(r.latitude-(float)(rec.latitude))<0.02):
                print("Coordinates too close")
                raise Exception

    except:
        print("Coordinates too close! Record not added")
        message="Coordinates too close to an existing location! Record not added"
        return render_template('Message.html', message=message)

    # try block used to handle cases where we try to add record with duplicate pin-code
    try:
        db.session.add(rec)
        db.session.commit()

    except:
        ch=False
        print("Duplicate Key Value!")
        message = "Pin Code specified already exists in the database! Record not added"
        return render_template('Message.html', message=message)

    message = "Record added Successfully"
    return render_template('Message.html', message=message)

# required GET API : get_using_self | Interview Question 2
@app.route("/get_using_self", methods=['GET'])
def get_radius():

    return render_template('get_postgres_self.html')

@app.route("/get_using_postgres", methods=['GET'])
def get_radius_earth():

    return render_template('get_postgres_earth.html')


# using earthdistance
@app.route("/display_earth", methods=['POST'])
def useearth():

    #connect to database for executing postgresql commands from ide
    conn = None
    try:
        conn = psycopg2.connect("dbname = 'jimmy' user = 'jimmy' host = 'localhost' password = 'hello123'")
        print("Connected...")
    except:
        print("I am unable to connect the database:")
        #sys.exit(1)

    #execute the following command using earthdistance

    lat=str(request.form['latitude'])
    lon=str(request.form['longitude'])
    rad=str((float(request.form['radius']))*1000)

    abc="hi"+lat


    curs = conn.cursor()
    command="SELECT * FROM record WHERE earth_box(ll_to_earth("+lat+","+lon+"),"+rad+") @>ll_to_earth(record.latitude,record.longitude); ;"
    curs.execute(command)

    new_list=list()

    for row in curs:
        new_list.append(row)
    print(curs)

    return render_template('display_earthdistance.html', records=new_list)


#web-app/page to display the results of get_using_postgres
@app.route("/display",methods=['POST'])
def display():

    myRecord=Record.query.all()

    lat=(float)(request.form['latitude'])
    long=(float)(request.form['longitude'])
    r= float(request.form['radius'])

    print(lat,long)

    l=list()

    for rec in myRecord:
        try:
            print(".")
            R = 6373.0


            lat1 = radians(lat)
            lon1 = radians(long)
            lat2 = radians(rec.latitude)
            lon2 = radians(rec.longitude)

            dlon = lon2 - lon1
            dlat = lat2 - lat1

            a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))

            distance = R * c
            print(distance,lat2,lon2)
            if(distance<=r):
                l.append(rec)
        except:
            continue

    print(l)
    return render_template('display.html', records=l)


if __name__=='__main__':
    app.run(debug=True)
