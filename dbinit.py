import sqlite3

conn = sqlite3.connect('nfl.db')

c = conn.cursor()

#TODO: Determine of scrapy needs "High Concurrency". Might be better to use a client server instead


#TODO: Come up with a decent schema
# Current thoughts: player % (name, age, weight, height, external stats)
c.execute('''CREATE TABLE quarterbacks
             (comps INTEGER, pass_att INTEGER, pct REAL, pass_yards INTEGER, pass_avg REAL, pass_td INTEGER, interceptions INTEGER,
              sck INTEGER, scky INTEGER, rate REAL, rush_att INTEGER, rush_yards INTEGER, rush_avg REAL, rush_td INTEGER,
              fum INTEGER, lost INTEGER)''')

c.execute('''CREATE TABLE offense_players
             (rec INTEGER, recv_yards INTEGER, recv_avg INTEGER, recv_long INTEGER , recv_lng INTEGER, recv_td INTEGER, rush_att INTEGER,
              rush_yards INTEGER, rush_avg REAL, rush_long INTEGER, rush_td INTEGER, fumb INTEGER, lost INTEGER)''')

c.execute('''CREATE TABLE defense_players
             (comb INTEGER, total INTEGER, ast INTEGER, sck REAL, sfty INTEGER,  pdef INTEGER, interceptions INTEGER, yds INTEGER,
               avg REAL, long INTEGER, tds INTEGER, ff INTEGER)''')


c.execute('''CREATE TABLE punters
             (punts INTEGER, yards INTEGER, net_yards INTEGER, long INTEGER, avg REAL, net_avg REAL, blk INTEGER, oob INTEGER, dn INTEGER,
              INTEGER in_20, tb INTEGER, fc INTEGER, ret INTEGER, rety INTEGER, td INTEGER)''')

c.execute('''CREATE TABLE placekickers
             (fg_blk INTEGER, lng INTEGER, fg_att INTEGER, fgm INTEGER, pct REAL, xpm INTEGER, xp_att INTEGER, xp_pct REAL, ko_blk INTEGER,
              ko INTEGER, ko_avg INTEGER, tb INTEGER, ret INTEGER, ret_yd INTEGER)''')
#Not ready to add yet
#c.execute('''CREATE TABLE offensive_line_player''')
#c.execute('''CREATE TABLE coaches''')
#c.execute('''CREATE TABLE teams''')
