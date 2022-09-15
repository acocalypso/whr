# Webhook receiver for getting data from ATV devices
# replacement for ATVdetails
#
__orig_author__ = "GhostTalker"
__modified_by__ = "AcoVanConis"
__copyright__ = "Copyright 2022, The GhostTalker project"
__version__ = "0.2.3"
__status__ = "DEV"

import os
import sys
import time
import datetime
import json
import requests
import configparser
import pymysql
from mysql.connector import Error
from mysql.connector import pooling
from flask import Flask, request

## read config
_config = configparser.ConfigParser()
_rootdir = os.path.dirname(os.path.abspath('config.ini'))
_config.read(_rootdir + "/config.ini")
_host = _config.get("socketserver", "host", fallback='0.0.0.0')
_port = _config.get("socketserver", "port", fallback='5050')
_mysqlhost = _config.get("mysql", "mysqlhost", fallback='127.0.0.1')
_mysqlport = _config.get("mysql", "mysqlport", fallback='3306')
_mysqldb = _config.get("mysql", "mysqldb")
_mysqluser = _config.get("mysql", "mysqluser")
_mysqlpass = _config.get("mysql", "mysqlpass")

## do validation and checks before insert
def validate_string(val):
   if val != None:
        if type(val) is int:
            #for x in val:
            #   print(x)
            return str(val).encode('utf-8')
        else:
            return val

## create connection pool and connect to MySQL
try:
    connection_pool = pooling.MySQLConnectionPool(pool_name="mysql_connection_pool",
                                                  pool_size=5,
                                                  pool_reset_session=True,
                                                  host=_mysqlhost,
                                                  port=_mysqlport,
                                                  database=_mysqldb,
                                                  user=_mysqluser,
                                                  password=_mysqlpass)

    print("Create connection pool: ")
    print("Connection Pool Name - ", connection_pool.pool_name)
    print("Connection Pool Size - ", connection_pool.pool_size)

    # Get connection object from a pool
    connection_object = connection_pool.get_connection()

    if connection_object.is_connected():
        db_Info = connection_object.get_server_info()
        print("Connected to MySQL database using connection pool ... MySQL Server version on ", db_Info)

        cursor = connection_object.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("Your connected to - ", record)

except Error as e:
    print("Error while connecting to MySQL using Connection pool ", e)

finally:
    # closing database connection.
    if connection_object.is_connected():
        cursor.close()
        connection_object.close()
        print("MySQL connection is closed")

## webhook receiver
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        if request.json["type"] is 'raid':
            print("Data received from Webhook is: ", request.json)
            # parse json data to SQL insert
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            latitude = validate_string(request.json["message"]["latitude"])
            longitude = validate_string(request.json["message"]["longitude"])
            level = validate_string(request.json["message"]["level"])
            pokemon_id = validate_string(request.json["message"]["pokemon_id"])
            team_id = validate_string(request.json["message"]["team_id"])
            cp = validate_string(request.json["message"]["cp"])
            start = validate_string(request.json["message"]["start"])
            end = validate_string(request.json["message"]["end"])
            name = validate_string(request.json["message"]["name"])
            evolution = validate_string(request.json["message"]["evolution"])
            spawn = validate_string(request.json["message"]["spawn"])
            move_1 = validate_string(request.json["message"]["move_1"])
            move_2 = validate_string(request.json["message"]["move_2"])
            gym_id = validate_string(request.json["message"]["gym_id"])
            url = validate_string(request.json["message"]["url"])
            is_ex_raid_eligible = validate_string(request.json["message"]["is_ex_raid_eligible"])
            is_exclusive = validate_string(request.json["message"]["is_exclusive"])
		    
		    
            insert_stmt1 = "\
                INSERT INTO raids \
                    (timestamp, \
                    latitude, \
                    longitude, \
                    level, \
		    		pokemon_id, \
                    team_id, \
                    cp, \
                    start, \
                    end, \
		    		name, \
                    evolution, \
		    		spawn, \
                    move_1, \
                    move_2, \
                    gym_id, \
                    url, \
                    is_ex_raid_eligible, \
                    is_exclusive) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) \
                ON DUPLICATE KEY UPDATE \
                    timestamp = VALUES(timestamp), \
                    latitude = VALUES(latitude), \
                    longitude = VALUES(longitude), \
                    level = VALUES(level), \
                    pokemon_id = VALUES(pokemon_id), \
                    team_id = VALUES(team_id), \
                    cp = VALUES(cp), \
                    start = VALUES(start), \
                    end = VALUES(end), \
                    name = VALUES(name), \
                    evolution = VALUES(evolution), \
                    spawn = VALUES(spawn), \
                    move_1 = VALUES(move_1), \
                    move_2 = VALUES(move_2), \
                    url = VALUES(url), \
                    is_ex_raid_eligible = VALUES(is_ex_raid_eligible), \
                    is_exclusive = VALUES(is_exclusive)"
		    
            data1 = (timestamp, latitude, longitude, int(level), int(pokemon_id), int(team_id), int(cp), start, end, str(name), int(evolution), spawn, int(move_1), int(move_2),str(gym_id), str(url), str(is_ex_raid_eligible), str(is_exclusive))
		    
            try:
                connection_object = connection_pool.get_connection()
            
                # Get connection object from a pool
                if connection_object.is_connected():
                    print("MySQL pool connection is open.")
                    # Executing the SQL command
                    cursor = connection_object.cursor()
                    cursor.execute(insert_stmt1,data1)
                    connection_object.commit()
                    print("Data inserted")
                    
            except Exception as e:
                # Rolling back in case of error
                connection_object.rollback()
                print(e)
                print("Data NOT inserted. rollbacked.")
		    
            finally:
                # closing database connection.
                if connection_object.is_connected():
                    cursor.close()
                    connection_object.close()
                    print("MySQL pool connection is closed.")

        return "Webhook received!"

# start scheduling
try:
    app.run(host=_host, port=_port)
	
except KeyboardInterrupt:
    print("Webhook receiver will be stopped")
    exit(0)
