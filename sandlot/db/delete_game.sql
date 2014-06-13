--enable foreign key support for the session
PRAGMA foreign_keys = ON;

  DELETE
    FROM pitch
   WHERE EXISTS (SELECT NULL
                   FROM at_bat
                  WHERE at_bat.game_id = ?
                    AND at_bat.at_bat_id = pitch.at_bat_id)
;

  DELETE
    FROM runner
   WHERE EXISTS (SELECT NULL
                   FROM at_bat
                  WHERE at_bat.game_id = ?
                    AND at_bat.at_bat_id = runner.at_bat_id)
;

  DELETE
    FROM starting_pitcher
   WHERE game_id = ?
;

  DELETE
    FROM action
   WHERE game_id = ?
;

  DELETE
    FROM at_bat
   WHERE game_id = ?
;

  DELETE
    FROM game_player
   WHERE game_id = ?
;

  DELETE
    FROM game_coach
   WHERE game_id = ?
;

  DELETE
    FROM game_umpire
   WHERE game_id = ?
;

  DELETE
    FROM game
   WHERE game_id = ?
;
