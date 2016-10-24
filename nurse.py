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
    open_charts = open_charts.fetchall()
    open_charts_id = list()

    if len(open_charts):
        for row in open_charts:
            open_charts_id.append(int(row[0]))

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
            if next_action != 1: # This patient doesn't already exist
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



    '''
    conn.commit()
    '''