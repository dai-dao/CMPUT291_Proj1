from db_utility import *
import hashlib
from datecheck import valid_date

def init(conn, c):

    def act1():
        print "Creating report: "
        sdate = raw_input("Enter Start Date (YYYY-MM-DD HH:MM:SS): ")
        edate = raw_input("Enter End Date (YYYY-MM-DD HH:MM:SS): ")
        
            
        query = "select staff_id, drug_name, sum(amount) * days_between from " \
                "( " \
                "select * , round(julianday(min(end_med ,'%s')) - julianday(max(start_med, '%s'))) " % (edate, sdate) + \
                "as days_between " \
                "from medications) " \
                "where days_between > 0 and days_between is not null "\
                "group by staff_id, drug_name"                
                

        result = c.execute(query)
        print_result(result.fetchall(), result, 'Report')

    def act2():
        print "Get Total amount prescribed for each drug"
        sdate = raw_input("Enter Start Date (YYYY-MM-DD HH:MM:SS): ")
        edate = raw_input("Enter End Date (YYYY-MM-DD HH:MM:SS): ")
        query = "select first_sub.category, second_sub.drug_name, second_sub.total_category, first_sub.type_total " + \
            "from " + \
            "    (select dr.category, sum(sub.Total) as type_total " + \
            "    from drugs dr " + \
            "    inner join " + \
            "        (SELECT drug_name, sum(amount) * " + \
            "           round(julianday(min(end_med ,'%s')) - julianday(max(start_med, '%s'))) " % (edate, sdate) + \
            "        AS Total " + \
            "        FROM medications " + \
            "        GROUP BY drug_name) " + \
            "    sub " + \
            "    on " + \
            "    dr.drug_name = sub.drug_name " + \
            "    group by dr.category) " + \
            "first_sub " + \
            "inner join " + \
            "    (select " + \
            "    dr.category, dr.drug_name, sub.Total as total_category " + \
            "    from " + \
            "    drugs dr " + \
            "    inner join " + \
            "    (SELECT " + \
            "    drug_name, sum(amount) * " \
            "                round(julianday(min(end_med ,'%s')) - julianday(max(start_med, '%s'))) " % (edate, sdate) + \
            "        AS Total " + \
            "    FROM " + \
            "    medications " + \
            "    GROUP BY " + \
            "    drug_name) sub " + \
            "    on " + \
            "    dr.drug_name = sub.drug_name " + \
            "    order by " + \
            "    dr.category) " + \
            "second_sub " + \
            "on " + \
            "first_sub.category = second_sub.category " + \
            "where total_category > 0 and type_total > 0 " + \
            "order by first_sub.category "

        result = c.execute(query)
        print_result(result.fetchall(), result, 'Total Amount Prescribed for each Drug')

    def act3():
        print "List all medications for diagnosis: "
        diagnosis = raw_input("Enter the diagnosis: ")
        query = "select diag.diagnosis, med.drug_name, count(med.drug_name) as drug_frequency " + \
                "from " + \
                "diagnoses diag, medications med where diag.chart_id = med.chart_id " + \
                "and diag.diagnosis = '%s'" % diagnosis + \
                "group by drug_name " + \
                "order by diagnosis, drug_frequency "

        result = c.execute(query)
        print_result(result.fetchall(), result, 'List all medications for diagnosis')

    def act4():
        print 'List all diagnoses for drug: '
        drug = raw_input("Enter the Drug Name: " )
        query = "select med.drug_name, diag.diagnosis, avg(med.amount) as average_amount " + \
                "from medications med, diagnoses diag where med.chart_id = diag.chart_id " + \
                "and med.drug_name = '%s'" % drug + \
                "group by diagnosis " + \
                "order by drug_name, average_amount"

        result = c.execute(query)
        print_result(result.fetchall(), result, 'All diagnoses: ')

        

    def act5():
        print "You chose to add a new user to the database."
        while True:
            nrole = raw_input("Enter role of new user: ").upper()
            if nrole not in ("D", "N", "A"):
                print "Role must be D, N, or A. Try again"
                continue
            break

        nname = raw_input("Enter name of new user: ")
        nlogin = raw_input("Enter the username of new user: ")
        nlogin = hashlib.sha224(nlogin)
        npassword = raw_input("Enter password of new user: ")
        npassword = hashlib.sha224(npassword)

        insertion = (nrole, str(nname), str(nlogin), str(npassword))

        c.execute("INSERT INTO staff VALUES ((select max(staff_id) from staff) + 1,?,?,?, ?)", insertion)
        sid = int(c.execute("select max(staff_id) from staff").fetchall()[0][0])
        print 'New user created successfully. Your staff_id is: ' + str(sid)

    while 1:
        action = raw_input("\nAction 1: Create report\n"
                           "Action 2: Total amount prescribed for each drug\n"
                           "Action 3: List all medications for diagnosis\n"
                           "Action 4: List all diagnoses for drug\n"
                           "Action 5: Add new user to database\n"
                           "Log out: PRESS 6\n"
                           "Enter action: ")

        action = int(action)

        if action not in [1, 2, 3, 4, 5, 6]:
            print "Please enter a correct action."
            continue


        while action == 1:
            try:
                act1()
                break
            except Exception as msg:
                print msg

        while action == 2:
            try:
                act2()
                break
            except Exception as msg:
                print msg

        while action == 3:
            try:
                act3()
                break
            except Exception as msg:
                print msg

        while action == 4:
            try:
                act4()
                break
            except Exception as msg:
                print msg

        while action == 5:
            try:
                act5()
                break
            except Exception as msg:
                print msg

        if action == 6:
            break

    conn.commit()
