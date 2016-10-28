# Display chart of patient
from db_utility import *


def init(staff_id, conn, c):

    staff_id = int(staff_id)

    def start():
        first_action = int(raw_input("\n" \
                                     "Log Out: PRESS 1" \
                                     "Action 2: Show Patients and Perform Actions\n"
                                     "Enter action: "))
        return first_action

    def start_next():
        print "Available patients"
        # 1. Display all available patients
        result = c.execute("SELECT * FROM %s;" % 'patients')
        rows = result.fetchall()
        print_result(rows, result, 'patients')

        patient_hcnos = list()
        for row in rows:
            patient_hcnos.append(int(row[0]))

        # 2. Choose a patient and display all charts based on adate
        while 1:
            patient_hcno = int(raw_input("Enter patient hcno: "))
            if patient_hcno not in patient_hcnos:
                print 'This patient is not in database. Please try again!'
            else:
                break

        # Action 1: List all Charts
        result = c.execute("Select * from charts where hcno = %d order by adate DESC;" % patient_hcno)
        rows = result.fetchall()
        print_result(rows, result, 'charts')

        chart_ids = list()
        for row in rows:
            chart_ids.append(int(row[0]))

        # Next: Select a chart
        while 1:
            chart_id = int(raw_input("Chart ID: "))
            if chart_id not in chart_ids:
                print 'This chart is not for this patient. Try again!'
            else:
                break

        symptoms = c.execute("Select * from symptoms where chart_id = %d and hcno=%d" % (chart_id, patient_hcno))
        rows = symptoms.fetchall()

        diagnoses = c.execute("Select * from diagnoses where chart_id = %d and hcno=%d" % (chart_id, patient_hcno))
        rows = diagnoses.fetchall()

        medications = c.execute("Select * from medications where chart_id = %d and hcno=%d" % (chart_id, patient_hcno))
        rows = medications.fetchall()

        action = int(raw_input("Action 1: Add symptoms\n" +
                               "Action 2: Add diagnosis\n" +
                               "Action 3: Add medications\n" +
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

        while 1:
            new_medication = raw_input("What medication? ")

            drug_sug_amount = c.execute("select sug_amount from dosage where age_group in " +
                                            "(select age_group from patients where hcno = %d)" % patient_hcno +
                                        " and drug_name = '%s'" % new_medication)

            rows = drug_sug_amount.fetchall()

            if (len(rows)):
                sug_amount = rows[0][0]
                break
            else:
                print "Drug is not in database"

        new_medication_amount = int(raw_input("What's the amount? "))
        new_sdate = raw_input("Start Date (YYYY-MM-DD HH:MM:SS): ")
        new_edate = raw_input("End Date (YYYY-MM-DD HH:MM:SS): ")

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
            c.execute("Insert into medications values " +
                  "(%d, %d, %d, DateTime('now'), '%s' , '%s', %d, '%s')" % (patient_hcno, chart_id, staff_id, new_sdate, new_edate, new_medication_amount, new_medication))
            medications = c.execute("Select * from medications where chart_id = %d and hcno = %d" % (chart_id, patient_hcno))
            print_result(medications.fetchall(), medications, 'medications')


    while 1:
        while 1:
            try:
                first_action = start()
                break
            except Exception as msg:
                print msg

        if first_action not in [1, 2]:
            print "Please enter a correct action."
            continue

        if first_action == 1:
            break

        if first_action == 2:
            action, patient_hcno, chart_id = start_next()

            if action not in [1,2,3]:
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

    conn.commit()
