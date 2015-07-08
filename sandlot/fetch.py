from bs4 import BeautifulSoup as BS
from urllib2 import urlopen, HTTPError
import gzip
from time import sleep


class GameDay(object):

    def __init__(self, date):
        self.date = date

    @property
    def url(self):
        year = unicode(self.date.year)
        month = unicode(self.date.month).zfill(2)
        day = unicode(self.date.day).zfill(2)
        return u'http://gdx.mlb.com/components/game/mlb/year_{year}/month_{month}/day_{day}/'.format(year=year, month=month, day=day)

    @property
    def game_ids(self):
        soup = BS(urlopen(self.url).read())
        return [unicode(a.attrs['href'])[:-1] for a in soup.find_all('a') \
                if a is not None and a.attrs.get('href', '').startswith('gid_')]



class GameResource(object):

    def __init__(self, game_id, game_day):
        self.game_id = game_id
        self.game_day = game_day

    @property
    def base_url(self):
        return self.game_day.url + self.game_id

    @property
    def inning_all_url(self):
        return self.base_url + '/inning/inning_all.xml'

    @property
    def inning_hit_url(self):
        return self.base_url + '/inning/inning_hit.xml'

    @property
    def players_url(self):
        return self.base_url + '/players.xml'



class XMLResource(object):

    def __init__(self, url):
        self.url = url

    @property
    def response_string(self):
        return urlopen(self.url).read()

    def save(self, file_name):
        response_string = self.response_string
        with gzip.open(file_name, 'wb') as f:
            f.write(response_string)



def fetch_one_date(date):
    game_day = GameDay(date)
    data_dir = './xml/{0}'.format(date.year)
    for game_id in game_day.game_ids:
        print 'Fetching data for %s' % game_id
        gr = GameResource(game_id, game_day)
        inning_all = XMLResource(gr.inning_all_url)
        try:
            inning_all.save('{0}/{1}-inning_all.xml.gz'.format(data_dir, game_id))
        except HTTPError:
            print 'WARNING:  No data for %s - skipping...\n' % game_id
            continue
        inning_hit = XMLResource(gr.inning_hit_url)
        inning_hit.save('{0}/{1}-inning_hit.xml.gz'.format(data_dir, game_id))
        players = XMLResource(gr.players_url)
        players.save('{0}/{1}-players.xml.gz'.format(data_dir, game_id))
        print 'Got it!\n'



import datetime

one_day = datetime.timedelta(days=1)

def fetch_multiple_dates(start, until):
    while start < until:
        print start
        print '=================================================='
        fetch_one_date(start)
        start += one_day
        print 'Sleeping...\n'
        sleep(10)



from argparse import ArgumentParser

argument_parser = ArgumentParser()
argument_parser.add_argument('-s')
argument_parser.add_argument('-u')



from os import popen

latest = popen("ls xml/* | awk -F'_' '{ print $2$3$4 }' | grep '\d' | tail -1").read().strip()

default_start = datetime.datetime.strptime(latest, '%Y%m%d').date() + one_day
default_until = datetime.date.today() - datetime.timedelta(hours=26)



if __name__ == '__main__':
    args = argument_parser.parse_args()
    start = default_start if args.s is None \
            else datetime.datetime.strptime(args.s, '%Y%m%d').date()
    until = default_until if args.u is None \
            else datetime.datetime.strptime(args.u, '%Y%m%d').date()
    print '{0} until {1}\n'.format(start, until)
    fetch_multiple_dates(start, until)
