--enable foreign key support for the session
PRAGMA foreign_keys = ON;

  DELETE
    FROM starting_pitcher
   WHERE game_id = ?
;
