import sqlite3
import hashlib
import re

hospital_database = 'hospital.db.sqlite'
#initialization of the database 
conn = sqlite3.connect('.\hospital.db')

c = conn.cursor()
c.execute(' PRAGMA forteign_keys=ON; ')

#printing of the welcome screen for the database user 
print "Welcome to the Hospital database.\n".upper()
print "Please enter your username and password below to start\n"


while True:
    username_input = raw_input("username: ")
    password_input = raw_input("password: ")

#hashing of the entered user inputs so that they may be compared against the database
    username = hashlib.sha224(username_input).hexdigest()
    password = hashlib.sha224(password_input).hexdigest()

#checks to see if the user inputs are within the table (and sets a flag for user type?)
    if re.match("^[A-Za-z0-9_]*$", username) and re.match("^[A-Za-z0-9_]*$", password):
        c.execute("SELECT * FROM users WHERE username=? AND password=?;", (username, password))
        id_exists = c.fetchone()
        if id_exists:
            print 'Hello "DNA" user'
            break
        else:
            print "Your username or password is not correct, try again."
    
  


conn.close()