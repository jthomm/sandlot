--enable foreign key support for the session
PRAGMA foreign_keys = ON;

--[game]
CREATE TABLE game (
    game_id    TEXT PRIMARY KEY
  , venue_name TEXT --`venue`
  , date_str   TEXT --`date_string`
  , away_abbr  TEXT --`away`, `abbr`
  , away_full  TEXT --`away`, `full_name`
  , home_abbr  TEXT --`home`, `abbr`
  , home_full  TEXT --`home`, `full_name`
)
;

--[game > at_bat]
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
  , inning_num  INTEGER
  , inning_side TEXT
  , game_id     TEXT
  , FOREIGN KEY (batter_id, game_id) REFERENCES game_player (player_id, game_id)
  , FOREIGN KEY (pitcher_id, game_id) REFERENCES game_player (player_id, game_id)
  , FOREIGN KEY (game_id) REFERENCES game (game_id)
)
;

--[game > action]
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
  , inning_num  INTEGER
  , inning_side TEXT
  , game_id     TEXT
  , FOREIGN KEY (game_id) REFERENCES game (game_id)
)
;

--[game > batted_ball]
CREATE TABLE batted_ball (
    batted_ball_id INTEGER PRIMARY KEY
  , description    TEXT  --`description`
  , x              FLOAT --`x`
  , y              FLOAT --`y`
  , r              FLOAT --`r`
  , theta          FLOAT --`theta`
  , batter_id      TEXT  --`batter_id`
  , pitcher_id     TEXT  --`pitcher_id`
  , result         TEXT  --`result`
  , team           TEXT  --`team`
  , inning_num     TEXT  --`inning`
  , game_id        TEXT
  , FOREIGN KEY (batter_id, game_id) REFERENCES game_player (player_id, game_id)
  , FOREIGN KEY (pitcher_id, game_id) REFERENCES game_player (player_id, game_id)
  , FOREIGN KEY (game_id) REFERENCES game (game_id)
)
;

--[game > at_bat > pitch]
CREATE TABLE pitch (
    pitch_id     INTEGER PRIMARY KEY
  , description  TEXT    --`description`
  , commentary   TEXT    --`cc`
  , pitch_num    INTEGER --`pitch_id`
  , timestamp    TEXT    --`timestamp`
  , pitch_type   TEXT    --`pitch_type`
  , confidence   FLOAT   --`type_confidence`
  , zone_num     INTEGER --`zone`
  , sz_top       INTEGER --`sz_top`
  , sz_bot       INTEGER --`sz_bot`
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
  , FOREIGN KEY (at_bat_id) REFERENCES at_bat (at_bat_id)
)
;

--[game > at_bat > runner]
CREATE TABLE runner (
    runner_id   INTEGER PRIMARY KEY
  , player_id   TEXT --`runner_id`
  , start_base  TEXT --`start`
  , end_base    TEXT --`end`
  , event_type  TEXT --`event`
  , at_bat_id   INTEGER
  , FOREIGN KEY (at_bat_id) REFERENCES at_bat (at_bat_id)
)
;

--[game > game_umpire]
CREATE TABLE game_umpire (
    umpire_id      TEXT --`umpire_id`
  , full_name      TEXT --`full_name`
  , position       TEXT --`position`
  , game_id        INTEGER
  , FOREIGN KEY (game_id) REFERENCES game (game_id)
  , PRIMARY KEY (umpire_id, game_id)
)
;

--[game > game_player]
CREATE TABLE game_player (
    player_id      TEXT --`player_id`
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
  , game_id        TEXT
  , FOREIGN KEY (game_id) REFERENCES game (game_id)
  , PRIMARY KEY (player_id, game_id)
)
;

--[game > game_coach]
CREATE TABLE game_coach (
    coach_id   TEXT --`coach_id`
  , first_name TEXT --`first_name`
  , last_name  TEXT --`last_name`
  , team_abbr  TEXT
  , status     TEXT
  , uni_number INTEGER --`uniform_number`
  , position   TEXT --`position`
  , game_id    TEXT
  , FOREIGN KEY (game_id) REFERENCES game (game_id)
  , PRIMARY KEY (coach_id, game_id)
)
;
