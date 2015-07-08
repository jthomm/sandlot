  --DROP VIEW v_pitch_result;
  CREATE VIEW v_pitch_result AS
  SELECT pitch.pitch_id,
         CASE WHEN (   (    pitch.result_code = 'X'
                        AND at_bat.description LIKE '%bunt%')
                    OR pitch.description IN ('Foul Bunt',
                                             'Missed Bunt'))      THEN 'BUNT'
              WHEN (   pitch.result_code = 'X'
                    OR pitch.description LIKE 'Foul%'
                    OR pitch.description LIKE 'Swinging%')        THEN 'SWING'
              WHEN (   pitch.description IN ('Called Strike',
                                             'Ball In Dirt',
                                             'Intent Ball',
                                             'Pitchout',
                                             'Hit By Pitch')
                    OR pitch.description LIKE 'Ball%')            THEN 'LOOK'
                                                                  ELSE 'OTHER'
         END AS reaction,
         CASE 
              WHEN pitch.result_code = 'X'
               AND (   at_bat.description LIKE '%bunt%'
                    OR at_bat.description LIKE '%ground ball%'
                    OR at_bat.description LIKE '%grounds out%'
                    OR at_bat.description LIKE '%grounds into%') THEN 'GROUND'
              WHEN pitch.result_code = 'X'
               AND at_bat.event_type = 'Field Error'             THEN 'ERROR'
              WHEN pitch.result_code = 'X'
               AND at_bat.event_type IN ('Fielders Choice',
                                         'Fielders Choice Out')  THEN 'CHOICE'
              WHEN pitch.result_code = 'X'
               AND at_bat.event_type IN ('Fan Interference',
                                         'Fan interference',
                                         'Catcher Interference',
                                         'Batter Interference')  THEN 'INTER'
              WHEN pitch.result_code = 'X'                       THEN 'AIR'
              
              
              WHEN pitch.description LIKE 'Foul%'                THEN 'FOUL'
              
              WHEN (   pitch.description = 'Called Strike'
                    OR pitch.description = 'Missed Bunt'
                    OR pitch.description LIKE 'Swinging%'
                    OR pitch.result_code = 'S')                  THEN 'STRIKE'
              
              WHEN (   pitch.description LIKE 'Ball%'
                    OR pitch.description IN ('Ball In Dirt',
                                             'Intent Ball',
                                             'Pitchout',
                                             'Hit By Pitch')
                    OR pitch.result_code = 'B')                  THEN 'BALL'
         END AS result
    FROM at_bat,
         pitch
   WHERE at_bat.at_bat_id = pitch.at_bat_id
;



  --DROP VIEW v_at_bat_bunt;
  CREATE VIEW v_at_bat_bunt AS
  SELECT at_bat.at_bat_id,
         CASE WHEN (   at_bat.description LIKE '%bunt ground ball to%'
                    OR at_bat.description LIKE '%bunt grounds out%'
                    OR at_bat.description LIKE '%ground bunts into%')
              THEN 'Grounder'
              WHEN (   at_bat.description LIKE '%bunt line drive to%'
                    OR at_bat.description LIKE '%bunt lines out%'
                    OR at_bat.description LIKE '%bunt lines into%')
              THEN 'Liner'
              WHEN (   at_bat.description LIKE '%bunt pop to%'
                    OR at_bat.description LIKE '%bunt pops out%'
                    OR at_bat.description LIKE '%bunt pops into%')
              THEN 'Popup'
              WHEN (    at_bat.description LIKE '%strikes out on%'
                    AND at_bat.description LIKE '%missed bunt%')
              THEN 'Strikeout (miss)'
              WHEN (    at_bat.description LIKE '%strikes out on%'
                    AND at_bat.description LIKE '%foul bunt%')
              THEN 'Strikeout (foul)'
              ELSE 'Unknown (sacrifice)'
         END bunt
    FROM at_bat
   WHERE at_bat.description LIKE '%bunt%'
;



  --DROP VIEW v_at_bat_error;
  CREATE VIEW v_at_bat_error AS
  SELECT at_bat.at_bat_id,
         CASE WHEN at_bat.description LIKE '%fielding error%'     THEN 'Fielding'
              WHEN at_bat.description LIKE '%throwing error%'     THEN 'Throwing'
              WHEN at_bat.description LIKE '%missed catch error%' THEN 'Catching'
              ELSE 'Other'
         END category,
         CASE WHEN at_bat.description LIKE '%by pitcher%'         THEN 1
              WHEN at_bat.description LIKE '%by catcher%'         THEN 2
              WHEN at_bat.description LIKE '%by first baseman%'   THEN 3
              WHEN at_bat.description LIKE '%by second baseman%'  THEN 4
              WHEN at_bat.description LIKE '%by shortstop%'       THEN 6
              WHEN at_bat.description LIKE '%by third baseman%'   THEN 5
              WHEN at_bat.description LIKE '%by left fielder%'    THEN 7
              WHEN at_bat.description LIKE '%by center fielder%'  THEN 8
              WHEN at_bat.description LIKE '%by right fielder%'   THEN 9
         END position
    FROM at_bat
   WHERE at_bat.event_type = 'Field Error'
;



  --DROP VIEW v_at_bat_strikeout;
  CREATE VIEW v_at_bat_strikeout AS
  SELECT at_bat.at_bat_id,
         CASE WHEN at_bat.description LIKE '%strikes out swinging%'
              THEN 'Swinging'
              WHEN at_bat.description LIKE '%called out on strikes%'
              THEN 'Looking'
              WHEN (    at_bat.description LIKE '%strikes out on%'
                    AND at_bat.description LIKE '%missed bunt%')
              THEN 'Missed Bunt'
              WHEN (    at_bat.description LIKE '%strikes out on%'
                    AND at_bat.description LIKE '%foul bunt%')
              THEN 'Foul Bunt'
              WHEN (    at_bat.description LIKE '%strikes out on%'
                    AND at_bat.description LIKE '%foul tip%')
              THEN 'Foul Tip'
              ELSE 'Unknown'
         END strikeout
    FROM at_bat
   WHERE at_bat.event_type IN ('Strikeout', 'Strikeout - DP')
      OR (    at_bat.event_type = 'Batter Interference'
          AND (   at_bat.description LIKE '%strikes out%'
               OR at_bat.description LIKE '%called out on strikes%'))
;



  --DROP VIEW v_at_bat_pa;
  CREATE VIEW v_at_bat_pa AS
  SELECT at_bat.at_bat_id,
         CASE WHEN at_bat.event_type IN ('Walk',
                                         'Intent Walk',
                                         'Hit By Pitch',
                                         'Runner Out',
                                         'Catcher Interference')
              THEN at_bat.event_type

              WHEN v_at_bat_bunt.at_bat_id IS NOT NULL
              THEN 'Bunt ' || v_at_bat_bunt.bunt

              WHEN v_at_bat_strikeout.at_bat_id IS NOT NULL
              THEN 'Strikeout ' || v_at_bat_strikeout.strikeout

              WHEN (   at_bat.description LIKE '%ground ball%'
                    OR at_bat.description LIKE '%grounds out%'
                    OR at_bat.description LIKE '%grounds into%')
              THEN 'Grounder'

              WHEN (   at_bat.description LIKE '%line drive%'
                    OR at_bat.description LIKE '%lines out%'
                    OR at_bat.description LIKE '%lines into%')
              THEN 'Liner'

              WHEN (   at_bat.description LIKE '%sacrifice fly%'
                    OR at_bat.description LIKE '%fly ball%'
                    OR at_bat.description LIKE '%flies out%'
                    OR at_bat.description LIKE '%flies into%')
              THEN 'Fly Ball'

              WHEN (   at_bat.description LIKE '%pop up%'
                    OR at_bat.description LIKE '%pops out%'
                    OR at_bat.description LIKE '%pops into%')
              THEN 'Popup'

              WHEN at_bat.description LIKE '%grand slam%'
              THEN 'Air Ball (home run)'

              WHEN at_bat.event_type = 'Fan interference'
              THEN 'Air Ball (interference)'

              WHEN (    v_at_bat_error.category = 'Fielding'
                    AND v_at_bat_error.position >= 7)
              THEN 'Air Ball (error)'

              WHEN (    v_at_bat_error.category = 'Fielding'
                    AND v_at_bat_error.position <= 6)
              THEN 'Grounder (error)'

              WHEN (    v_at_bat_error.category = 'Throwing'
                    AND v_at_bat_error.position <= 6)
              THEN 'Grounder (error)'

              WHEN v_at_bat_error.at_bat_id IS NOT NULL
              THEN 'Unknown (error)'

              WHEN (   at_bat.event_type IN ('Fielders Choice', 'Fielders Choice Out')
                    OR at_bat.description LIKE "%fielder's choice%")
              THEN 'Grounder (fc)'

         END pa
    FROM at_bat
    LEFT JOIN v_at_bat_bunt      ON at_bat.at_bat_id = v_at_bat_bunt.at_bat_id
    LEFT JOIN v_at_bat_error     ON at_bat.at_bat_id = v_at_bat_error.at_bat_id
    LEFT JOIN v_at_bat_strikeout ON at_bat.at_bat_id = v_at_bat_strikeout.at_bat_id
;



  --DROP VIEW v_pitch_category;
  CREATE VIEW v_pitch_category AS
  SELECT pitch.pitch_id,
         CASE WHEN pitch.pitch_type = 'FF'                THEN 1
              WHEN pitch.pitch_type IN ('FT', 'SI')       THEN 2
              WHEN pitch.pitch_type = 'FA'                THEN 3
              WHEN pitch.pitch_type IN ('CH', 'FS')       THEN 4
              WHEN pitch.pitch_type IN ('FC', 'SL')       THEN 5
              WHEN pitch.pitch_type IN ('SC', 'KC', 'CU') THEN 6
              WHEN pitch.pitch_type = 'KN'                THEN 7
              WHEN pitch.pitch_type = 'EP'                THEN 8
                                                          ELSE NULL
         END AS cat_a,
         CASE pitch.pitch_type
              WHEN 'FF' THEN 1
              WHEN 'FT' THEN 2
              WHEN 'SI' THEN 3
              WHEN 'FA' THEN 4
              WHEN 'CH' THEN 5
              WHEN 'FS' THEN 6
              WHEN 'FC' THEN 7
              WHEN 'SL' THEN 8
              WHEN 'SC' THEN 9
              WHEN 'KC' THEN 10
              WHEN 'CU' THEN 11
              WHEN 'KN' THEN 12
              WHEN 'EP' THEN 13
         END AS cat_b
    FROM pitch
;



  --DROP VIEW v_min_hr;
  CREATE VIEW v_min_hr AS
  SELECT batted_ball.batted_ball_id,
         CASE WHEN (   (batted_ball.x = 0 AND batted_ball.y = 0)
                    OR batted_ball.description = 'Error'
                    OR batted_ball.description LIKE '%nterference')
              THEN NULL
              WHEN theta >= 45.0  AND theta < 47.5  AND r >= 304.2 THEN 1
              WHEN theta >= 47.5  AND theta < 50.0  AND r >= 326.0 THEN 1
              WHEN theta >= 50.0  AND theta < 52.5  AND r >= 333.4 THEN 1
              WHEN theta >= 52.5  AND theta < 55.0  AND r >= 333.3 THEN 1
              WHEN theta >= 55.0  AND theta < 57.5  AND r >= 339.6 THEN 1
              WHEN theta >= 57.5  AND theta < 60.0  AND r >= 346.3 THEN 1
              WHEN theta >= 60.0  AND theta < 62.5  AND r >= 349.7 THEN 1
              WHEN theta >= 62.5  AND theta < 65.0  AND r >= 358.2 THEN 1
              WHEN theta >= 65.0  AND theta < 67.5  AND r >= 356.2 THEN 1
              WHEN theta >= 67.5  AND theta < 70.0  AND r >= 360.6 THEN 1
              WHEN theta >= 70.0  AND theta < 72.5  AND r >= 365.7 THEN 1
              WHEN theta >= 72.5  AND theta < 75.0  AND r >= 369.7 THEN 1
              WHEN theta >= 75.0  AND theta < 77.5  AND r >= 360.1 THEN 1
              WHEN theta >= 77.5  AND theta < 80.0  AND r >= 379.2 THEN 1
              WHEN theta >= 80.0  AND theta < 82.5  AND r >= 374.3 THEN 1
              WHEN theta >= 82.5  AND theta < 85.0  AND r >= 388.1 THEN 1
              WHEN theta >= 85.0  AND theta < 87.5  AND r >= 398.7 THEN 1
              WHEN theta >= 87.5  AND theta < 90.0  AND r >= 395.3 THEN 1
              WHEN theta >= 90.0  AND theta < 92.5  AND r >= 385.7 THEN 1
              WHEN theta >= 92.5  AND theta < 95.0  AND r >= 382.9 THEN 1
              WHEN theta >= 95.0  AND theta < 97.5  AND r >= 385.7 THEN 1
              WHEN theta >= 97.5  AND theta < 100.0 AND r >= 382.4 THEN 1
              WHEN theta >= 100.0 AND theta < 102.5 AND r >= 373.8 THEN 1
              WHEN theta >= 102.5 AND theta < 105.0 AND r >= 322.4 THEN 1
              WHEN theta >= 105.0 AND theta < 107.5 AND r >= 360.3 THEN 1
              WHEN theta >= 107.5 AND theta < 110.0 AND r >= 353.6 THEN 1
              WHEN theta >= 110.0 AND theta < 112.5 AND r >= 344.7 THEN 1
              WHEN theta >= 112.5 AND theta < 115.0 AND r >= 341.6 THEN 1
              WHEN theta >= 115.0 AND theta < 117.5 AND r >= 336.7 THEN 1
              WHEN theta >= 117.5 AND theta < 120.0 AND r >= 332.1 THEN 1
              WHEN theta >= 120.0 AND theta < 122.5 AND r >= 324.1 THEN 1
              WHEN theta >= 122.5 AND theta < 125.0 AND r >= 322.8 THEN 1
              WHEN theta >= 125.0 AND theta < 127.5 AND r >= 320.3 THEN 1
              WHEN theta >= 127.5 AND theta < 130.0 AND r >= 326.3 THEN 1
              WHEN theta >= 130.0 AND theta < 132.5 AND r >= 323.3 THEN 1
              WHEN theta >= 132.5 AND theta < 135.0 AND r >= 314.7 THEN 1
                                                                   ELSE 0
         END AS is_hr
    FROM batted_ball
;



CREATE TABLE pitch_end (
    pitch_id     INTEGER PRIMARY KEY
  , t            FLOAT
  , vx_end       FLOAT
  , vy_end       FLOAT
  , vz_end       FLOAT
  , FOREIGN KEY (pitch_id) REFERENCES pitch (pitch_id)
)
;



  --DROP VIEW v_pitch_zone;
  CREATE VIEW v_pitch_zone AS
  SELECT pitch.pitch_id,
         CASE WHEN at_bat.batter_stnd = 'R'
               AND ((pitch.pfx_end_x + 0.04167)*(pitch.pfx_end_x + 0.04167)/1.17361) + ((pitch.pfx_end_z - 2.52083)*(pitch.pfx_end_z - 2.52083)/0.95877) <= 1
              THEN 1
              WHEN at_bat.batter_stnd = 'L'
               AND ((pitch.pfx_end_x + 0.22918)*(pitch.pfx_end_x + 0.22918)/1.12891) + ((pitch.pfx_end_z - 2.50000)*(pitch.pfx_end_z - 2.50000)/0.91840) <= 1
              THEN 1
              ELSE 0
         END AS end_zone,
         CASE WHEN at_bat.batter_stnd = 'R'
               AND ((pitch.pfx_end_x - pitch.mvt_x/12.0 + 0.04167)*(pitch.pfx_end_x - pitch.mvt_x/12.0 + 0.04167)/1.17361) + ((pitch.pfx_end_z - pitch.mvt_z/12.0 - 2.52083)*(pitch.pfx_end_z - pitch.mvt_z/12.0 - 2.52083)/0.95877) <= 1
              THEN 1
              WHEN at_bat.batter_stnd = 'L'
               AND ((pitch.pfx_end_x - pitch.mvt_x/12.0 + 0.22918)*(pitch.pfx_end_x - pitch.mvt_x/12.0 + 0.22918)/1.12891) + ((pitch.pfx_end_z - pitch.mvt_z/12.0 - 2.50000)*(pitch.pfx_end_z - pitch.mvt_z/12.0 - 2.50000)/0.91840) <= 1
              THEN 1
              ELSE 0
         END AS brk_zone
    FROM pitch,
         at_bat
   WHERE pitch.at_bat_id = at_bat.at_bat_id
;
