from db_utility import *

def init(conn, c):

    action = int(raw_input("Action 1: Create report\n"
                       "Action 2: Total amount prescribed for each drug\n"
                       "Action 3: List all medications for diagnosis\n"
                       "Action 4: List all diagnoses for drug:"))

    if action == 1:
        sdate = raw_input("Enter Start Date (YYYY-MM-DD HH:MM:SS): ")
        edate = raw_input("Enter End Date (YYYY-MM-DD HH:MM:SS): ")


        query = "SELECT staff_id,  drug_name,  sum(amount) * " \
                "           round(julianday(min(end_med ,'%s')) - julianday(max(start_med, '%s'))) " % (edate, sdate) + \
                "    AS Total " + \
                "FROM medications " + \
                "GROUP BY staff_id, drug_name"

        result = c.execute(query)
        print_result(result, 'Report')

    if action == 2:
        sdate = raw_input("Enter Start Date (YYYY-MM-DD HH:MM:SS): ")
        edate = raw_input("Enter End Date (YYYY-MM-DD HH:MM:SS): ")

        # Needs some more checking, there are negative values involved
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

    if action == 3:
        diagnosis = raw_input("Enter the diagnosis: ")
        query = "select diag.diagnosis, med.drug_name, count(med.drug_name) as drug_frequency " + \
                "from " + \
                "diagnoses diag, medications med where diag.chart_id = med.chart_id " + \
                "and diag.diagnosis = '%s'" % diagnosis + \
                "group by drug_name " + \
                "order by diagnosis, drug_frequency "

        result = c.execute(query)
        print_result(result, 'List all medications for diagnosis')

    if action == 4:
        drug = raw_input("Enter the Drug Name: " )
        query = "select med.drug_name, diag.diagnosis, avg(med.amount) as average_amount " + \
                "from medications med, diagnoses diag where med.chart_id = diag.chart_id " + \
                "and med.drug_name = %s" % drug + \
                "group by diagnosis " + \
                "order by drug_name, average_amount"
        result = c.execute(query)
        print_result(result, 'List all diagnosis for medication')




