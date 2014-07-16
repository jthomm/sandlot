from collections import OrderedDict
from math import sqrt, atan2, pi



ORIGIN_X = 125.163
ORIGIN_Y = 204.337
DISTANCE = 2.29



class BattedBalls(tuple):

    def __new__(cls, root_element):
        lst = [BattedBall(child).as_dict for child in root_element]
        return super(BattedBalls, cls).__new__(cls, lst)



class BattedBall(object):

    def __init__(self, element):
        self.element = element

    @property
    def description(self):
        return unicode(self.element.attrib['des'])

    @property
    def x(self):
        return float(self.element.attrib['x'])

    @property
    def y(self):
        return float(self.element.attrib['y'])

    @property
    def r(self):
        return DISTANCE*sqrt((self.x - ORIGIN_X)**2 + (ORIGIN_Y - self.y)**2)

    @property
    def theta(self):
        return atan2(ORIGIN_Y - self.y, self.x - ORIGIN_X)*180/pi

    @property
    def batter_id(self):
        return unicode(self.element.attrib['batter'])

    @property
    def pitcher_id(self):
        return unicode(self.element.attrib['pitcher'])

    @property
    def result(self):
        return unicode(self.element.attrib['type'])

    @property
    def team(self):
        return unicode(self.element.attrib['team'])

    @property
    def inning(self):
        return int(self.element.attrib['inning'])

    @property
    def as_dict(self):
        dct = OrderedDict()
        dct['description'] = self.description
        dct['x'] = self.x
        dct['y'] = self.y
        dct['r'] = self.r
        dct['theta'] = self.theta
        dct['batter_id'] = self.batter_id
        dct['pitcher_id'] = self.pitcher_id
        dct['result'] = self.result
        dct['team'] = self.team
        dct['inning'] = self.inning
        return dct
