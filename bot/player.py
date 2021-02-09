import re
from uuid import uuid4

from db import DB, dbconnection
from misc import sanitize, split_discord_name as dnsplit

# ================================================
# Database
db = DB()



# ================================================
# Player functions

@dbconnection
def create(discord_name, discord_id):
    db.cursor()
    name, discriminator = dnsplit(discord_name)
    nick = name + "#" + discriminator
    uuid = uuid4()
    
    # Insert into players
    sql = "INSERT INTO `players` (`uuid`, `name`) VALUES ('%s','%s')"
    cur.execute(sql, uuid, nick)

    # Insert into discord accounts
    sql = "INSERT INTO `discord_accounts` (`id`,`name`,`discriminator`,`player_id`) VALUES (%d,'%s')"
    cur.execute(sql, discord_id, name, discriminator, uuid)

@dbconnection
def get_uuid(discord_id):
    cur = db.cursor()
    sql = "SELECT `player_id` FROM `discord_accounts` WHERE `id`=%d"
    cur.execute(sql, discord_id)
    if cur.rowcount == 0:
        return False
    res = cur.fetchall()
    return res[0][0]

def exists(discord_id):
    if get_uuid(discord_id)
        return True
    return False

@dbconnection
def change_name(discord_id, new_name):
    cur = db.cursor()
    new_name = sanitize(new_name)
    uuid = get_uuid(discord_id)
    sql = "UPDATE `players` SET `name`='%s' WHERE `uuid`='%s'"
    cur.execute(sql, new_name, uuid)

@dbconnection
def get_num_games(discord_id, league_id=None):
    cur = db.cursor
    if league_id is None:
        

