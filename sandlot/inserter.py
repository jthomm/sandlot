class Inserter(object):

    def __init__(self, connection):
        self.cursor = connection.cursor()

    def insert(self, *args):
        raise NotImplementedError()



class GameInserter(Inserter):

    def insert(self, game_id, game):
        self.cursor.execute('''
        INSERT INTO game (
            game_id
          , venue_name
          , date_str
          , away_abbr
          , away_full
          , home_abbr
          , home_full
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (game_id,
              game['venue'],
              game['date_string'],
              game['away']['abbr'],
              game['away']['full_name'],
              game['home']['abbr'],
              game['home']['full_name'],)
        )
        #return self.cursor.lastrowid
        return game_id



class AtBatInserter(Inserter):

    def insert(self, inning_num, inning_side, game_id, at_bat): 
        self.cursor.execute('''
        INSERT INTO at_bat (
            description
          , event_type
          , at_bat_num
          , timestamp
          , balls_aft
          , strikes_aft
          , outs_aft
          , batter_id
          , batter_stnd
          , pitcher_id
          , pitcher_hnd
          , inning_num
          , inning_side
          , game_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (at_bat['description'],
              at_bat['event'],
              at_bat['number'],
              at_bat['timestamp'],
              at_bat['balls'],
              at_bat['strikes'],
              at_bat['outs'],
              at_bat['batter_id'],
              at_bat['batter_stance'],
              at_bat['pitcher_id'],
              at_bat['pitcher_hand'],
              inning_num,
              inning_side,
              game_id,)
        )
        return self.cursor.lastrowid



class ActionInserter(Inserter):

    def insert(self, inning_num, inning_side, game_id, action):
        self.cursor.execute('''
        INSERT INTO action (
            description
          , event_type
          , player_id
          , timestamp
          , pitch_num
          , balls_bef
          , strikes_bef
          , outs_bef
          , inning_num
          , inning_side
          , game_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (action['description'],
              action['event'],
              action['player_id'],
              action['timestamp'],
              action['pitch'],
              action['balls'],
              action['strikes'],
              action['outs'],
              inning_num,
              inning_side,
              game_id,)
        )
        return self.cursor.lastrowid



class PitchInserter(Inserter):

    def insert(self, at_bat_id, pitch):
        self.cursor.execute('''
        INSERT INTO pitch (
            description
          , commentary
          , pitch_num
          , timestamp
          , pitch_type
          , confidence
          , zone_num
          , sz_top
          , sz_bot
          , nastiness
          , result_code
          , gd_end_x
          , gd_end_z
          , start_speed
          , end_speed
          , mvt_x
          , mvt_z
          , pfx_end_x
          , pfx_end_z
          , pfx_start_id
          , x_nought
          , y_nought
          , z_nought
          , vx_start
          , vy_start
          , vz_start
          , ax_start
          , ay_start
          , az_start
          , spin_angle
          , spin_rate
          , y_max_break
          , break_angle
          , break_mag
          , at_bat_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (pitch['description'],
              pitch['cc'],
              pitch['pitch_id'],
              pitch['timestamp'],
              pitch['pitch_type'],
              pitch['type_confidence'],
              pitch['zone'],
              pitch['sz_top'],
              pitch['sz_bot'],
              pitch['nasty'],
              pitch['result'],
              pitch['x'],
              pitch['y'],
              pitch['start_speed'],
              pitch['end_speed'],
              pitch['pfx_x'],
              pitch['pfx_z'],
              pitch['px'],
              pitch['pz'],
              pitch['sv_id'],
              pitch['x0'],
              pitch['y0'],
              pitch['z0'],
              pitch['vx0'],
              pitch['vy0'],
              pitch['vz0'],
              pitch['ax'],
              pitch['ay'],
              pitch['az'],
              pitch['spin_dir'],
              pitch['spin_rate'],
              pitch['break_y'],
              pitch['break_angle'],
              pitch['break_length'],
              at_bat_id,)
        )
        return self.cursor.lastrowid



class RunnerInserter(Inserter):

    def insert(self, at_bat_id, runner):
        self.cursor.execute('''
        INSERT INTO runner (
            player_id
          , start_base
          , end_base
          , event_type
          , at_bat_id
        ) VALUES (?, ?, ?, ?, ?)
        ''', (runner['runner_id'],
              runner['start'],
              runner['end'],
              runner['event'],
              at_bat_id,)
        )
        return self.cursor.lastrowid



class GameUmpireInserter(Inserter):

    def insert(self, game_id, umpire):
        self.cursor.execute('''
        INSERT INTO game_umpire (
            umpire_id
          , full_name
          , position
          , game_id
        ) VALUES (?, ?, ?, ?)
        ''', (umpire['umpire_id'],
              umpire['full_name'],
              umpire['position'],
              game_id,)
        )
        return self.cursor.lastrowid



class GamePlayerInserter(Inserter):

    def insert(self, game_id, player):
        self.cursor.execute('''
        INSERT INTO game_player (
            player_id
          , first_name
          , last_name
          , box_name
          , handedness
          , team_id
          , team_abbr
          , status
          , uni_number
          , position
          , game_position
          , curr_position
          , batting_order
          , avg
          , rbi
          , hr
          , wins
          , losses
          , era
          , game_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (player['player_id'],
              player['first_name'],
              player['last_name'],
              player['box_name'],
              player['handedness'],
              player['team_id'],
              player['team_abbr'],
              player['status'],
              player['uniform_number'],
              player['position'],
              player['game_position'],
              player['current_position'],
              player['batting_order'],
              player['avg'],
              player['rbi'],
              player['hr'],
              player['wins'],
              player['losses'],
              player['era'],
              game_id,)
        )
        return self.cursor.lastrowid



class GameCoachInserter(Inserter):

    def insert(self, team_abbr, status, game_id, coach):
        self.cursor.execute('''
        INSERT INTO game_coach (
            coach_id
          , first_name
          , last_name
          , team_abbr
          , status
          , uni_number
          , position
          , game_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (coach['coach_id'],
              coach['first_name'],
              coach['last_name'],
              team_abbr,
              status,
              coach['uniform_number'],
              coach['position'],
              game_id,)
        )
        return self.cursor.lastrowid
