# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
stations = Base.classes.station
measurements = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all avaialable api route."""
    return (
        f"Available routes:<br/>"
        f"/api/v1.0/percipitation<br/>"
        f"/api/v1.0/stations"
    )

@app.route("/api/v1.0/percipitation")
def names():
    session = Session(engine)

    #Query percicpitation analysis
    query_date = dt.date(2017, 8, 23)
    lyt_date = query_date - dt.timedelta(days=365)
    results = session.query(measurements.date, measurements.prcp).filter(measurements.date > lyt_date).all()
    session.close()

    percipitaction = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        percipitaction.append(prcp_dict)

    return jsonify(percipitaction)

if __name__ == '__main__':
    app.run(debug=True)