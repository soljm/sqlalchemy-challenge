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
# Homepage route
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

# Create function that returns date of one year ago
def one_year_ago(session):
    return session.query(func.max(func.date(func.julianday(Measurement.date, '-1 year')))).scalar_subquery()

# Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create a session
    session = Session(engine)

    # Query precipitation data within the last 12 months
    prcp_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago(session)).all()

    # Close session
    session.close()

    # Create dictionary from precipitation data
    prcp_dict = {}
    for date, prcp in prcp_data:
        prcp_dict[date] = prcp

    # Return dictionary (already in JSON)
    return prcp_dict

# Stations route
@app.route("/api/v1.0/stations")
def stations():
    # Create session
    session = Session(engine)

    # Query station list
    station_results = session.query(Station.station).all()

    # Close session
    session.close()

    # Create list of station IDs
    station_list = []
    for station, in station_results:
        station_list.append(station)

    # Return list (already in JSON)
    return station_list

# Temperature route
@app.route("/api/v1.0/tobs")
def tobs():
    # Create session
    session = Session(engine)

    # Subquery to find most active station ID
    most_active = session.query(Measurement.station)\
    .group_by(Measurement.station).order_by(func.count(Measurement.station).desc())\
    .limit(1).scalar_subquery()

    # Query for temperature of most active station within 12 months
    temp = session.query(Measurement.date, Measurement.tobs)\
    .filter(Measurement.date >= one_year_ago(session)).filter(Measurement.station == most_active).all()

    # Close session
    session.close()

    # Create list of temperature data
    tobs_list = []
    for date, tobs in temp:
        tobs_dict = {
            "Date": date,
            "Temperature": tobs
        }
        tobs_list.append(tobs_dict)
    
    # Return list of temperature (already in JSON)
    return tobs_list

# Dynamic start date route
@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create session
    session = Session(engine)

    # Query min, max, and average of user inputed start date 
    tmin, tmax, tavg = session.query(
            func.min(Measurement.tobs),
            func.max(Measurement.tobs),
            func.avg(Measurement.tobs)
        ).filter(Measurement.date >= start).first()

    # Close session
    session.close()

    # Return min, average, and max (alraedy in JSON)
    return {
        "TMIN": tmin,
        "TAVG": tavg,
        "TMAX": tmax
    }

# Dynamic start and end date route
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    # Create session
    session = Session(engine)

    # Query min, max, and average of temperature between dates (inclusive) 
    tmin, tmax, tavg = session.query(
            func.min(Measurement.tobs),
            func.max(Measurement.tobs),
            func.avg(Measurement.tobs)
        ).filter(Measurement.date >= start).filter(Measurement.date <= end).first()

    # Close session
    session.close()

    # Return min, average, and max (already in JSON)
    return {
        "TMIN": tmin,
        "TAVG": tavg,
        "TMAX": tmax
    }

# Run app
if __name__ == "__main__":
    app.run(debug=True)