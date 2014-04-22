from collections import OrderedDict
from datetime import datetime



def except_value_error_none(old_f):
    def new_f(*args, **kwargs):
        try:
            return old_f(*args, **kwargs)
        except ValueError:
            return None
    return new_f



class Game(object):

    def __init__(self, element):
        self.element = element

    @property
    def venue(self):
        return unicode(self.element.attrib['venue'])

    @property
    def date_string(self):
        #return unicode(self.element.attrib['date'])
        dt = datetime.strptime(self.element.attrib['date'], '%B %d, %Y')
        return unicode(dt.strftime('%Y-%m-%d'))

    @property
    def away(self):
        team_element = [child for child in self.element \
                        if child.tag == 'team' and \
                           child.attrib['type'] == 'away'][0]
        return Team(team_element).as_dict

    @property
    def home(self):
        team_element = [child for child in self.element \
                        if child.tag == 'team' and \
                           child.attrib['type'] == 'home'][0]
        return Team(team_element).as_dict

    @property
    def umpires(self):
        umpires_element = [child for child in self.element \
                           if child.tag == 'umpires'][0]
        return [Umpire(child).as_dict for child in umpires_element]

    @property
    def as_dict(self):
        dct = OrderedDict()
        dct['venue'] = self.venue
        dct['date_string'] = self.date_string
        dct['away'] = self.away
        dct['home'] = self.home
        dct['umpires'] = self.umpires
        return dct



class Umpire(object):

    def __init__(self, element):
        self.element = element

    @property
    def umpire_id(self):
        return unicode(self.element.attrib['id'])

    @property
    def full_name(self):
        return unicode(self.element.attrib['name'])

    @property
    def position(self):
        return unicode(self.element.attrib['position'])

    @property
    def as_dict(self):
        dct = OrderedDict()
        dct['umpire_id'] = self.umpire_id
        dct['full_name'] = self.full_name
        dct['position'] = self.position
        return dct



class Team(object):

    def __init__(self, element):
        self.element = element

    @property
    def status(self):
        return unicode(self.element.attrib['type'])

    @property
    def abbr(self):
        return unicode(self.element.attrib['id'])

    @property
    def full_name(self):
        return unicode(self.element.attrib['name'])

    @property
    def players(self):
        return [Player(child).as_dict for child in self.element \
                if child.tag == 'player']

    @property
    def coaches(self):
        return [Coach(child).as_dict for child in self.element \
                if child.tag == 'coach']

    @property
    def as_dict(self):
        dct = OrderedDict()
        dct['status'] = self.status
        dct['abbr'] = self.abbr
        dct['full_name'] = self.full_name
        dct['players'] = self.players
        dct['coaches'] = self.coaches
        return dct



class Player(object):

    def __init__(self, element):
        self.element = element

    @property
    def player_id(self):
        return unicode(self.element.attrib['id'])

    @property
    def first_name(self):
        return unicode(self.element.attrib['first'])

    @property
    def last_name(self):
        return unicode(self.element.attrib['last'])

    @property
    def box_name(self):
        return unicode(self.element.attrib['boxname'])

    @property
    def handedness(self):
        return unicode(self.element.attrib['rl'])

    @property
    def team_id(self):
        return unicode(self.element.attrib['team_id'])

    @property
    def team_abbr(self):
        return unicode(self.element.attrib['team_abbrev'])

    @property
    def parent_team_id(self):
        return unicode(self.element.attrib['team_id'])

    @property
    def parent_team_abbr(self):
        return unicode(self.element.attrib['team_abbrev']) 

    @property
    def status(self):
        return unicode(self.element.attrib['status'])

    @property
    @except_value_error_none
    def uniform_number(self):
        return int(self.element.attrib['num'])

    @property
    def position(self):
        return unicode(self.element.attrib['position'])

    @property
    def game_position(self):
        attrib = self.element.attrib
        if 'game_position' in attrib:
            return unicode(attrib['game_position'])
        else:
            return self.position

    @property
    def current_position(self):
        attrib = self.element.attrib
        if 'current_position' in attrib:
            return unicode(attrib['current_position'])
        else:
            return self.game_position

    @property
    def batting_order(self):
        attrib = self.element.attrib
        if 'bat_order' in attrib:
            return int(attrib['bat_order'])
        else:
            return None

    @property
    def avg(self):
        return float(self.element.attrib['avg'])

    @property
    def rbi(self):
        return int(self.element.attrib['rbi'])

    @property
    def hr(self):
        return int(self.element.attrib['hr'])

    @property
    def wins(self):
        attrib = self.element.attrib
        if 'wins' in attrib:
            return int(attrib['wins'])
        else:
            return None

    @property
    def losses(self):
        attrib = self.element.attrib
        if 'losses' in attrib:
            return int(attrib['losses'])
        else:
            return None

    @property
    def era(self):
        attrib = self.element.attrib
        if 'era' in attrib:
            try:
                return float(attrib['era'])
            except ValueError:
                return None
        else:
            return None

    @property
    def as_dict(self):
        dct = OrderedDict()
        dct['player_id'] = self.player_id
        dct['first_name'] = self.first_name
        dct['last_name'] = self.last_name
        dct['box_name'] = self.box_name
        dct['handedness'] = self.handedness
        dct['team_id'] = self.team_id
        dct['team_abbr'] = self.team_abbr
        dct['parent_team_id'] = self.parent_team_id
        dct['parent_team_abbr'] = self.parent_team_abbr
        dct['status'] = self.status
        dct['uniform_number'] = self.uniform_number
        dct['position'] = self.position
        dct['game_position'] = self.game_position
        dct['current_position'] = self.current_position
        dct['batting_order'] = self.batting_order
        dct['avg'] = self.avg
        dct['rbi'] = self.rbi
        dct['hr'] = self.hr
        dct['wins'] = self.wins
        dct['losses'] = self.losses
        dct['era'] = self.era
        return dct



class Coach(object):

    def __init__(self, element):
        self.element = element

    @property
    def coach_id(self):
        return unicode(self.element.attrib['id'])

    @property
    def first_name(self):
        return unicode(self.element.attrib['first'])

    @property
    def last_name(self):
        return unicode(self.element.attrib['last'])

    @property
    def uniform_number(self):
        try:
            return int(self.element.attrib['num'])
        except ValueError:
            # Will return `ValueError` when coach is a "special assistant"
            # and therefore has no uniform number.
            return None

    @property
    def position(self):
        return unicode(self.element.attrib['position'])

    @property
    def as_dict(self):
        dct = OrderedDict()
        dct['coach_id'] = self.coach_id
        dct['first_name'] = self.first_name
        dct['last_name'] = self.last_name
        dct['uniform_number'] = self.uniform_number
        dct['position'] = self.position
        return dct
