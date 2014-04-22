--enable foreign key support for the session
PRAGMA foreign_keys = ON;

CREATE TABLE pitch_cat (
    pitch_type TEXT PRIMARY KEY
  , cat_a INTEGER
  , cat_b INTEGER
)
;
