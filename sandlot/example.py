from lxml import etree

game_id = 'gid_2013_04_29_minmlb_detmlb_1'
#game_id = 'gid_2013_04_30_nynmlb_miamlb_1'

def get_root(game_id):
    file_name = '{game_id}.xml'.format(game_id=game_id)
    with open(file_name, 'rb') as f:
        xml_string = f.read()
        xml_unicode = unicode(xml_string, 'Latin-1')
        return etree.fromstring(xml_unicode)



from inning import Inning

innings = [Inning(child).as_dict for child in root]


import simplejson as json

json_string = json.dumps(innings, indent=2)

with open(u'%s.json' % game_id, 'wb') as f: f.write(json_string)




from collections import OrderedDict

rows = list()

for inning in innings:
    for side in ('top', 'bottom',):
        for at_bat in inning[side]['at_bats']:
            dct = OrderedDict()
            dct['inning'] = inning['number']
            dct['side'] = side
            dct['balls'] = at_bat['balls']
            dct['strikes'] = at_bat['strikes']
            dct['outs'] = at_bat['outs']
            dct['timestamp'] = at_bat['timestamp']
            dct['batter_id'] = at_bat['batter_id']
            dct['batter_stance'] = at_bat['batter_stance']
            dct['pitcher_id'] = at_bat['pitcher_id']
            dct['pitcher_hand'] = at_bat['pitcher_hand']
            dct['description'] = at_bat['description']
            dct['event'] = at_bat['event']
            runners_before = [r['start'] for r in at_bat['runners'] \
                              if r['start'] != u'']
            runners_before.sort()
            dct['runners'] = u','.join(runners_before)
            dct['foul_balls'] = len([pitch for pitch in at_bat['pitches'] \
                                     if 'Foul' in pitch['description']])
            final_pitch = at_bat['pitches'][-1]
            dct['fp_desc'] = final_pitch['description']
            dct['fp_comm'] = final_pitch['cc']
            dct['fp_type'] = final_pitch['pitch_type']
            dct['fp_nasty'] = final_pitch['nasty']
            dct['total_pitches'] = len(at_bat['pitches'])
            dct['total_nasty'] = sum([p['nasty'] for p in at_bat['pitches']])
            rows.append(dct)

with open('foo.csv', 'wb') as f:
    headers = rows[0].keys()
    import csv
    w = csv.writer(f, quoting=csv.QUOTE_MINIMAL, delimiter=',')
    w.writerow(headers)
    w.writerows([r.values() for r in rows])
