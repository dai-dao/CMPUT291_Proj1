import sqlite3
import hashlib
import re
import doctor 
from db_utility import *


#a funtion to handle the Doctor roles in the database
def doctorUser(staff_id, conn, c):
    doctor.init(staff_id, conn, c)
    i = 2
    return i


#a function to handle the Nurse roles in the database
def nurseUser():
    i = 1
    return i


#a function to handle the Admin roles in the database
def adminUser():
    i = 0
    return i



#initialization of the database 

hospital_database = 'hospital.db.sqlite'

conn = sqlite3.connect('.\hospital.db')

c = conn.cursor()
c.execute(' PRAGMA forteign_keys=ON; ')
executeScript('table.sql', c)
executeScript('a3_data.sql', c)


#printing of the welcome screen for the database user 
print "============================================================\n"
print "************* Welcome to the Hospital database *************\n".upper()
print "Please enter your username and password below to start"
print "or type 'exit' in both fields to exit.\n"

#CURRENT USERNAMES & PASSWORDS:
# Doctor: adoc, coda
#         bdoc, codb
#         
#
# Nurse:  anur, runa
#         bnur, runb
#
# admin:  aadm, mdaa
#         badm, mdab



#loops if user enters username or password that is not in the database
#exits if user enters 'exit' in both fields
while True:
    
    username_input = raw_input("username: ")
    password_input = raw_input("password: ")

#hashing of the entered user inputs so that they may be compared against the database
    username = hashlib.sha224(username_input).hexdigest()
    password = hashlib.sha224(password_input).hexdigest()
    print username
    print password
    
    
    
#Breaks the loop to exit the database
    if username == '95d0df0e937ba7c068e398dee3ce00904558864a701013b1d9682d5d' and password =='95d0df0e937ba7c068e398dee3ce00904558864a701013b1d9682d5d':
        print 'Now exiting the Hospital database...'
        break
    
#checks to see if the user inputs are within the table and protects
#against SQL injection
    
    if re.match("^[A-Za-z0-9_]*$", username) and re.match("^[A-Za-z0-9_]*$", password):
        c.execute("SELECT role, staff_id FROM staff WHERE login=? AND password=?;", (username, password))
        
        user_exists = c.fetchone()
        if user_exists:
            if user_exists[0] == 'A':
                print '\nHello Administrator'
                adminUser()
                break
            if user_exists[0] == 'D':
                print '\nHello Doctor'
                doctorUser(user_exists[1], conn, c) 
                break
            if user_exists[0] == 'N':
                print '\nHello Nurse'
                print user_exists[0]
                nurseUser()
                break
        else:
            print "\nYour username or password is not correct, try again.\n"
    
  


conn.close()