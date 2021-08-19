# Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.

# Use Flask to create your routes.
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# set up database and classes
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)  

Measurement = Base.classes.measurement
Station = Base.classes.station

# create flask
app = Flask(__name__)
# Routes

# /

# Home page.
# List all routes that are available.
@app.route("/")
def home_page():
    return(
        f"Welcome to the home page<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start> and /api/v1.0/<start>/<end>"
    )

# /api/v1.0/precipitation
# Convert the query results to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data"""

    session = Session(engine)
    date_year_ago = dt.datetime(2017, 8, 23) - dt.timedelta(days=365)
    prcp_results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > date_year_ago).\
        order_by(Measurement.date).all()
    # print(prcp_results)
    ret = {x:y for x,y in prcp_results}
    # print(ret)
    session.close()
    return jsonify(ret)



# /api/v1.0/stations
# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    """Return the weather stations"""
    session = Session(engine)
    station_activity = session.query(Station.station).all()
    # print(station_activity)
    session.close()
    return jsonify([x[0] for x in station_activity])


# /api/v1.0/tobs
# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    """Return the weather stations"""
    session = Session(engine)
    station_id = "USC00519281"
    date_year_ago = dt.datetime(2017, 8, 23) - dt.timedelta(days=365)
    obs_results = session.query(Measurement.tobs, Measurement.date).\
        filter(Measurement.date > date_year_ago).\
        filter(Measurement.station == station_id).\
        order_by(Measurement.date).all()
    # print(obs_results)
    session.close()
    return jsonify([x[0] for x in obs_results])


# /api/v1.0/<start> and /api/v1.0/<start>/<end>/api/v1.0/2017-06-13
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def status(start, end=None):
    """Return the weather stations"""
    session = Session(engine)
    sel = (func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))
    station_id = "USC00519281"
    start = dt.datetime.strptime(start, "%Y-%m-%d")
    # date_year_ago = dt.datetime(2017, 8, 23) - dt.timedelta(days=365)
    obs_results = session.query(*sel).\
        filter(Measurement.station == station_id).\
        filter(Measurement.date >= start)
    if end:
        end = dt.datetime.strptime(end, "%Y-%m-%d")
        obs_results = obs_results.filter(Measurement.date <= end)
    obs_results = obs_results.all()
    # print(obs_results)
    # return jsonify({x:y for x, y in obs_results})
    session.close()
    return jsonify(list(np.ravel(obs_results)))


if __name__ == "__main__":
    app.run(debug=True)