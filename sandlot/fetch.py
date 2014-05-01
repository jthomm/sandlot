from bs4 import BeautifulSoup as BS
from urllib2 import urlopen, HTTPError
import gzip
from time import sleep


class GameDay(object):
#
    def __init__(self, date):
        self.date = date
#
    @property
    def url(self):
        year = unicode(self.date.year)
        month = unicode(self.date.month).zfill(2)
        day = unicode(self.date.day).zfill(2)
        return u'http://gdx.mlb.com/components/game/mlb/year_{year}/month_{month}/day_{day}/'.format(year=year, month=month, day=day)
#
    @property
    def game_ids(self):
        soup = BS(urlopen(self.url).read())
        return [unicode(a.attrs['href'])[:-1] for a in soup.find_all('a') \
                if a is not None and a.attrs.get('href', '').startswith('gid_')]



class GameResource(object):
#
    def __init__(self, game_id, game_day):
        self.game_id = game_id
        self.game_day = game_day
#
    @property
    def base_url(self):
        return self.game_day.url + self.game_id
#
    @property
    def inning_all_url(self):
        return self.base_url + '/inning/inning_all.xml'
#
    @property
    def inning_hit_url(self):
        return self.base_url + '/inning/inning_hit.xml'
#
    @property
    def players_url(self):
        return self.base_url + '/players.xml'



class XMLResource(object):
#
    def __init__(self, url):
        self.url = url
#
    @property
    def response_string(self):
        return urlopen(self.url).read()
#
    def save(self, file_name):
        response_string = self.response_string
        with gzip.open(file_name, 'wb') as f:
            f.write(response_string)



#from os import listdir
#for date in sorted(list(set(f[4:14] for f in listdir('./xml/2014/')))): date

import datetime

one_day = datetime.timedelta(days=1)

start = datetime.date(2014, 4, 30)
until = datetime.date(2014, 5, 1)

while start < until:
    print start
    print '=================================================='
    game_day = GameDay(start)
    for game_id in game_day.game_ids:
        print 'Fetching data for %s' % game_id
        gr = GameResource(game_id, game_day)
        inning_all = XMLResource(gr.inning_all_url)
        try:
            inning_all.save('./xml/2014/%s-inning_all.xml.gz' % game_id)
        except HTTPError:
            print 'WARNING:  No data for %s - skipping...\n' % game_id
            continue
        inning_hit = XMLResource(gr.inning_hit_url)
        inning_hit.save('./xml/2014/%s-inning_hit.xml.gz' % game_id)
        players = XMLResource(gr.players_url)
        players.save('./xml/2014/%s-players.xml.gz' % game_id)
        print 'Got it!\n'
    start += one_day
    print 'Sleeping...\n'
    sleep(10)
