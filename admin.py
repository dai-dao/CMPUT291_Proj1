from db_utility import *
import hashlib

def init(conn, c):

    def act1():
        print "Creating report: "
        sdate = raw_input("Enter Start Date (YYYY-MM-DD HH:MM:SS): ")
        edate = raw_input("Enter End Date (YYYY-MM-DD HH:MM:SS): ")


        query = "SELECT staff_id,  drug_name,  sum(amount) * " \
                "           round(julianday(min(end_med ,'%s')) - julianday(max(start_med, '%s'))) " % (edate, sdate) + \
                "    AS Total " + \
                "FROM medications " + \
                "GROUP BY staff_id, drug_name"

        try:
            result = c.execute(query)
            print_result(result.fetchall(), result, 'Report')
        except OperationalError as msg:
            print msg
            return -1
        return 1

    def act2():
        print "Get Total amount prescribed for each drug"
        sdate = raw_input("Enter Start Date (YYYY-MM-DD HH:MM:SS): ")
        edate = raw_input("Enter End Date (YYYY-MM-DD HH:MM:SS): ")
        try:
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
            print_result(result, 'Total Amount Prescribed for each Drug')

        except OperationalError as msg:
            print msg
            return -1
        return 1

    def act3():
        print "List all medications for diagnosis: "
        diagnosis = raw_input("Enter the diagnosis: ")
        query = "select diag.diagnosis, med.drug_name, count(med.drug_name) as drug_frequency " + \
                "from " + \
                "diagnoses diag, medications med where diag.chart_id = med.chart_id " + \
                "and diag.diagnosis = '%s'" % diagnosis + \
                "group by drug_name " + \
                "order by diagnosis, drug_frequency "

        try:
            result = c.execute(query)
            print_result(result.fetchall(), result, 'List all medications for diagnosis')
        except OperationalError as msg:
            print msg
            return -1
        return 1

    def act4():
        print 'List all diagnoses for drug: '
        drug = raw_input("Enter the Drug Name: " )
        query = "select med.drug_name, diag.diagnosis, avg(med.amount) as average_amount " + \
                "from medications med, diagnoses diag where med.chart_id = diag.chart_id " + \
                "and med.drug_name = %s" % drug + \
                "group by diagnosis " + \
                "order by drug_name, average_amount"

        try:
           result = c.execute(query)
        except OperationalError as msg:
            print msg
            return -1
        return 1

        print_result(result, 'List all diagnosis for medication')

    def act5():
        while True:
            print "You chose to add a new user to the database."
            sid = raw_input("Enter staff_id of new user: ")
            while True:
                nrole = raw_input("Enter role of new user: ").upper()
                if nrole not in ("D", "N", "A"):
                    print "Role must be D, N, or A. Try again"
                    continue
                break

            while True:

                nname = raw_input("Enter name of new user: ")

                nlogin = raw_input("Enter the username of new user: ")
                h = hashlib.sha224()
                h.update(nlogin)
                nlogin = h.hexdigest()
                nlogin = str(nlogin)

                query = "SELECT s.login FROM staff s"
                c.execute(query)
                rows = c.fetchall()

                flag = True
                for each in rows:
                    if each[0] == nlogin:
                        flag = False

                if flag == False:
                    print "Username already exists in table. Enter another one."
                    continue

                break

            npassword = raw_input("Enter password of new user: ")
            h2 = hashlib.sha224()
            h2.update(npassword)
            npassword = h2.hexdigest()
            npassword = str(npassword)

            insertion = (sid, nrole, nname, nlogin, npassword)


            try:
                c.execute("INSERT INTO staff VALUES (?,?,?,?,?)", insertion)
            except sqlite3.IntegrityError:
                print "Staff ID already exists in table. Try again"
                continue

            break

        return 1

    while 1:
        action = int(raw_input("\nAction 1: Create report\n"
                               "Action 2: Total amount prescribed for each drug\n"
                               "Action 3: List all medications for diagnosis\n"
                               "Action 4: List all diagnoses for drug\n"
                               "Action 5: Add new user to database\n"
                               "Log out: PRESS 6\n"
                               "Enter action: "))

        while action == 1:
            result = act1()
            if result: break

        while action == 2:
            result = act2()
            if result: break

        while action == 3:
            result = act3()
            if result: break

        while action == 4:
            result = act4()
            if result: break

        while action == 5:
            result = act5()
            if result: break

        if action == 6:
            break

        if action not in [1,2,3,4,5,6]:
            print "Please enter a correct action."

    conn.commit()
