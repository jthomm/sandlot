--enable foreign key support for the session
PRAGMA foreign_keys = ON;

CREATE TABLE starting_pitcher (
    pitcher_id TEXT
  , game_id TEXT
  , side TEXT
  , FOREIGN KEY (pitcher_id, game_id) REFERENCES game_player (player_id, game_id)
  , PRIMARY KEY (pitcher_id, game_id, side)
)
;
