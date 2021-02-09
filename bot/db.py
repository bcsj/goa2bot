import mysql.connector

# Connection
cnx_info = {
    'host': '',
    'user': '',
    'password': '',
    'database': ''
}

# Database connection decorator
def dbconnection(func):
    def wrapper(*args, **kwargs):
        uuid = uuid4()
        db.connect(uuid)
        res = func(*args, **kwargs)
        db.close(uuid)
        return res
    return wrapper

class DB:
    def __init__(self):
        self.cnx = None
        self.uuid = None
        # The uuid ensures that we don't accidentally open/close the connection prematurely because another function call wanted a connection to the database.
    
    def connect(self, uuid):
        if uuid is None:
            self.cnx = mysql.connector.connect(**cnx_info)
            self.uuid = uuid

    def cursor(self):
        return self.cnx.cursor(buffered=True)

    def close(self, uuid):
        if uuid == self.uuid:
            self.cnx.close()
            self.uuid = None
