import psycopg2

conn = None
cur = None

def start_connection():
    global conn, cur
    conn = connect_postgres_with_link()
    cur = conn.cursor()

def connect_postgres():
    print("Attempting to connect to the database...")
    n = input("enter the database name: ")
    u = input("enter your database username: (blank for default)")
    p = input("enter your database password: ")
    if u == "":
        u = "postgres"  # set as default
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


# connect online
def connect_postgres_with_link():
    conn_str = "postgres://cse412_1716:rXmvrZ07nhKSr1m0FTv_@cse412-1716.postgresql.a.osc-fr1.scalingo-dbs.com:33302/cse412_1716?sslmode=prefer"
    link = conn_str or str(input("Insert the database link from the user manual here: "))
    try:
        c = psycopg2.connect(link)
        print("Successfully connected to the database")
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


def print_all_transactions(transactions):
    print("Printing all states:")
    for transaction in transactions:
        print("   " + str(transaction))  # print the states row


# print transactions in a formatted style
def print_transactions(transactions):
    if not transactions:
        print("no transactions to print")
        return
    for transaction in transactions:
        print("Transaction " + str(transaction[0]) + ": " + str(transaction[3]) + " | " + str(
            transaction[4]) + " | " + str(transaction[5]))


def print_senators(senators):
    for senator in senators:
        print("Senator " + str(senator[1]) + " " + str(senator[2]) + " : " + str(senator[5]))


def get_all_senators():
    cur.execute("SELECT * FROM senator")
    result = cur.fetchall()
    return result


def get_all_states():
    cur.execute("SELECT * FROM state")
    result = cur.fetchall()
    return result


def get_all_transactions():
    cur.execute("SELECT * FROM transaction")
    result = cur.fetchall()
    return result


def get_all_stocks():
    cur.execute("SELECT * FROM stock")
    result = cur.fetchall()
    return result


# set value to less than or equal to 0 for any of the ranges to not check that range
def get_transactions_in_amount_range(amount_range):
    sql_query = "SELECT * FROM transaction WHERE t_amount = '" + str(amount_range) + "'"
    cur.execute(sql_query)
    result = cur.fetchall()
    #print(sql_query)
    return result


def get_transactions_with_type(transaction_type):
    # sql query beforehand
    sql_query = "SELECT * FROM transaction WHERE t_type = '" + str(transaction_type) + "'"
    cur.execute(sql_query)
    result = cur.fetchall()
    #print(sql_query)
    return result

def get_transactions_with_amount_range_and_type(amount_range, transaction_type):
    sql_query = "SELECT * FROM transaction WHERE t_amount = '" + str(amount_range) + "' AND t_stockidkey IN (SELECT stck_stockidkey FROM stock WHERE stck_sector = '" + str(transaction_type) + "')"
    cur.execute(sql_query)
    result = cur.fetchall()
    #print(sql_query)
    return result

def get_stock_sectors():
    sql_query = "SELECT DISTINCT stck_sector FROM stock"
    cur.execute(sql_query)
    result = cur.fetchall()
    #print(sql_query)
    return result

def get_transactions_with_stock(stock_id):
    sql_query = "SELECT * FROM transaction WHERE t_stockidkey = '" + str(stock_id) + "'"
    cur.execute(sql_query)
    result = cur.fetchall()
    #print(sql_query)
    return result


def get_transactions_with_senator(senator_id):
    sql_query = "SELECT * FROM transaction WHERE t_senatoridkey = '" + str(senator_id) + "'"
    cur.execute(sql_query)
    result = cur.fetchall()
    #print(sql_query)
    return result


def sort_transaction_by_column(transactions, column_index, is_reversed):
    print("attempting to sort by column: " + str(column_index))
    result = transactions

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


def add_transaction(senator_id, stock_id, amount_range, date, stock_type):
    # get all the transactions
    transactions = get_all_transactions()

    # get the last transaction in the list sorted by ids, make this transaction id + 1 that
    # most recent transaction should be the first
    result = sort_transaction_by_column(transactions, 0, True)
    print(result)

    # get the first id in transaction list
    new_id = int(result[0][0]) + 1

    print("adding new transaction with id of " + str(new_id))

    sql_query = f"INSERT INTO transaction(t_transactionid, t_senatoridkey, t_stockidkey, t_amount, t_date, t_type) VALUES ('{new_id}', '{senator_id}', '{stock_id}', '{amount_range}', '{date}', '{stock_type}')"
    #print(sql_query)
    cur.execute(sql_query)


def delete_transaction(transaction_id):
    transactions = get_all_transactions()
    removed = []
    for transaction in transactions:
        if int(transaction[0]) == transaction_id:
            print("found id of: " + str(transaction_id))
            removed = transaction
            print("removing...")
            cur.execute("DELETE FROM transaction WHERE t_transactionid = '" + str(transaction_id) + "'")
            print("removed!")
            return removed
    return None


def find_senator_id(senator_name):
    for senator in get_all_senators():
        current_name = str(senator[1]) + " " + str(senator[2])  # get the name of current senator
        if senator_name == current_name:
            return senator[0]  # return the id of this senator
    return None  # return none otherwise


def find_stock_id(stock_ticker):
    for stock in get_all_stocks():
        if stock[3] == stock_ticker:
            return stock[0]  # found the right stock ticker so return
    return None  # return none otherwise


def find_stock(stock_id):
    for stock in get_all_stocks():
        if stock[0] == stock_id:
            return stock  # found the right stock ticker so return stock
    return None  # return none otherwise


def find_senator(senator_id):
    for senator in get_all_senators():
        if senator[0] == senator_id:
            return senator  # return senator
    return None  # return none otherwise


# find transaction with given transaction id
def find_transaction(transaction_id):
    transactions = get_all_transactions()  # get all of the transactions
    found = []
    for transaction in transactions:
        if int(transaction[0]) == transaction_id:
            print("found id of: " + str(transaction_id))
            found = transaction
            return transaction  # found transaction so return it
    return None  # return none if none found

def get_senator_by_transaction_id(t_id):
    sql_query = "SELECT s_firstname, s_lastname FROM transaction, senator WHERE t_senatoridkey = s_senatoridkey AND t_transactionid = " + str(t_id)
    cur.execute(sql_query)
    result = cur.fetchall()
    return result

def get_state_by_senator_name(first, last):
    sql_query="SELECT st_statename FROM senator, state, represents WHERE st_stateidkey = r_stateidkey AND s_senatoridkey = r_senatoridkey AND s_firstname = '" + str(first) +"' AND s_lastname = '" + str(last)+"'"
    cur.execute(sql_query)
    result = cur.fetchall()
    return result

def get_stock_info_from_transaction_id(t_id):
    sql_query = "SELECT stck_stockname, stck_sector FROM transaction, stock WHERE"
    sql_query = sql_query + " t_stockidkey = stck_stockidkey AND t_transactionid = '" + str(t_id) + "'"
    cur.execute(sql_query)
    result = cur.fetchall()
    return result


def print_transaction(transaction):
    transaction_id = str(transaction[0])
    transaction_amount = str(transaction[3])
    transaction_type = str(transaction[4])
    transaction_date = str(transaction[5])
    senator = find_senator(transaction[1])
    stock = find_stock(transaction[2])
    senator_name = str(senator[1]) + " " + str(senator[2])  # get the name of current senator
    stock_name = str(stock[1])
    stock_ticker = str(stock[3])
    print(
        transaction_id + ": " + senator_name + " | " + transaction_type + " | " + stock_name + " (" + stock_ticker + ") | " + transaction_amount + " | " + transaction_date)
