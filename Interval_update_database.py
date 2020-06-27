from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from Layout_table import Base,table_structure
from requests import get
from datetime import date
from datetime import datetime
import os
now = datetime.now()
time = now.strftime("%H:%M:%S")
today = date.today()

#database connect

def database_connect():
    path = 'mysql+mysqlconnector://{}:{}@localhost:{}/{}'.format(os.getenv('User_name'),os.getenv('Password'),os.getenv('Port'),os.getenv('Db_name'))
    engine = create_engine(path)  
    return engine


#session Create

def Session_create(sess_engine):
	sess_maker = sessionmaker()
	sess_maker.configure(bind=sess_engine)
	sess = sess_maker()
	return sess

#update..
    
def update(sess):
    url = 'https://api.tfl.gov.uk/bikepoint'
    response = get(url)
    api_data = response.json()
    for x in api_data:
        id_of_bike = x['id']
        name = x['commonName']
        lat = x['lat']
        long = x['lon']
        for y in x['additionalProperties']:
            if y['key']=='NbBikes':
                no_bikes = y['value']
            if y['key']=='NbEmptyDocks':
                emp_docks = y['value']
            if y['key']=='NbDocks':
                tt_docks = y['value']

        sess.query(table_structure).filter(table_structure.bike_id == id_of_bike).update({"latitude": lat,"longitude":long,"available_bikes":no_bikes,"empty_docks":emp_docks,"total_docks":tt_docks,"date_of_update":today,"time_of_update": time})
    sess.commit()
        
    pass

if __name__ == '__main__':
    eng = database_connect()
    sess = Session_create(eng)
    update(sess)
    
