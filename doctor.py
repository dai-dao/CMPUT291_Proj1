# Display chart of patient
from db_utility import *


def init(staff_id, conn, c):

    staff_id = int(staff_id)

    def start():
        print "Available patients"
        # 1. Display all available patients
        result = c.execute("SELECT * FROM %s;" % 'patients')
        print_result(result.fetchall(), result, 'patients')

        # 2. Choose a patient and display all charts based on adate
        # Action 1: List all Charts
        patient_hcno = int(raw_input("Enter patient hcno: "))
        result = c.execute("Select * from charts where hcno = %d order by adate DESC;" % patient_hcno)

        rows = result.fetchall()

        print "Length is: " + str(len(rows))

        if len(rows) == 0:
            print 'There\'s  no patients with this hcno. Try again!'
            return -1, None, None, None

        print_result(rows, result, 'charts')

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

        action = int(raw_input("Action 1: Add symptoms\n" +
                               "Action 2: Add diagnosis\n" +
                               "Action 3: Add medications\n" +
                               "Log out: PRESS 4\n" +
                               "Enter Action: "))

        return action, patient_hcno, chart_id

    def act1(patient_hcno, chart_id):
        print "Insert symptoms: "
        new_symptom = raw_input("What symptom? ")

        c.execute("Insert into symptoms values ('%s', %d, %d, DateTime('now'), '%s')" % (patient_hcno, chart_id, staff_id , new_symptom))

        # Display new result
        symptoms = c.execute("Select * from symptoms where chart_id = %d and hcno=%d" % (chart_id, patient_hcno))
        print_result(symptoms.fetchall(), symptoms, 'symptoms')

    def act2(patient_hcno, chart_id):
        print "Insert diagnosis: "
        new_diagnosis = raw_input("What diagnosis? ")

        c.execute("Insert into diagnoses values ('%s', %d, %d, DateTime('now'), '%s')" % (patient_hcno, chart_id, staff_id , new_diagnosis))

        # Display new result
        diagnoses = c.execute("Select * from diagnoses where chart_id = %d and hcno=%d" % (chart_id, patient_hcno))
        print_result(diagnoses.fetchall(), diagnoses, 'diagnoses')

    def act3(patient_hcno, chart_id):
        print "Insert medication: "
        new_medication = raw_input("What medication? ")
        new_medication_amount = int(raw_input("What's the amount? "))
        new_sdate = raw_input("Start Date (YYYY-MM-DD HH:MM:SS): ")
        new_edate = raw_input("End Date (YYYY-MM-DD HH:MM:SS): ")

        drug_sug_amount = c.execute("select sug_amount from dosage where age_group in " +
                                        "(select age_group from patients where hcno = %d)" % patient_hcno +
                                    " and drug_name = '%s'" % new_medication)

        rows = drug_sug_amount.fetchall()

        if (len(rows)):
            sug_amount = rows[0][0]
        else:
            print "Drug is not in database"
            return

        confirm_add = False
        if sug_amount >= new_medication_amount:
            print "Suggested amount is greater than newly prescribed amount.\n"
            confirm_add = True
        else:
            print "Suggest amount is: %d\n" % sug_amount
            confirm = raw_input("WARNING: Newly Prescribed amount is greater than suggested amount. Want to proceed? (y/n): ")
            if (confirm == 'y'):
                confirm_add = True

        allergic_med = c.execute("select drug_name, ia.canbe_alg " +
                                 "from reportedallergies al, inferredallergies ia " +
                                 "where al.drug_name = ia.alg and hcno = %d" % patient_hcno)

        rows = allergic_med.fetchall()

        if (len(rows)):
            allergic1 = rows[0][0]
            allergic2 = rows[0][1]
            if allergic1 == new_medication:
                print 'WARNING: Patient is allergic to this drug directly: %s\n' % allergic1
            if allergic2 == new_medication:
                print 'WARNING: Patient is inferred to be allergic to this drug: %s\n' % allergic2
        else:
            print "There's no record of allergy to this drug.\n"

        if confirm_add:
            try:
                c.execute("Insert into medications values " +
                      "(%d, %d, %d, DateTime('now'), '%s' , '%s', %d, '%s')" % (patient_hcno, chart_id, staff_id, new_sdate, new_edate, new_medication_amount, new_medication))
                medications = c.execute("Select * from medications where chart_id = %d and hcno = %d" % (chart_id, patient_hcno))
                print_result(medications.fetchall(), medications, 'medications')
            except OperationalError as msg:
                print msg
                return -1

        return 1

    while 1:
        while 1:
            try:
                action, patient_hcno, chart_id = start()
                break
            except Exception as msg:
                print msg

        if action not in [1,2,3,4]:
            print "Please enter a correct action."
            continue

        while action == 1:
            try:
                act1(patient_hcno, chart_id)
                break
            except Exception as msg:
                print msg

        while action == 2:
            try:
                act2(patient_hcno, chart_id)
                break
            except Exception as msg:
                print msg

        while action == 3:
            try:
                act3(patient_hcno, chart_id)
                break
            except Exception as msg:
                print msg

        if action == 4:
            break

    conn.commit()
