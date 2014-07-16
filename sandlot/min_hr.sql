ELECT v.*,
         1.0*hrs/batteds hr_rate,
         1.0*max_hrs/batteds max_hr_rate
    FROM (
  SELECT batter_id,
         MAX (batter_name) batter_name,
         COUNT (*) batteds,
         SUM (is_hr) hrs,
         SUM (max_hr) max_hrs
    FROM (
  SELECT t.*,
         CASE WHEN theta_bin = 0 AND r >= 304.2 THEN 1
              WHEN theta_bin = 1 AND r >= 326.0 THEN 1
              WHEN theta_bin = 2 AND r >= 333.4 THEN 1
              WHEN theta_bin = 3 AND r >= 333.3 THEN 1
              WHEN theta_bin = 4 AND r >= 339.6 THEN 1
              WHEN theta_bin = 5 AND r >= 346.3 THEN 1
              WHEN theta_bin = 6 AND r >= 349.7 THEN 1
              WHEN theta_bin = 7 AND r >= 358.2 THEN 1
              WHEN theta_bin = 8 AND r >= 356.2 THEN 1
              WHEN theta_bin = 9 AND r >= 360.6 THEN 1
              WHEN theta_bin = 10 AND r >= 365.7 THEN 1
              WHEN theta_bin = 11 AND r >= 369.7 THEN 1
              WHEN theta_bin = 12 AND r >= 360.1 THEN 1
              WHEN theta_bin = 13 AND r >= 379.2 THEN 1
              WHEN theta_bin = 14 AND r >= 374.3 THEN 1
              WHEN theta_bin = 15 AND r >= 388.1 THEN 1
              WHEN theta_bin = 16 AND r >= 398.7 THEN 1
              WHEN theta_bin = 17 AND r >= 395.3 THEN 1
              WHEN theta_bin = 18 AND r >= 385.7 THEN 1
              WHEN theta_bin = 19 AND r >= 382.9 THEN 1
              WHEN theta_bin = 20 AND r >= 385.7 THEN 1
              WHEN theta_bin = 21 AND r >= 382.4 THEN 1
              WHEN theta_bin = 22 AND r >= 373.8 THEN 1
              WHEN theta_bin = 23 AND r >= 322.4 THEN 1
              WHEN theta_bin = 24 AND r >= 360.3 THEN 1
              WHEN theta_bin = 25 AND r >= 353.6 THEN 1
              WHEN theta_bin = 26 AND r >= 344.7 THEN 1
              WHEN theta_bin = 27 AND r >= 341.6 THEN 1
              WHEN theta_bin = 28 AND r >= 336.7 THEN 1
              WHEN theta_bin = 29 AND r >= 332.1 THEN 1
              WHEN theta_bin = 30 AND r >= 324.1 THEN 1
              WHEN theta_bin = 31 AND r >= 322.8 THEN 1
              WHEN theta_bin = 32 AND r >= 320.3 THEN 1
              WHEN theta_bin = 33 AND r >= 326.3 THEN 1
              WHEN theta_bin = 34 AND r >= 323.3 THEN 1
              WHEN theta_bin = 35 AND r >= 314.7 THEN 1
              ELSE 0
         END max_hr,
         CASE WHEN description = 'Home Run' THEN 1 ELSE 0 END is_hr
    FROM (
  SELECT batted_ball.*,
         game_player.first_name || ' ' || game_player.last_name batter_name,
         CASE WHEN theta >= 45.0 AND theta < 47.5 THEN 0
              WHEN theta >= 47.5 AND theta < 50.0 THEN 1
              WHEN theta >= 50.0 AND theta < 52.5 THEN 2
              WHEN theta >= 52.5 AND theta < 55.0 THEN 3
              WHEN theta >= 55.0 AND theta < 57.5 THEN 4
              WHEN theta >= 57.5 AND theta < 60.0 THEN 5
              WHEN theta >= 60.0 AND theta < 62.5 THEN 6
              WHEN theta >= 62.5 AND theta < 65.0 THEN 7
              WHEN theta >= 65.0 AND theta < 67.5 THEN 8
              WHEN theta >= 67.5 AND theta < 70.0 THEN 9
              WHEN theta >= 70.0 AND theta < 72.5 THEN 10
              WHEN theta >= 72.5 AND theta < 75.0 THEN 11
              WHEN theta >= 75.0 AND theta < 77.5 THEN 12
              WHEN theta >= 77.5 AND theta < 80.0 THEN 13
              WHEN theta >= 80.0 AND theta < 82.5 THEN 14
              WHEN theta >= 82.5 AND theta < 85.0 THEN 15
              WHEN theta >= 85.0 AND theta < 87.5 THEN 16
              WHEN theta >= 87.5 AND theta < 90.0 THEN 17
              WHEN theta >= 90.0 AND theta < 92.5 THEN 18
              WHEN theta >= 92.5 AND theta < 95.0 THEN 19
              WHEN theta >= 95.0 AND theta < 97.5 THEN 20
              WHEN theta >= 97.5 AND theta < 100.0 THEN 21
              WHEN theta >= 100.0 AND theta < 102.5 THEN 22
              WHEN theta >= 102.5 AND theta < 105.0 THEN 23
              WHEN theta >= 105.0 AND theta < 107.5 THEN 24
              WHEN theta >= 107.5 AND theta < 110.0 THEN 25
              WHEN theta >= 110.0 AND theta < 112.5 THEN 26
              WHEN theta >= 112.5 AND theta < 115.0 THEN 27
              WHEN theta >= 115.0 AND theta < 117.5 THEN 28
              WHEN theta >= 117.5 AND theta < 120.0 THEN 29
              WHEN theta >= 120.0 AND theta < 122.5 THEN 30
              WHEN theta >= 122.5 AND theta < 125.0 THEN 31
              WHEN theta >= 125.0 AND theta < 127.5 THEN 32
              WHEN theta >= 127.5 AND theta < 130.0 THEN 33
              WHEN theta >= 130.0 AND theta < 132.5 THEN 34
              WHEN theta >= 132.5 AND theta < 135.0 THEN 35
              ELSE NULL
         END theta_bin
    FROM batted_ball,
         game_player,
         game
   WHERE batted_ball.batter_id = game_player.player_id
     AND batted_ball.game_id = game_player.game_id
     AND game_player.game_id = game.game_id
     AND (batted_ball.x != 0 OR batted_ball.y != 0)
     AND batted_ball.description != 'Error'
     AND batted_ball.description NOT LIKE '%nterference'
     AND DATE (game.date_str) >= DATE ('2014-01-01')
         ) t
         ) u
GROUP BY batter_id
         ) v
   WHERE batteds >= 100
ORDER BY 1.0*max_hrs/batteds DESC
;
