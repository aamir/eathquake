__author__ = 'aamir'
import os
import sqlite3
import requests
import datetime

api_endpoint = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson"


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Data:
    def __init__(self, last_days):
        self.data_file = 'earthquakes.db'
        self.date_file = 'date.txt'
        self.until = last_days
        if not os.path.exists(self.data_file):
            self.conn = sqlite3.connect(self.data_file)
            self.conn.row_factory = dict_factory
            self.c = self.conn.cursor()
            # Create table
            self.c.execute(
                '''CREATE TABLE quakes (quake_id TEXT PRIMARY KEY, place TEXT, time datetime, lat real, lon real, mag real)''')
            # Save (commit) the changes
            self.conn.commit()
        else:
            self.conn = sqlite3.connect(self.data_file)
            self.conn.row_factory = dict_factory
            self.c = self.conn.cursor()

    def get(self):
        if os.path.exists(self.date_file):
            f = open(self.date_file, 'r')
            strDate = f.readline()
            if strDate:
                last_updated_date_time = datetime.datetime.strptime(strDate, "%Y-%m-%d %H:%M:%S")
                current_date_time = datetime.datetime.now()
                margin = datetime.timedelta(minutes=15)
                if current_date_time - last_updated_date_time >= margin:
                    return self.refetch()
                else:
                    return self.db()
            else:
                self.refetch()
        else:
            return self.refetch()

    def db(self):
        current_date_time = (datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds()
        margin = datetime.timedelta(days=self.until).total_seconds()
        greater_than_date_time = current_date_time - margin
        strTime = str(greater_than_date_time)
        dbmodels = self.c.execute(''' SELECT * FROM quakes WHERE time >= ? ''',
                                  (strTime, )).fetchall()
        self.conn.close()
        return dbmodels

    def refetch(self):
        dbmodels = []
        db_t = []
        r = requests.get(api_endpoint)
        data = r.json()
        features = data['features']
        for feature in features:
            dbmodel = dict()
            geometry = feature['geometry']
            properties = feature['properties']
            cordinates = geometry['coordinates']
            dbmodel['quake_id'] = feature['id']
            dbmodel['place'] = properties['place']
            dbmodel['lon'] = cordinates[0]
            dbmodel['lat'] = cordinates[1]
            dbmodel['mag'] = properties['mag']
            dbmodel['time'] = properties['time']/1000
            db_t.append((dbmodel['quake_id'], dbmodel['place'], dbmodel['time'], dbmodel['lat'], dbmodel['lon'],
                         dbmodel['mag']))
            dbmodels.append(dbmodel)
        # TODO make db call async
        self.c.executemany("INSERT OR REPLACE INTO quakes VALUES (?,?,?,?,?,?)", db_t)
        self.conn.commit()
        f = open(self.date_file, 'w')
        current_date_time = datetime.datetime.now()
        f.write(current_date_time.strftime("%Y-%m-%d %H:%M:%S"))
        return self.db()
