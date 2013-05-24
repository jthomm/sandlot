from __future__ import division
import sqlite3 as lite
from collections import OrderedDict



def row_factory(cursor, row):
    return OrderedDict((column[0], row[i],) for i, column in \
                        enumerate(cursor.description))

connection = lite.connect('foo.db')
connection.row_factory = row_factory

main_cursor = connection.cursor()
main_cursor.executescript(open('./db/ddl.sql', 'rb').read())



from inserter import GameInserter, InningInserter, AtBatInserter, ActionInserter, PitchInserter, RunnerInserter

game_inserter = GameInserter(connection)
inning_inserter = InningInserter(connection)
at_bat_inserter = AtBatInserter(connection)
action_inserter = ActionInserter(connection)
pitch_inserter = PitchInserter(connection)
runner_inserter = RunnerInserter(connection)



from scraping import Game, Innings
from lxml import etree
import gzip

def get_game(gameday_id):
    file_name = './xml/2013/%s-players.xml.gz' % gameday_id
    return Game(etree.fromstring(gzip.open(file_name, 'rb').read())).as_dict

def get_innings(gameday_id):
    file_name = './xml/2013/%s-inning_all.xml.gz' % gameday_id
    return Innings(etree.fromstring(gzip.open(file_name, 'rb').read()))

gameday_ids = ('gid_2013_05_20_phimlb_miamlb_1',
               'gid_2013_05_15_clemlb_phimlb_1',)

#gameday_ids = ('gid_2013_05_20_phimlb_miamlb_1',)

for gameday_id in gameday_ids:
    game = get_game(gameday_id)
    innings = get_innings(gameday_id)
    game_id = game_inserter.insert(gameday_id, game)
    for inning in innings:
        inning_id = inning_inserter.insert(game_id, inning)
        for side in ('top', 'bottom',):
            if inning[side] is None:
                continue
            for at_bat in inning[side]['at_bats']:
                at_bat_id = at_bat_inserter.insert(inning_id, side, at_bat)
                for pitch in at_bat['pitches']:
                    pitch_id = pitch_inserter.insert(at_bat_id, pitch)
                for runner in at_bat['runners']:
                    runner_id = runner_inserter.insert(at_bat_id, runner)
            for action in inning[side]['actions']:
                action_id = action_inserter.insert(inning_id, side, action)
