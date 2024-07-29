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
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/search_date/<start_date><br/>"
        f"/api/v1.0/search_date/<start_date>/<end_date>"
    )

@app.route("/api/v1.0/percipitation")
def percipatation():
    session = Session(engine)

    #Query percicpitation analysis
    query_date = dt.date(2017, 8, 23)
    lyt_date = query_date - dt.timedelta(days=365)
    results = session.query(measurements.date, measurements.prcp).filter(measurements.date > lyt_date).all()
    session.close()

    precipitation = {date:precip for date, precip in results}

    # percipitaction = []
    # for date, prcp in results:
    #     prcp_dict = {}
    #     prcp_dict[date] = prcp
    #     percipitaction.append(prcp_dict)

    return jsonify(precipitation)



@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)

    #Query the stations
    stations_result = session.query(measurements.station).distinct().all()
    session.close()
    return_list = list(np.ravel(stations_result))
    print(return_list)
    return jsonify(return_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    query_date = dt.date(2017, 8, 23)
    lyt_date = query_date - dt.timedelta(days=365)
    most_active_ttm = session.query(measurements.date, measurements.tobs).\
    filter(measurements.date > lyt_date).\
    filter(measurements.station == 'USC00519281').all()

    session.close()
    most_active_result = list(np.ravel(most_active_ttm))
    return jsonify(most_active_result)

@app.route("/api/v1.0/search_date/<start_date>")
def dynamic_route_1(start_date):
    start = dt.datetime.strptime(start_date, "%m%d%Y") #08012015
    data = session.query(func.min(measurements.tobs),
       func.max(measurements.tobs),
       func.avg(measurements.tobs)).filter(measurements.date >= start).all()
    
    

    temperature_to_return = list(np.ravel(data))

    return temperature_to_return

@app.route("/api/v1.0/search_date/<start_date>/<end_date>")
def dynamic_route_2(start_date, end_date):
    start = dt.datetime.strptime(start_date, "%m%d%Y") #08012015
    end = dt.datetime.strptime(end_date, "%m%d%Y")
    data_end = session.query(func.min(measurements.tobs),
       func.max(measurements.tobs),
       func.avg(measurements.tobs)).filter(measurements.date >= start, measurements.date <= end).all()
    
    session.close()
    
    limited_temp_return = list(np.ravel(data_end))

    return limited_temp_return

if __name__ == '__main__':
    app.run(debug=True)