  DROP VIEW v_at_bat_error;
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

  DROP VIEW v_at_bat_bunt;
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

  DROP VIEW v_at_bat_strikeout;
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

  DROP VIEW v_at_bat_pa;
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
