# Display chart of patient
from db_utility import *
import sqlite3


def init(staff_id, conn, c):

    # 1.
    action = int(raw_input("Action 1: Create new chart\n" \
                           "Action 2: Close chart\n"
                           "Pick one: "))

    # Find all open charts for this patients
    patient_hcno = int(raw_input("Please enter healthcare number: "))
    open_charts = c.execute("Select * from charts where hcno= %d and edate is null" % patient_hcno)
    
    open_charts_id = list()
    
    patient_exists = 0
    
    if len(open_charts.fetchall()):
        patient_exists = 1
        print_result(open_charts, "Open Charts: ")
        open_charts = open_charts.fetchall()        
        for row in open_charts:
            open_charts_id.append(int(row[0]))
        print open_charts_id
        
    
    if action == 1:
        next_action = 0
        if len(open_charts):
            next_action = int(raw_input("This patient has open charts.\n" \
                              "Action 1: Close chart and Create New one\n" \
                              "Action 2: Don't create new one\n" \
                              "Pick one: "))

        if next_action == 1:
            # Close open charts
            for cid in open_charts_id:
                c.execute("update charts set edate=DateTime('now') where chart_id=%d" % cid)

        if next_action == 2:
            pass

        # Create new charts
        if next_action != 2:
            patient_hcno = 0
            if next_action != 1 and not patient_exists: # This patient doesn't already exist
                print "This patient's information doesn't already exist"
                name = raw_input("Please enter patient name: ")
                age_group = raw_input("Please enter patient's age group: ")
                address = raw_input("Please enter patient's address: ")
                phone = raw_input("Please enter patient's phone: ")
                emg_phone = raw_input("Please enter patient's emergency phone: ")
                # Insert patient's information
                c.execute("insert into patients values(%s, %d, %d, %d, %d, %d)" % (patient_hcno, name, age_group, address, phone, emg_phone))

            else:
                print "This patient's information already exists in database."

            c.execute("insert into charts values((select max(chart_id) from charts) + 1, %d, DateTime('now'), NULL)" % patient_hcno)

    if action == 2:
        # Close open charts
        for cid in open_charts_id:
            c.execute("update charts set edate=DateTime('now') where chart_id=%d", cid)


    # 3. Display all available patients
    result = c.execute("SELECT * FROM %s;" % 'patients')
    print_result(result, 'patients')

    # 4. Choose a patient and display all charts based on adate
    # Action 1: List all Charts
    patient_hcno = int(raw_input("Enter patient hcno: "))
    result = c.execute("Select * from charts where hcno = %d order by adate DESC;" % patient_hcno)
    print_result(result, 'charts')
   
   
    # Next: Select a chart
    chart_id = int(raw_input("Chart ID: "))
    symptoms = c.execute("Select * from symptoms where chart_id = %d and hcno=%d" % (chart_id, patient_hcno))
    
    diagnoses = c.execute("Select * from diagnoses where chart_id = %d and hcno=%d" % (chart_id, patient_hcno))
    medications = c.execute("Select * from medications where chart_id = %d and hcno=%d" % (chart_id, patient_hcno))    
    print_result(diagnoses, 'diagnoses')
    print_result(medications, 'medications')
    print_result(symptoms, 'symptoms')
   
    new_symptom = raw_input("What symptom? ")
    c.execute("Insert into symptoms values ('%s', %d, %d, DateTime('now'), '%s')" % (patient_hcno, int(chart_id), int(staff_id) , new_symptom))
   
           # Display new result
    symptoms = c.execute("Select * from symptoms where chart_id = %d and hcno=%d" % (chart_id, patient_hcno))
    
    
    print_result(symptoms, 'symptoms')
    


    
    conn.commit()
    