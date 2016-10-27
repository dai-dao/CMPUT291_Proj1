# Display chart of patient
from db_utility import *
import sqlite3


def init(staff_id, conn, c):

    def start():
        action = int(raw_input("Action 1: Create new chart\n" \
                               "Action 2: Close chart\n"
                               "Action 3: Show patients and charts\n"
                               "Log out: PRESS 4"
                               "Enter Action: "))

        # Find all open charts for this patients
        patient_hcno = int(raw_input("Please enter healthcare number: "))
        open_charts = c.execute("Select * from charts where hcno= %d and edate is null" % patient_hcno)
        open_charts_id = list()

        if len(open_charts.fetchall()):
            print_result(open_charts, "Open Charts: ")
            for row in open_charts.fetchall():
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
            try:
                result = c.execute(query)
                print_result(result, 'Patient Table')

            except OperationalError as msg:
                print msg
                return

        else:
            print "This patient's information already exists in database."

        query = "insert into charts values((select max(chart_id) from charts) + 1, %d, DateTime('now'), NULL)" % patient_hcno
        try:
            c.execute(query)
        except OperationalError as msg:
            print msg
            return

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
        try:
            result = c.execute("SELECT * FROM %s;" % 'patients')
            print_result(result, 'patients')
        except OperationalError as msg:
            print msg
            return

        # 4. Choose a patient and display all charts based on adate
        # Action 1: List all Charts
        patient_hcno = int(raw_input("Enter patient hcno: "))
        try:
            result = c.execute("Select * from charts where hcno = %d order by adate DESC;" % patient_hcno)
            print_result(result, 'charts')
        except OperationalError as msg:
            print msg
            return

        # Next: Select a chart
        chart_id = int(raw_input("Chart ID: "))
        try:
            symptoms = c.execute("Select * from symptoms where chart_id = %d and hcno=%d" % (chart_id, patient_hcno))
            diagnoses = c.execute("Select * from diagnoses where chart_id = %d and hcno=%d" % (chart_id, patient_hcno))
            medications = c.execute("Select * from medications where chart_id = %d and hcno=%d" % (chart_id, patient_hcno))
        except OperationalError as msg:
            print msg
            return

        print_result(diagnoses, 'diagnoses')
        print_result(medications, 'medications')
        print_result(symptoms, 'symptoms')

        new_symptom = raw_input("What symptom? ")
        try:
            c.execute("Insert into symptoms values ('%s', %d, %d, DateTime('now'), '%s')" % (patient_hcno, int(chart_id), int(staff_id) , new_symptom))
            # Display new result
            symptoms = c.execute("Select * from symptoms where chart_id = %d and hcno=%d" % (chart_id, patient_hcno))
            print_result(symptoms, 'symptoms')
        except OperationalError as msg:
            print msg
            return

    while 1:
        action, patient_hcno, open_charts_id = start()

        while action == 1:
            result = act1(patient_hcno, open_charts_id)
            if result: break

        while action == 2:
            result = act2(patient_hcno, open_charts_id)
            if result: break

        while action == 3:
            result = act3()
            if result: break

        if action == 4:
            break

        if action not in [1,2,3,4]:
            print "Please enter a correct action."

    conn.commit()
    