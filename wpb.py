import config
import sqlite3

#Opens the account database, returning the SQLite object.
def opendb() :
    accounts = sqlite3.connect(config.path + '/accounts.sqlite3')
    with accounts:
        accounts.execute("CREATE TABLE IF NOT EXISTS accounts "
                         "(username TEXT NOT NULL PRIMARY KEY, " +
                         " balance INTEGER NOT NULL)")
    return accounts

#Opens the queue database, returning the SQLite object.
def openqueue() :
    queue = sqlite3.connect(config.path + '/accounts.sqlite3')
    with queue:
        queue.execute("CREATE TABLE IF NOT EXISTS queue"
                      "(username TEXT NOT NULL PRIMARY KEY,"
                      " action INTEGER NOT NULL)")
    return queue

#Delete the selected user account.
def deleteaccount(user: str, accountsdb) :
    user = user.lower()
    with accountsdb:
        accountsdb.execute("DELETE FROM accounts WHERE username=" + user)

#Create a new account. Returns true if the user already has an account, otherwise, returns false
def createaccount(user: str, accountsdb, startingbalance: int = 0) :
    user = user.lower()
    with accountsdb :

        accountsdb.execute("INSERT INTO accounts (username, balance) VALUES (?, 0)"
                           " ON CONFLICT (username) DO UPDATE SET balance = balance",
                           (user,))
        if (startingbalance != 0) :
            change(user, startingbalance, accountsdb)
            
#Credit or debit an account with a certain number of points
def change(user: str, amount: int, accountsdb) :
    user = user.lower()
    accountsdb.execute("UPDATE accounts " +
                       "SET balance = balance + " + str(amount) +
                       " WHERE username =\"" + user + '"')

#Queries a user's balance. Returns None if the user doesn't have an account
def balance(user: str, accountsdb = None) :
    if accountsdb == None :
        accountsdb = opendb()
    user = user.lower()
    record = accountsdb.execute("SELECT balance FROM accounts WHERE username=\"" + user + '"')
    record = record.fetchone()
    if record is None :
        return None
    else :
        (balance, ) = record
    return balance