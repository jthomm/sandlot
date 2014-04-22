--enable foreign key support for the session
PRAGMA foreign_keys = ON;

  DELETE
    FROM pitch_cat
;

  INSERT
    INTO pitch_cat
  SELECT 'FF' pitch_type, 1  cat_a, 1 cat_b UNION ALL
  SELECT 'FT' pitch_type, 2  cat_a, 2 cat_b UNION ALL
  SELECT 'SI' pitch_type, 3  cat_a, 2 cat_b UNION ALL
  SELECT 'FA' pitch_type, 4  cat_a, 3 cat_b UNION ALL
  SELECT 'CH' pitch_type, 5  cat_a, 4 cat_b UNION ALL
  SELECT 'FS' pitch_type, 6  cat_a, 4 cat_b UNION ALL
  SELECT 'FC' pitch_type, 7  cat_a, 5 cat_b UNION ALL
  SELECT 'SL' pitch_type, 8  cat_a, 5 cat_b UNION ALL
  SELECT 'SC' pitch_type, 9  cat_a, 6 cat_b UNION ALL
  SELECT 'KC' pitch_type, 10 cat_a, 6 cat_b UNION ALL
  SELECT 'CU' pitch_type, 11 cat_a, 6 cat_b UNION ALL
  SELECT 'KN' pitch_type, 12 cat_a, 7 cat_b UNION ALL
  SELECT 'EP' pitch_type, 13 cat_a, 8 cat_b
;
