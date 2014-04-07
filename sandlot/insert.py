from __future__ import division
import sqlite3 as lite
from collections import OrderedDict



def row_factory(cursor, row):
    return OrderedDict((column[0], row[i],) for i, column in \
                        enumerate(cursor.description))

connection = lite.connect('foo.db')
connection.row_factory = row_factory

main_cursor = connection.cursor()
#main_cursor.executescript(open('./db/create_tables.sql', 'rb').read())

main_cursor.execute('SELECT DISTINCT gameday_id FROM game')
existing_gameday_ids = [row['gameday_id'] for row in main_cursor]



from inserter import GameInserter, InningInserter, AtBatInserter, ActionInserter, PitchInserter, RunnerInserter, GameUmpireInserter, GamePlayerInserter, GameCoachInserter

game_inserter = GameInserter(connection)
inning_inserter = InningInserter(connection)
at_bat_inserter = AtBatInserter(connection)
action_inserter = ActionInserter(connection)
pitch_inserter = PitchInserter(connection)
runner_inserter = RunnerInserter(connection)
game_umpire_inserter = GameUmpireInserter(connection)
game_player_inserter = GamePlayerInserter(connection)
game_coach_inserter = GameCoachInserter(connection)



from scraping import Game, Innings
from lxml import etree
import gzip

def get_game(gameday_id):
    file_name = './xml/2013/%s-players.xml.gz' % gameday_id
    return Game(etree.fromstring(gzip.open(file_name, 'rb').read())).as_dict

def get_innings(gameday_id):
    file_name = './xml/2013/%s-inning_all.xml.gz' % gameday_id
    return Innings(etree.fromstring(gzip.open(file_name, 'rb').read()))

#gameday_ids = ('gid_2013_05_20_phimlb_miamlb_1',
#               'gid_2013_05_15_clemlb_phimlb_1',)

def insert_game(gameday_id):
    game, innings = get_game(gameday_id), get_innings(gameday_id)
    game_id = game_inserter.insert(gameday_id, game)
    for umpire in game['umpires']:
        game_umpire_id = game_umpire_inserter.insert(game_id, umpire)
    for status in ('away', 'home',):
        team = game[status]
        for player in team['players']:
            game_player_id = game_player_inserter.insert(game_id, player)
        for coach in team['coaches']:
            game_coach_id = game_coach_inserter.insert(
                team['abbr'],
                'A' if status == 'away' else 'H',
                game_id,
                coach)
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

from sys import argv
gameday_id = argv[1]
print 'GameDay ID: {0}'.format(argv[1])
if gameday_id in existing_gameday_ids:
    print 'Already exists in the database; exiting...'
else:
    insert_game(gameday_id)
    connection.commit()
    print 'Committed...'
