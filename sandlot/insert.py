import sqlite3
from os import path, listdir

DB_NAME = 'qux.db'

connection = sqlite3.connect(DB_NAME)

cursor = connection.cursor()
cursor.execute('PRAGMA foreign_keys = ON')
cursor.execute('PRAGMA journal_mode = OFF')
cursor.execute('PRAGMA synchronous = OFF')
#cursor.executescript(open('./db/create_tables.sql', 'rb').read())
#cursor.executescript(open('./db/create_views.sql', 'rb').read())
#create_view('starting_pitcher')
#create_view('pitch_cat')

#cursor.execute('SELECT DISTINCT game_id FROM batted_ball')
cursor.execute('SELECT DISTINCT game_id FROM game')
existing_game_ids = [row[0] for row in cursor]



from inserter import GameInserter, AtBatInserter, ActionInserter, BattedBallInserter, PitchInserter, RunnerInserter, GameUmpireInserter, GamePlayerInserter, GameCoachInserter

game_inserter = GameInserter(connection)
at_bat_inserter = AtBatInserter(connection)
action_inserter = ActionInserter(connection)
batted_ball_inserter = BattedBallInserter(connection)
pitch_inserter = PitchInserter(connection)
runner_inserter = RunnerInserter(connection)
game_umpire_inserter = GameUmpireInserter(connection)
game_player_inserter = GamePlayerInserter(connection)
game_coach_inserter = GameCoachInserter(connection)



from scraping import Game, Innings, BattedBalls
from lxml import etree
import gzip

def get_game(game_id):
    file_name = './xml/{0}/{1}-players.xml.gz'.format(game_id[4:8], game_id)
    return Game(etree.fromstring(gzip.open(file_name, 'rb').read())).as_dict

def get_innings(game_id):
    file_name = './xml/{0}/{1}-inning_all.xml.gz'.format(game_id[4:8], game_id)
    return Innings(etree.fromstring(gzip.open(file_name, 'rb').read()))

def get_batted_balls(game_id):
    file_name = './xml/{0}/{1}-inning_hit.xml.gz'.format(game_id[4:8], game_id)
    return BattedBalls(etree.fromstring(gzip.open(file_name, 'rb').read()))

def _old_insert_game(game_id):
    game, innings = get_game(game_id), get_innings(game_id)
    game_id = game_inserter.insert(game_id, game)
    for umpire in game['umpires']:
        game_umpire_id = game_umpire_inserter.insert(game_id, umpire)
    for status in ('away', 'home',):
        team = game[status]
        for player in team['players']:
            try:
                game_player_id = game_player_inserter.insert(game_id, player)
            except:
                print player
                raise
        for coach in team['coaches']:
            game_coach_id = game_coach_inserter.insert(
                team['abbr'],
                'A' if status == 'away' else 'H',
                game_id,
                coach)
    for inning in innings:
        for inning_side in ('top', 'bottom',):
            if inning[inning_side] is None:
                continue
            for at_bat in inning[inning_side]['at_bats']:
                at_bat_id = at_bat_inserter.insert(
                    inning['number'],
                    inning_side, game_id, at_bat)
                for pitch in at_bat['pitches']:
                    pitch_id = pitch_inserter.insert(at_bat_id, pitch)
                for runner in at_bat['runners']:
                    runner_id = runner_inserter.insert(at_bat_id, runner)
            for action in inning[inning_side]['actions']:
                action_id = action_inserter.insert(
                    inning['number'],
                    inning_side, game_id, action)

def _insert_game(game_id):
    game = get_game(game_id)
    game_id = game_inserter.insert(game_id, game)
    for umpire in game['umpires']:
        game_umpire_id = game_umpire_inserter.insert(game_id, umpire)
    for status in ('away', 'home',):
        team = game[status]
        for player in team['players']:
            try:
                game_player_id = game_player_inserter.insert(game_id, player)
            except:
                print player
                raise
        for coach in team['coaches']:
            game_coach_id = game_coach_inserter.insert(
                team['abbr'],
                'A' if status == 'away' else 'H',
                game_id,
                coach)

def _insert_innings(game_id):
    innings = get_innings(game_id)
    for inning in innings:
        for inning_side in ('top', 'bottom',):
            if inning[inning_side] is None:
                continue
            for at_bat in inning[inning_side]['at_bats']:
                at_bat_id = at_bat_inserter.insert(
                    inning['number'],
                    inning_side, game_id, at_bat)
                for pitch in at_bat['pitches']:
                    pitch_id = pitch_inserter.insert(at_bat_id, pitch)
                for runner in at_bat['runners']:
                    runner_id = runner_inserter.insert(at_bat_id, runner)
            for action in inning[inning_side]['actions']:
                action_id = action_inserter.insert(
                    inning['number'],
                    inning_side, game_id, action)

def _insert_batted_balls(game_id):
    batted_balls = get_batted_balls(game_id)
    for batted_ball in batted_balls:
        batted_ball_id = batted_ball_inserter.insert(game_id, batted_ball)

def insert_game(game_id):
    _insert_game(game_id)
    _insert_innings(game_id)
    _insert_batted_balls(game_id)

def exec_view_sql(view_name, sql_file_name):
    view_root = path.join('./db/materialized_views', view_name)
    view_sql = ''
    with open(path.join(view_root, sql_file_name), 'rb') as sql_file:
        view_sql = sql_file.read()
    cursor.executescript(view_sql)

def create_view(view_name):
    exec_view_sql(view_name, 'create_table.sql')

def refresh_view(view_name):
    exec_view_sql(view_name, 'refresh.sql')



if __name__ == '__main__':
    import fileinput
    for line in fileinput.input():
        game_id = line.rstrip()
        print 'GameDay ID: {0}'.format(game_id)
        if game_id in existing_game_ids:
            print 'Already exists in the database; exiting...'
        else:
            insert_game(game_id)
            #_insert_batted_balls(game_id)
            connection.commit()
            print 'Committed...'
    for view_name in listdir('./db/materialized_views'):
        print 'Refreshing view: {0}'.format(view_name)
        refresh_view(view_name)
        connection.commit()
        print 'Committed...'
