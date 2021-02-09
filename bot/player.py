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
def create(discord_name, discord_id):
    db.cursor()
    uuid = uuid4()
    name, discriminator = dnsplit(discord_name)
    nick = name + "#" + discriminator

    # Insert into players
    sql = """
        INSERT INTO players (
            uuid, 
            name) 
        VALUES ('%s','%s')
        """
    cur.execute(sql, uuid, nick)

    # Insert into discord accounts
    sql = """
        INSERT INTO discord_accounts (
            id,
            name,
            discriminator,
            player_id) 
        VALUES (%d,'%s','%s','%s')
        """
    cur.execute(sql, discord_id, name, discriminator, uuid)

@dbconnection
def get_uuid(discord_id):
    cur = db.cursor()
    sql = """
        SELECT player_id 
        FROM discord_accounts 
        WHERE id=%d
        """
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
    sql = """
        UPDATE players 
        SET name='%s' 
        WHERE uuid='%s'
        """
    cur.execute(sql, new_name, uuid)

@dbconnection
def get_num_games(discord_id, league_id=None):
    cur = db.cursor
    uuid = get_uuid(discord_id)
    if league_id is None:
        sql = """
            SELECT * 
            FROM game_players 
            WHERE player_id='%s'
            """
        cur.execute(sql, uuid)
        return cur.rowcount
    else:
        # TODO Implement league filtered count
        None

@dbconnection
def get_num_wins(discord_id, league_id=None):
    cur = db.cursor
    uuid = get_uuid(discord_id)
    if league_id is None:
        sql = """
            SELECT 
                g.state, 
                g.winning_team, 
                gp.player_id,
                gp.team 
            FROM games AS g 
            LEFT JOIN game_players AS gp 
            ON g.uuid = gp.game_id
            WHERE g.state=3 
                AND gp.player_id='%s' 
                AND g.winning_team=gp.team
            """
        cur.execute(sql, uuid)
        return cur.rowcount
    else:
        # TODO Implement league filtered count
        None

def get_win_rate(discord_id, league_id=None):
    w = get_num_wins(discord_id, league_id=None)
    g = get_num_games(discord_id, league_id=None)
    return win_rate(g, w)

def get_confidence(discord_id, league_id=None):
    g = get_num_games(discord_id, league_id=None)
    return confidence(g)

def get_p_value(discord_id, league_id=None):
    w = get_num_wins(discord_id, league_id=None)
    g = get_num_games(discord_id, league_id=None)
    return p_value(g, w)