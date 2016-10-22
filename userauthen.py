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




#loops if user enters username or password that is not in the database
while True:
    
    username_input = raw_input("username: ")
    password_input = raw_input("password: ")

#hashing of the entered user inputs so that they may be compared against the database
    username = hashlib.sha224(username_input).hexdigest()
    password = hashlib.sha224(password_input).hexdigest()
    


#CURRENT USERNAMES & PASSWORDS:
# Doctor: username
#         password
#
# Nurse:  password
#         username
#
# admin:  admin
#         admin
    
    #checks to see if the user inputs are within the table
    if re.match("^[A-Za-z0-9_]*$", username) and re.match("^[A-Za-z0-9_]*$", password):
        c.execute("SELECT id FROM users WHERE username=? AND password=?;", (username, password))
        
        user_exists = c.fetchone()
        if user_exists:
            if user_exists[0] == 'A':
                print '\nHello Administrator'
                break
            if user_exists[0] == 'D':
                print '\nHello Doctor'
                break            
            if user_exists[0] == 'N':
                print '\nHello Nurse'
                break            
        else:
            print "\nYour username or password is not correct, try again.\n"
    
  


conn.close()