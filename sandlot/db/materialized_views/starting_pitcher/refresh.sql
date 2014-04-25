--enable foreign key support for the session
PRAGMA foreign_keys = ON;

  DELETE
    FROM starting_pitcher
;

  INSERT
    INTO starting_pitcher (pitcher_id,
                           game_id,
                           side)
  SELECT t.pitcher_id,
         u.game_id,
         u.side
    FROM at_bat t,
         (
  SELECT MIN (at_bat_num) at_bat_num,
         game_id,
         CASE inning_side WHEN 'top' THEN 'home' ELSE 'away' END side
    FROM at_bat
   WHERE inning_num = 1
GROUP BY game_id,
         inning_side
         ) u
   WHERE t.game_id = u.game_id
     AND t.at_bat_num = u.at_bat_num
;
