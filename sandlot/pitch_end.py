import pandas as pd
import sqlite3

DB_NAME = 'qux.db'

df = None
with sqlite3.connect(DB_NAME) as n:
    df = pd.read_sql("""
        SELECT pitch.pitch_id,
               pitch.y_nought,
               pitch.vy_start,
               pitch.ay_start,
               pitch.vx_start,
               pitch.ax_start,
               pitch.vz_start,
               pitch.az_start
          FROM pitch
          LEFT
          JOIN pitch_end
            ON pitch.pitch_id = pitch_end.pitch_id
         WHERE pitch_end.pitch_id IS NULL""", n)

df[u'vy_end'] = -(df[u'vy_start']**2 + 2*df[u'ay_start']*(0 - df[u'y_nought']))**0.5
df[u't'] = (df[u'vy_end'] - df[u'vy_start'])/df[u'ay_start']

df[u'vx_end'] = df[u'vx_start'] + df[u'ax_start']*df[u't']
df[u'vz_end'] = df[u'vz_start'] + df[u'az_start']*df[u't']


with sqlite3.connect(DB_NAME) as n:
    df[[u'pitch_id', u't', u'vx_end', u'vy_end', u'vz_end']].to_sql(name='pitch_end', con=n, if_exists='append', index=False)
