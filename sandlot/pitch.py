from lxml import etree

class Pitch(object):

    def __init__(self, element):
        self.element = element

    @property
    def description(self):
        return unicode(self.element.attrib['des'])

    @property
    def pitch_id(self):
        """A unique identification number for a pitch within a game.  
        Increments by one for each pitch but not consecutive between at bats.
        """
        return int(self.element.attrib['id'])

    @property
    def pitch_type(self):
        """A one-letter abbreviation for the result of the pitch.  
        Can be S (strike, including foul balls), B (ball), or X (in play).
        """
        return unicode(self.element.attrib['type'])

    @property
    def timestamp(self):
        return unicode(self.element.attrib['tfs_zulu'])

    @property
    def x(self):
        """Horizontal location of a pitch as it crosses home plate.  
        As input by the Gameday stringer using the old Gameday coordinate
        system.
        """
        return float(self.element.attrib['x'])

    @property
    def y(self):
        """Vertical location of a pitch as it crosses home plate.  
        As input by the Gameday stringer using the old Gameday coordinate
        system.  Equivalent to the `z` coordinate in the new PITCHf/x 
        coordinate system.
        """
        return float(self.element.attrib['y'])

    @property
    def start_speed(self):
        """Pitch speed (mph) at the "initial point", `y0`."""
        return float(self.element.attrib['start_speed'])

    @property
    def end_speed(self):
        """Pitch speed (mph) as it crosses the front of home plate."""
        return float(self.element.attrib['end_speed'])

    @property
    def sz_top(self):
        """Distance (ft) from the ground to the top of the batter's
        strike zone.  The PITCHf/x operator sets a line at the batter's
        belt as he settles into hitting position and the PITCHf/x software
        adds four inches above that line to determine the top of the zone.
        """
        return float(self.element.attrib['sz_top'])

    @property
    def sz_bot(self):
        """Distance (ft) from the ground to the bottom of the batter's
        strike zone.  The PITCHf/x operator sets a line at the hollow of 
        the batter's knee as he settles into hitting position.
        """
        return float(self.element.attrib['sz_bot'])
