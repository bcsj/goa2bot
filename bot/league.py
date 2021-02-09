from uuid import uuid4

from db import DB, dbconnection
from misc import sanitize, split_discord_name as dnsplit
from misc import win_rate, confidence, p_value
# ================================================
# Database
db = DB()

# ================================================
# Player functions

@dbconnection
def create(name, started_at, end_at, description, mode):
    db.cursor()
    uuid = uuid4()
    # TODO: Need to figure out some sanitizing here

    # Insert into players
    sql = """
        INSERT INTO leagues (
            uuid, 
            name,
            started_at
            end_at,
            description,
            mode) 
        VALUES ('%s','%s',DATE(%s),DATE(%s),'%s', %d)
        """
    cur.execute(sql, uuid, name, str(started_at), str(end_at), description, mode)
