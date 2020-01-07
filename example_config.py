#Rename this file to config.py and place in project root
import os

class Config(object):
    MYSQL_USER = 'example_user';
    MYSQL_PASSWORD = 'my_pass';
    MYSQL_DB = 'my_db';
    MYSQL_HOST = 'localhost';
    MYSQL_PORT = 3306;
    SECRET_KEY = os.urandom(32)
    ADMIN_USERS = ['my_admin_user']
