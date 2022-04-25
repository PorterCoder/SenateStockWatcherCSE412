import psycopg2


def connect_postgres(name, user, password):
    print("Attempting to connect to the database...")
    n = name
    u = user
    if u == "":
        u = "postgres"
    p = password
    c = None
    try:
        c = psycopg2.connect(
            dbname=n,
            user=u,
            host='localhost',  # assumes local host for now
            password=p
        )
        print("Successful Connection.")
    except Exception as err:
        print("I am unable to connect to the database")
        c = None
        exit()
    return c


def print_all_senators(senators):
    print("Printing all senators:")
    for senator in senators:
        print("   " + str(senator))  # print the senator row


def print_all_states(states):
    print("Printing all states:")
    for state in states:
        print("   " + str(state))  # print the states row


# set value to less than or equal to 0 for any of the ranges to not check that range
def get_transactions_in_amount_range(amount_range):
    # amount_range == $1,001 - $15,000 or $50,001 - $100,000
    # or $15,001 - $50,000 or $100,001 - $250,000
    # or $250,001 - $500,000 or $500,001 - $1,000,000

    # sql query beforehand
    sql_query = "SELECT * FROM transaction WHERE t_amount = '" + amount_range + "'"
    cur.execute(sql_query)
    result = cur.fetchall()

    print(sql_query)

    # return the result
    return result


def get_transactions_with_type(transaction_type):
    # sql query beforehand
    sql_query = "SELECT * FROM transaction WHERE t_type = '" + transaction_type + "'"
    cur.execute(sql_query)
    result = cur.fetchall()

    print(sql_query)

    # return the result
    return result


def sort_transaction_by_column(transactions, column_index, is_reversed):
    print("attempting to sort by colum: " + str(column_index))
    result = transactions
    print(transactions)
    # if this list is empty then return
    if not transactions:
        print("the transaction list you are trying to sort is empty!")
        return

    # if the column to sort by is not in range then return
    if column_index not in range(0, len(transactions[0])):
        print(str(column_index) + " is not in range of 0 - " + str(len(transactions[0]) - 1))
        return

    # sort by the column index
    result.sort(key=lambda i: i[column_index], reverse=is_reversed)

    print("sorting transaction by column " + str(column_index) + " was successful!")
    return result


def add_transaction(stock_id, senator_id, stock_type, amount_range):
    # get all the transactions
    cur.execute("SELECT * FROM transaction")
    transactions = cur.fetchall()

    # get the last transaction in the list sorted by ids, make this transaction id + 1 that
    # most recent transaction should be the first
    result = sort_transaction_by_column(transactions, 0, False)

    # get the first id in transaction list
    new_id = int(result[0][0]) + 1

    print(new_id)


def delete_transaction(transaction_id):
    cur.execute("SELECT * FROM transaction")
    transactions = cur.fetchall()
    removed = []
    for transaction in transactions:
        if int(transaction[0]) == transaction_id:
            print("found id of " + str(transaction_id))
            removed = transaction
            print("removing...")
            break

    # if removed is null then could not find
    if not removed:
        print("could not find transaction of " + str(transaction_id))
    else:
        print("removed transaction: " + str(transaction))


def print_transactions(transactions):
    for transaction in transactions:
        print("Transaction " + str(transaction[0]) + ": " + str(transaction[3]) + " | " + str(
            transaction[4]) + " | " + str(transaction[5]))


databaseName = input("enter the database name: ")
databaseUser = input("enter your database username: (blank for default)")
databasePassword = input("enter your database password: ")

conn = connect_postgres(databaseName, databaseUser, databasePassword)
cur = conn.cursor()

# EXAMPLES -----------------------------------------------------------------------------------------------------


add_transaction(1, 2, 3, 4)
delete_transaction(1)
delete_transaction(0)


# test = get_transactions_in_amount_range("$1,001 - $15,000")

# sort by transaction result by id (transaction 1 first when True, the newest transaction first when False)
# sorted_by_id = sort_transaction_by_column(test, 0, True)
# sort by transaction result by date (the newest first when True, oldest when False)
# sorted_by_date = sort_transaction_by_column(test, 4, True)

# print_transactions(sorted_by_id)
# print_transactions(sorted_by_date)
