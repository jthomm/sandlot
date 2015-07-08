sandlot
=======

A Python handler for the MLB Gameday API

#### A few good commands...

```sh
python fetch.py -s 20150611 -u 20150616
ls xml/2015/ | grep players | grep -v old | cut -d \- -f 1 | python insert.py
cat db/delete_game.sql | sed "s/?/'gid_2015_06_15_tormlb_nynmlb_1'/g" | pbcopy
```
