
# Display chart of patient
from db_utility import *


def init(staff_id, conn, c):
    def start():
        # 1. Display all available patients
        try:
            result = c.execute("SELECT * FROM %s;" % 'patients')
            print_result(result, 'patients')
            
            # 2. Choose a patient and display all charts based on adate
            # Action 1: List all Charts
            patient_hcno = int(raw_input("Enter patient hcno: "))
            result = c.execute("Select * from charts where hcno = %d order by adate DESC;" % patient_hcno)
            
            check = c.execute("Select distinct(hcno) from charts;").fetchall()
            
            i = 0
            check_list = []
            while i < len(check):
                
                check_list.append(int(check[i][0]))
                i = i+1
                
            
            while (True):
                if patient_hcno not in check_list:
                    print "User not in patient list or has no chart.\n"
                    patient_hcno = int(raw_input("Enter patient hcno: "))
                    result = c.execute("Select * from charts where hcno = %d order by adate DESC;" % patient_hcno)
                else:
                    break
                
            result = c.execute("Select * from charts where hcno = %d order by adate DESC;" % patient_hcno)
                     
            print_result(result, 'charts')
                       

            # Next: Select a chart
            chart_id = int(raw_input("Chart ID: "))
            symptoms = c.execute("Select * from symptoms where chart_id = %d and hcno=%d" % (chart_id, patient_hcno))
            diagnoses = c.execute("Select * from diagnoses where chart_id = %d and hcno=%d" % (chart_id, patient_hcno))
            medications = c.execute("Select * from medications where chart_id = %d and hcno=%d" % (chart_id, patient_hcno))
        except OperationalError as msg:
            print msg
            return -1, None, None, None

        print_result(symptoms, 'symptoms')
        print_result(diagnoses, 'diagnoses')
        print_result(medications, 'medications')

        action = raw_input("Action 1: Add symptoms\n" +
                           "Action 2: Add diagnosis\n" +
                           "Action 3: Add medications\n"
                           "Log out: PRESS 4\n" +
                           "Enter Action: ")

        return 1, action, patient_hcno, chart_id

    def act1(patient_hcno, chart_id):
        new_symptom = raw_input("What symptom? ")

        try:
            c.execute("Insert into symptoms values ('%s', %d, %d, DateTime('now'), '%s')" % (patient_hcno, chart_id, staff_id , new_symptom))

            # Display new result
            symptoms = c.execute("Select * from symptoms where chart_id = %d and hcno=%d" % (chart_id, patient_hcno))
            print_result(symptoms, 'symptoms')
        except OperationalError as msg:
            print msg
            return -1
        return 1

    def act2(patient_hcno, chart_id):
        new_diagnosis = raw_input("What diagnosis? ")

        try:
            c.execute("Insert into diagnoses values ('%s', %d, %d, DateTime('now'), '%s')" % (patient_hcno, chart_id, staff_id , new_diagnosis))

            # Display new result
            diagnoses = c.execute("Select * from diagnoses where chart_id = %d and hcno=%d" % (chart_id, patient_hcno))
            print_result(diagnoses, 'diagnoses')
        except OperationalError as msg:
            print msg
            return -1

        return 1

    def act3(patient_hcno, chart_id):
        new_medication = raw_input("What medication? ")
        new_medication_amount = int(raw_input("What's the amount? "))
        new_sdate = raw_input("Start Date (YYYY-MM-DD HH:MM:SS): ")
        new_edate = raw_input("End Date (YYYY-MM-DD HH:MM:SS): ")
        try :
            drug_sug_amount = c.execute("select sug_amount from dosage where age_group in " +
                                        "(select age_group from patients where hcno = %d)" % patient_hcno +
                                    " and drug_name = '%s'" % new_medication)
        except OperationalError as msg:
            print msg
            return -1

        drug_sug_amount = drug_sug_amount.fetchall()

        if (len(drug_sug_amount)):
            sug_amount = drug_sug_amount[0][0]
        else:
            print "Drug is not in database"
            return 1

        confirm_add = False
        if sug_amount >= new_medication_amount:
            print "Suggested amount is greater than newly prescribed amount.\n"
            confirm_add = True
        else:
            print "Suggest amount is: %d\n" % sug_amount
            confirm = raw_input("WARNING: Newly Prescribed amount is greater than suggested amount. Want to proceed? (y/n): ")
            if (confirm == 'y'):
                confirm_add = True

        try:
            allergic_med = c.execute("select drug_name, ia.canbe_alg " +
                                 "from reportedallergies al, inferredallergies ia " +
                                 "where al.drug_name = ia.alg and hcno = %d" % patient_hcno)
        except OperationalError as msg:
            print msg
            return -1

        allergic_med = allergic_med.fetchall()

        if (len(allergic_med)):
            allergic1 = allergic_med[0][0]
            allergic2 = allergic_med[0][1]
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
                print_result(medications, 'medications')
            except OperationalError as msg:
                print msg
                return -1

        return 1

    while 1:
        while 1:
            result, action, patient_hcno, chart_id = start()
            if result: break

        while action == 1:
            result = act1(patient_hcno, chart_id)
            if result: break

        while action == 2:
            result = act2(patient_hcno, chart_id)
            if result: break

        while action == 3:
            result = act3(patient_hcno, chart_id)
            if result: break

        if action == 4:
            break

        if action not in [1,2,3,4]:
            print "Please enter a correct action."

    conn.commit()
