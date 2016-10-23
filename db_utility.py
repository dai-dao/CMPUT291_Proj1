import sqlite3
from sqlite3 import OperationalError


def executeScript(script, c):
    fd = open(script, 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # Execute every command from the input file
    for command in sqlCommands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        try:
            c.execute(command)
        except OperationalError, msg:
            print "Command skipped: ", msg


def print_result(result, table):
    # Get all rows.
    rows = result.fetchall();

    # \n represents an end-of-line
    print "\n--- TABLE ", table, "\n"

    # This will print the name of the columns, padding each name up
    # to 22 characters. Note that comma at the end prevents new lines
    for desc in result.description:
        print desc[0].rjust(22, ' '),

    # End the line with column names
    print ""
    for row in rows:
        for value in row:
            # Print each value, padding it up with ' ' to 22 characters on the right
            print str(value).rjust(22, ' '),
        # End the values from the row
        print ""
