def game_values(gameday_id, game):
    return (
        gameday_id
      , game['venue']
      , game['date_str']
      , game['away']['abbr']
      , game['away']['full_name']
      , game['home']['abbr']
      , game['home']['full_name']
    )

def inning_values(game_id, inning):
    return (
        inning['number']
      , game_id
    )

def at_bat_values(inning_id, at_bat, side, team_abbr):
    return (
        at_bat['description']
      , at_bat['event']
      , at_bat['number']
      , at_bat['timestamp']
      , at_bat['balls']
      , at_bat['strikes']
      , at_bat['outs']
      , at_bat['batter_id']
      , at_bat['batter_stance']
      , at_bat['pitcher_id']
      , at_bat['pitcher_hand']
      , inning_id
      , side
      , team_abbr
    )

def pitch_values(at_bat_id, pitch):
    return (
        pitch['description']
      , pitch['cc']
      , pitch['pitch_id']
      , pitch['timestamp']
      , pitch['pitch_type']
      , pitch['type_confidence']
      , pitch['zone']
      , pitch['nasty']
      , pitch['result']
      , pitch['x']
      , pitch['y']
      , pitch['start_speed']
      , pitch['end_speed']
      , pitch['pfx_x']
      , pitch['pfx_z']
      , pitch['px']
      , pitch['pz']
      , pitch['sv_id']
      , pitch['x0']
      , pitch['y0']
      , pitch['z0']
      , pitch['vx0']
      , pitch['vy0']
      , pitch['vz0']
      , pitch['ax']
      , pitch['ay']
      , pitch['az']
      , pitch['spin_dir']
      , pitch['spin_rate']
      , pitch['break_y']
      , pitch['break_angle']
      , pitch['break_length']
      , at_bat_id # at_bat rowid
    )

def foo():
    pass

'''
INSERT INTO game (
    gameday_id
  , venue_name
  , date_str
  , away_abbr
  , away_full
  , home_abbr
  , home_full
) VALUES (?, ?, ?, ?, ?, ?, ?)

INSERT INTO inning (
    inning_num
  , game_id
) VALUES (?, ?)

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
  , inning_id
  , side
  , team_abbr
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

INSERT INTO pitch (
    description
  , commentary
  , pitch_num
  , timestamp
  , pitch_type
  , confidence
  , zone_num
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
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
'''
