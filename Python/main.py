import psycopg2
import pygame
import sys



# ------------------ CONNECTING TO DATABASE, GETTING DATA -----------------
from psycopg2 import sql


def connect_postgres(name, user, password):
    print("Attempting to connect to the database...")
    n = name
    u = user
    if(u == ""):
        u = "postgres"
    p = password
    c = None
    try:
        c = psycopg2.connect(
            dbname=n,
            user=u,
            host='localhost', # assumes local host for now
            password=p
        )
        print("Successful Connection.")
    except Exception as err:
        print("I am unable to connect to the database")
        c = None
        exit()
    return c

databaseName = input("enter the database name: ")
databaseUser = input("enter your database username: (blank for default)")
databasePassword = input("enter your database password: ")
conn = connect_postgres(databaseName, databaseUser, databasePassword)


# create a new cursor using database connection
cur = conn.cursor()
# execute an sql query on the database
cur.execute("""SELECT * FROM senator""")
# set the query result into a list
senators = cur.fetchall()
# get all state info
cur.execute("""SELECT * FROM state""")
# set the query result into a list
states = cur.fetchall()


# use sql.SQL() to prevent SQL injection attack
#sql_object = sql.SQL(
#    # pass SQL statement to sql.SQL() method
#    "SELECT * FROM {} LIMIT 20;"
#).format(
#    # pass the identifier to the Identifier() method
#    sql.Identifier( table_name )
#)


# EXAMPLE OF NAMING COLUMNS
# for stateId, stateName, stateDate, stateCapital in states:
#    print(stateName) #print the current state row
#

# -------------------- FUNCTION DEFINITIONS ----------------------------------
def get_all_senators_of_party(partyName):
    senatorList = []
    for senator in senators:
        # check if party (last column) is same as partyName
        if(senator[-1] == partyName):
            senatorList.append(senator)
    return senatorList

def print_all_senators():
    print("Printing all senators:")
    for senator in senators:
        print("   " + str(senator))  # print the senator row

def print_all_states():
    print("Printing all states:")
    for state in states:
        print("   " + str(state))  # print the states row




# ----------------INPUT CONSOLE -------------------------------------
r = ""
#while user has not quit, get input
while r != "quit":
    response = input("Enter a command (type help for command list)")
    r = response.split(" ")[0] #get first one in response
    if r == "help":
        print("")
        print("pstates: print all states")
        print("psenators: print all senators")
        print("gsenators PARTYNAME: get all senators of party == (Democratic, Republican, Independent)")
        print("")
        continue
    elif r == "pstates":
        print_all_states()
        continue
    elif r == "psenators":
        print_all_senators()
        continue
    elif r == "gsenators":
        try:
            sen = get_all_senators_of_party(response.split(" ")[1]) #pass through party name
            print(sen)
        except:
            print("put an argument in after 'gsenators'")
        continue
    elif r == "quit":
        break
    else:
        print("that is not a command!")


print("Done.")
exit()
