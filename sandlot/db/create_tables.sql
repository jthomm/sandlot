--enable foreign key support for the session
PRAGMA foreign_keys = ON;

--[game]
CREATE TABLE game (
    game_id    INTEGER PRIMARY KEY
  , gameday_id TEXT UNIQUE
  , venue_name TEXT --`venue`
  , date_str   TEXT --`date_string`
  , away_abbr  TEXT --`away`, `abbr`
  , away_full  TEXT --`away`, `full_name`
  , home_abbr  TEXT --`home`, `abbr`
  , home_full  TEXT --`home`, `full_name`
)
;

--[game > inning]
CREATE TABLE inning (
    inning_id  INTEGER PRIMARY KEY
  , inning_num INTEGER --`number`
  , game_id    INTEGER
  , FOREIGN KEY(game_id) REFERENCES game(game_id)
)
;

--[game > inning > at_bat]
CREATE TABLE at_bat (
    at_bat_id   INTEGER PRIMARY KEY
  , description TEXT    --`description`
  , event_type  TEXT    --`event`
  , at_bat_num  INTEGER --`number`
  , timestamp   TEXT    --`timestamp`
  , balls_aft   INTEGER --`balls`
  , strikes_aft INTEGER --`strikes`
  , outs_aft    INTEGER --`outs`
  , batter_id   TEXT    --`batter_id`
  , batter_stnd TEXT    --`batter_stance`
  , pitcher_id  TEXT    --`pitcher_id`
  , pitcher_hnd TEXT    --`pitcher_hand`
  , inning_id   INTEGER
  , side        TEXT
  , FOREIGN KEY(inning_id) REFERENCES inning(inning_id)
)
;

--[game > inning > action]
CREATE TABLE action (
    action_id   INTEGER PRIMARY KEY
  , description TEXT    --`description`
  , event_type  TEXT    --`event`
  , player_id   TEXT    --`player_id`
  , timestamp   TEXT    --`timestamp`
  , pitch_num   INTEGER --`pitch`
  , balls_bef   INTEGER --`balls`
  , strikes_bef INTEGER --`strikes`
  , outs_bef    INTEGER --`outs`
  , inning_id   INTEGER
  , side        TEXT
  , FOREIGN KEY(inning_id) REFERENCES inning(inning_id)
)
;

--[game > inning > at_bat > pitch]
CREATE TABLE pitch (
    pitch_id     INTEGER PRIMARY KEY
  , description  TEXT    --`description`
  , commentary   TEXT    --`cc`
  , pitch_num    INTEGER --`pitch_id`
  , timestamp    TEXT    --`timestamp`
  , pitch_type   TEXT    --`pitch_type`
  , confidence   FLOAT   --`type_confidence`
  , zone_num     INTEGER --`zone`
  , nastiness    INTEGER --`nasty`
  , result_code  TEXT    --`result`
  , gd_end_x     FLOAT   --`x`
  , gd_end_z     FLOAT   --`y`
  , start_speed  FLOAT   --`start_speed`
  , end_speed    FLOAT   --`end_speed`
  , mvt_x        FLOAT   --`pfx_x`
  , mvt_z        FLOAT   --`pfx_z`
  , pfx_end_x    FLOAT   --`px`
  , pfx_end_z    FLOAT   --`pz`
  , pfx_start_id TEXT    --`sv_id`
  , x_nought     FLOAT   --`x0`
  , y_nought     FLOAT   --`y0`
  , z_nought     FLOAT   --`z0`
  , vx_start     FLOAT   --`vx0`
  , vy_start     FLOAT   --`vy0`
  , vz_start     FLOAT   --`vz0`
  , ax_start     FLOAT   --`ax`
  , ay_start     FLOAT   --`ay`
  , az_start     FLOAT   --`az`
  , spin_angle   FLOAT   --`spin_dir`
  , spin_rate    FLOAT   --`spin_rate`
  , y_max_break  FLOAT   --`break_y`
  , break_angle  FLOAT   --`break_angle`
  , break_mag    FLOAT   --`break_length`
  , at_bat_id    INTEGER
  , FOREIGN KEY(at_bat_id) REFERENCES at_bat(at_bat_id)
)
;

--[game > inning > at_bat > runner]
CREATE TABLE runner (
    runner_id   INTEGER PRIMARY KEY
  , player_id   TEXT --`runner_id`
  , start_base  TEXT --`start`
  , end_base    TEXT --`end`
  , event_type  TEXT --`event`
  , at_bat_id   INTEGER
  , FOREIGN KEY(at_bat_id) REFERENCES at_bat(at_bat_id)
)
;

--[game > game_umpire]
CREATE TABLE game_umpire (
    game_umpire_id INTEGER PRIMARY KEY
  , umpire_id      TEXT --`umpire_id`
  , full_name      TEXT --`full_name`
  , position       TEXT --`position`
  , game_id        INTEGER
  , FOREIGN KEY(game_id) REFERENCES game(game_id)
)
;

--[game > game_player]
CREATE TABLE game_player (
    game_player_id INTEGER PRIMARY KEY
  , player_id      TEXT --`player_id`
  , first_name     TEXT --`first_name`
  , last_name      TEXT --`last_name`
  , box_name       TEXT --`box_name`
  , handedness     TEXT --`handedness`
  , team_id        TEXT --`team_id`
  , team_abbr      TEXT --`team_abbr`
  , status         TEXT --`status`
  , uni_number     INTEGER --`uniform_number`
  , position       TEXT --`position`
  , game_position  TEXT --`game_position`
  , curr_position  TEXT --`current_position`
  , batting_order  INTEGER --`batting_order`
  , avg            FLOAT --`avg`
  , rbi            INTEGER --`rbi`
  , hr             INTEGER --`hr`
  , wins           INTEGER --`wins`
  , losses         INTEGER --`losses`
  , era            FLOAT --`era`
  , game_id        INTEGER
  , FOREIGN KEY(game_id) REFERENCES game(game_id)
)
;

--[game > game_coach]
CREATE TABLE game_coach (
    game_coach_id INTEGER PRIMARY KEY
  , coach_id   TEXT --`coach_id`
  , first_name TEXT --`first_name`
  , last_name  TEXT --`last_name`
  , team_abbr  TEXT
  , status     TEXT
  , uni_number INTEGER --`uniform_number`
  , position   TEXT --`position`
  , game_id    INTEGER
  , FOREIGN KEY(game_id) REFERENCES game(game_id)
)
;
