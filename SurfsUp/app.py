# Import the dependencies.
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def homepage():
    return """
    Welcome to the Climate API!<br/>
    Available Routes:<br/>
    /api/v1.0/precipitation<br/>
    /api/v1.0/stations<br/>
    /api/v1.0/tobs<br/>
    /api/v1.0/&lt;start&gt;<br/>
    /api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>
"""

def one_year_ago(session):
    return session.query(func.max(func.date(func.julianday(Measurement.date, '-1 year')))).scalar_subquery()

def most_active(session):
    return session.query(Measurement.station)\
    .group_by(Measurement.station).order_by(func.count(Measurement.station).desc())\
    .limit(1).scalar_subquery()

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create a session
    session = Session(engine)

    prcp_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago(session)).all()

    session.close()

    # Create dictionary
    prcp_dict = {}
    for date, prcp in prcp_data:
        prcp_dict[date] = prcp

    return prcp_dict

@app.route("/api/v1.0/stations")
def stations():
    # Create session
    session = Session(engine)

    station_results = session.query(Station.station).all()

    session.close()

    # Create list
    station_list = []
    for station, in station_results:
        station_list.append(station)

    return station_list

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    temp = session.query(Measurement.date, Measurement.tobs)\
    .filter(Measurement.date >= one_year_ago(session)).filter(Measurement.station == most_active(session)).all()

    session.close()

    # Create list
    tobs_list = []
    for date, tobs in temp:
        tobs_dict = {
            "date": date,
            "tobs": tobs
        }
        tobs_list.append(tobs_dict)
    
    return tobs_list

@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)

    tmin, tmax, tavg = session.query(
            func.min(Measurement.tobs),
            func.max(Measurement.tobs),
            func.avg(Measurement.tobs)
        ).filter(Measurement.date >= start).first()

    session.close()
    return {
        "TMIN": tmin,
        "TAVG": tavg,
        "TMAX": tmax
    }

@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    session = Session(engine)

    tmin, tmax, tavg = session.query(
            func.min(Measurement.tobs),
            func.max(Measurement.tobs),
            func.avg(Measurement.tobs)
        ).filter(Measurement.date >= start).filter(Measurement.date <= end).first()

    session.close()
    return {
        "TMIN": tmin,
        "TAVG": tavg,
        "TMAX": tmax
    }

if __name__ == "__main__":
    app.run(debug=True)