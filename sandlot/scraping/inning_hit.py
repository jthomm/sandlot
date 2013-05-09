from collections import OrderedDict



class BallsInPlay(tuple):

    def __new__(cls, root_element):
        lst = [BattedBall(child).as_dict for child in root_element]
        return super(BattedBalls, cls).__new__(cls, lst)



class BallInPlay(object):

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
        dct['batter_id'] = self.batter_id
        dct['pitcher_id'] = self.pitcher_id
        dct['result'] = self.result
        dct['team'] = self.team
        dct['inning'] = self.inning
        return dct
