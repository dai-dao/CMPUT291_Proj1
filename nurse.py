# Display chart of patient
from db_utility import *
import sqlite3


def init(staff_id, conn, c):

    staff_id = int(staff_id)

    def start():
        action = int(raw_input("Action 1: Create new chart\n" \
                               "Action 2: Close chart\n"
                               "Action 3: Show patients and charts\n"
                               "Log out: PRESS 4\n"
                               "Enter Action: "))

        # Find all open charts for this patients
        patient_hcno = int(raw_input("Please enter healthcare number: "))
        open_charts = c.execute("Select * from charts where hcno= %d and edate is null" % patient_hcno)
        open_charts_id = list()

        rows = open_charts.fetchall()

        if len(rows):
            print_result(rows, open_charts, "Open Charts: ")
            for row in rows:
                open_charts_id.append(int(row[0]))

        return action, patient_hcno, open_charts_id

    def act1(patient_hcno, open_charts_id):
        print "Create new chart"
        next_action = 0
        if len(open_charts_id):
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
        if len(open_charts_id) == 0: # This patient doesn't already exist
            print "This patient's information doesn't already exist"
            name = raw_input("Please enter patient name: ")
            age_group = raw_input("Please enter patient's age group: ")
            address = raw_input("Please enter patient's address: ")
            phone = raw_input("Please enter patient's phone: ")
            emg_phone = raw_input("Please enter patient's emergency phone: ")
            # Insert patient's information
            query = "insert into patients values(%s, %d, %d, %d, %d, %d)" % (patient_hcno, name, age_group, address, phone, emg_phone)
            result = c.execute(query)
            print_result(result.fetchall(), result, 'Patient Table')

        else:
            print "This patient's information already exists in database."

        query = "insert into charts values((select max(chart_id) from charts) + 1, %d, DateTime('now'), NULL)" % patient_hcno
        c.execute(query)

        print 'New chart inserted'

    def act2(open_charts_id):
        print "Close charts"
        # Close open charts
        for cid in open_charts_id:
            c.execute("update charts set edate=DateTime('now') where chart_id=%d", cid)
        print 'Open charts closed for this patient'

    def act3():
        print "Display patients and charts"
        # 3. Display all available patients
        result = c.execute("SELECT * FROM %s;" % 'patients')
        print_result(result.fetchall(), result, 'patients')

        # 4. Choose a patient and display all charts based on adate
        # Action 1: List all Charts
        patient_hcno = int(raw_input("Enter patient hcno: "))
        result = c.execute("Select * from charts where hcno = %d order by adate DESC;" % patient_hcno)
        print_result(result.fetchall(), result, 'charts')

        # Next: Select a chart
        chart_id = int(raw_input("Chart ID: "))
        symptoms = c.execute("Select * from symptoms where chart_id = %d and hcno=%d" % (chart_id, patient_hcno))
        rows = symptoms.fetchall()
        if len(rows) == 0:
            print 'There\'s no symptoms for this patient and chart'
        else:
            print_result(rows, symptoms, 'symptoms')

        diagnoses = c.execute("Select * from diagnoses where chart_id = %d and hcno=%d" % (chart_id, patient_hcno))
        rows = diagnoses.fetchall()
        if len(rows) == 0:
            print 'There\'s no diagnoses for this patient and chart'
        else:
            print_result(rows, diagnoses, 'diagnoses')

        medications = c.execute("Select * from medications where chart_id = %d and hcno=%d" % (chart_id, patient_hcno))
        rows = medications.fetchall()
        if len(rows) == 0:
            print 'There\'s no medications for this patient and chart'
        else:
            print_result(rows, medications, 'medications')

        new_symptom = raw_input("What symptom? ")
        c.execute("Insert into symptoms values ('%s', %d, %d, DateTime('now'), '%s')" % (patient_hcno, int(chart_id), int(staff_id) , new_symptom))
        # Display new result
        symptoms = c.execute("Select * from symptoms where chart_id = %d and hcno=%d" % (chart_id, patient_hcno))
        print_result(symptoms.fetchall(), symptoms, 'symptoms')

    while 1:
        while 1:
            try:
                action, patient_hcno, open_charts_id = start()
                break
            except Exception as msg:
                print msg

        if action not in [1,2,3,4]:
            print "Please enter a correct action."
            continue

        while action == 1:
            try:
                act1(patient_hcno, open_charts_id)
                break
            except Exception as msg:
                print msg

        while action == 2:
            try:
                act2(patient_hcno, open_charts_id)
                break
            except Exception as msg:
                print msg

        while action == 3:
            try:
                act3()
                break
            except Exception as msg:
                print msg

        if action == 4:
            break

    conn.commit()
    