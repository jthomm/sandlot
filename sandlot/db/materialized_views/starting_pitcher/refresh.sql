--enable foreign key support for the session
PRAGMA foreign_keys = ON;

  DELETE
    FROM starting_pitcher
;

  INSERT
   INTO starting_pitcher (pitcher_id,
                          game_id,
                          side)
  SELECT MIN (pitcher_id) pitcher_id,
         game_id,
         CASE inning_side WHEN 'top' THEN 'home' ELSE 'away' END side
    FROM at_bat
   WHERE inning_num = 1
GROUP BY game_id,
         inning_side
;
