from collections import OrderedDict



class Inning(object):

    def __init__(self, element):
        self.element = element

    @property
    def number(self):
        return int(self.element.attrib['num'])

    @property
    def away_team_abbr(self):
        return unicode(self.element.attrib['away_team'].upper())

    @property
    def home_team_abbr(self):
        return unicode(self.element.attrib['home_team'].upper())

    @property
    def is_final(self):
        return self.element.attrib['next'] == 'N'

    @property
    def top(self):
        top_elements = [child for child in self.element \
                        if child.tag == 'top']
        if len(top_elements) == 0:
            return None
        else:
            return Side(top_elements[0]).as_dict

    @property
    def bottom(self):
        bottom_elements = [child for child in self.element \
                           if child.tag == 'bottom']
        if len(bottom_elements) == 0:
            return None
        else:
            return Side(bottom_elements[0]).as_dict

    @property
    def as_dict(self):
        dct = OrderedDict()
        dct['number'] = self.number
        dct['away_team_abbr'] = self.away_team_abbr
        dct['home_team_abbr'] = self.home_team_abbr
        dct['is_final'] = self.is_final
        dct['top'] = self.top
        dct['bottom'] = self.bottom
        return dct



class Side(object):

    def __init__(self, element):
        self.element = element

    @property
    def at_bats(self):
        return [AtBat(child).as_dict for child in self.element \
                if child.tag == 'atbat']

    @property
    def actions(self):
        return [Action(child).as_dict for child in self.element \
                if child.tag == 'action']

    @property
    def as_dict(self):
        dct = OrderedDict()
        dct['at_bats'] = self.at_bats
        dct['actions'] = self.actions
        return dct



class Action(object):

    def __init__(self, element):
        self.element = element

    @property
    def balls(self):
        return int(self.element.attrib['b'])

    @property
    def strikes(self):
        return int(self.element.attrib['s'])

    @property
    def outs(self):
        return int(self.element.attrib['o'])

    @property
    def timestamp(self):
        return unicode(self.element.attrib['tfs_zulu'])

    @property
    def description(self):
        return unicode(self.element.attrib['des'])

    @property
    def event(self):
        return unicode(self.element.attrib['event'])

    @property
    def player_id(self):
        return unicode(self.element.attrib['player'])

    @property
    def pitch(self):
        return int(self.element.attrib['pitch'])

    @property
    def as_dict(self):
        dct = OrderedDict()
        dct['balls'] = self.balls
        dct['strikes'] = self.strikes
        dct['outs'] = self.outs
        dct['timestamp'] = self.timestamp
        dct['description'] = self.description
        dct['event'] = self.event
        dct['player_id'] = self.player_id
        dct['pitch'] = self.pitch
        return dct



class AtBat(object):

    def __init__(self, element):
        self.element = element

    @property
    def number(self):
        return int(self.element.attrib['num'])

    @property
    def balls(self):
        return int(self.element.attrib['b'])

    @property
    def strikes(self):
        return int(self.element.attrib['s'])

    @property
    def outs(self):
        return int(self.element.attrib['o'])

    @property
    def timestamp(self):
        return unicode(self.element.attrib['start_tfs_zulu'])

    @property
    def batter_id(self):
        return unicode(self.element.attrib['batter'])

    @property
    def batter_stance(self):
        return unicode(self.element.attrib['stand'])

    @property
    def batter_height(self):
        return unicode(self.element.attrib['b_height'])

    @property
    def pitcher_id(self):
        return unicode(self.element.attrib['pitcher'])

    @property
    def pitcher_hand(self):
        return unicode(self.element.attrib['p_throws'])

    @property
    def description(self):
        return unicode(self.element.attrib['des'])

    @property
    def event(self):
        return unicode(self.element.attrib['event'])

    @property
    def pitches(self):
        return [Pitch(child).as_dict for child in self.element \
                if child.tag == 'pitch']

    @property
    def runners(self):
        return [Runner(child).as_dict for child in self.element \
                if child.tag == 'runner']

    @property
    def as_dict(self):
        dct = OrderedDict()
        dct['number'] = self.number
        dct['balls'] = self.balls
        dct['strikes'] = self.strikes
        dct['outs'] = self.outs
        dct['timestamp'] = self.timestamp
        dct['batter_id'] = self.batter_id
        dct['batter_stance'] = self.batter_stance
        dct['batter_height'] = self.batter_height
        dct['pitcher_id'] = self.pitcher_id
        dct['pitcher_hand'] = self.pitcher_hand
        dct['description'] = self.description
        dct['event'] = self.event
        dct['pitches'] = self.pitches
        dct['runners'] = self.runners
        return dct



class Runner(object):

    def __init__(self, element):
        self.element = element

    @property
    def runner_id(self):
        return unicode(self.element.attrib['id'])

    @property
    def start(self):
        return unicode(self.element.attrib['start'])

    @property
    def end(self):
        return unicode(self.element.attrib['end'])

    @property
    def event(self):
        return unicode(self.element.attrib['event'])

    @property
    def as_dict(self):
        dct = OrderedDict()
        dct['runner_id'] = self.runner_id
        dct['start'] = self.start
        dct['end'] = self.end
        dct['event'] = self.event
        return dct


class Pitch(object):

    def __init__(self, element):
        self.element = element

    @property
    def description(self):
        return unicode(self.element.attrib['des'])

    @property
    def cc(self):
        """Additional comments about the pitch?"""
        return unicode(self.element.attrib['cc'])

    @property
    def pitch_id(self):
        """A unique identification number for a pitch within a game.  
        Increments by one for each pitch but not consecutive between at bats.
        """
        return int(self.element.attrib['id'])

    @property
    def result(self):
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
        """Speed (mph) of the ball at the initial distance, `y0`."""
        return float(self.element.attrib['start_speed'])

    @property
    def end_speed(self):
        """Speed (mph) of the ball as it crosses the front of home plate."""
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

    @property
    def pfx_x(self):
        """Horizontal movement (in) of the ball between `y0` and home plate 
        relative to a ball thrown at the same speed with no spin.  Measured 
        at `y`=40 ft. independent of `y0` value.
        """
        return float(self.element.attrib['pfx_x'])

    @property
    def pfx_z(self):
        """Vertical movement (in) of the ball between `y0` and home plate 
        relative to a ball thrown at the same speed with no spin.  Measured 
        at `y`=40 ft. independent of `y0` value.
        """
        return float(self.element.attrib['pfx_z'])

    @property
    def px(self):
        """Horizontal distance (ft) of the ball from the center of 
        home plate as it crosses the plate.  Negative values signify that 
        the ball was left of the center of the plate from the catcher and 
        umpire's perspectives.
        """
        return float(self.element.attrib['px'])

    @property
    def pz(self):
        """Vertical distance (ft) of the ball from the surface of 
        home plate as it crosses the plate."""
        return float(self.element.attrib['pz'])

    @property
    def x0(self):
        """Horizontal distance (ft) of the ball from the center of 
        home plate at the initial tracking location `y0`.
        """
        return float(self.element.attrib['x0'])

    @property
    def y0(self):
        """Longitudinal distance (ft) of the ball from the front of 
        home plate relative to which the PITCHf/x system calibrates its 
        initial measurements.  Sportvision uses 50.0 ft. as late as the 
        2013 season.  Initial tracking location.
        """
        return float(self.element.attrib['y0'])

    @property
    def z0(self):
        """Vertical distance (ft) of the ball from the surface of 
        home plate at the initial tracking location `y0`.
        """
        return float(self.element.attrib['z0'])

    @property
    def vx0(self):
        """Horizontal velocity (ft/second) of the ball at the initial 
        point `y0`.
        """
        return float(self.element.attrib['vx0'])

    @property
    def vz0(self):
        """Vertical velocity (ft/second) of the ball at the initial 
        point `y0`.
        """
        return float(self.element.attrib['vz0'])

    @property
    def vy0(self):
        """Longitudinal velocity (ft/second) of the ball at the initial 
        point `y0`.
        """
        return float(self.element.attrib['vy0'])

    @property
    def ax(self):
        """Horizontal acceleration (ft/second^2) of the ball at the initial 
        point `y0`.
        """
        return float(self.element.attrib['ax'])

    @property
    def ay(self):
        """Vertical acceleration (ft/second^2) of the ball at the initial 
        point `y0`.
        """
        return float(self.element.attrib['ay'])

    @property
    def az(self):
        """Longitudinal acceleration (ft/second^2) of the ball at the initial 
        point `y0`.
        """
        return float(self.element.attrib['az'])

    @property
    def spin_dir(self):
        """Angle between the `y` axis and the axis of rotation of the ball 
        with a sign such that 90 degrees corresponds to the spin pointing 
        upward, along the `z` axis.
        """
        return float(self.element.attrib['spin_dir'])

    @property
    def spin_rate(self):
        """Spin (rpm) of the ball."""
        return float(self.element.attrib['spin_rate'])

    @property
    def break_y(self):
        """Longitudinal distance (ft) of the ball from the front of 
        home plate at the time of the ball's greatest deviation from the 
        straight line path between `y0` and the front of home plate.
        """
        return float(self.element.attrib['break_y'])

    @property
    def break_angle(self):
        """Angle (degrees) of the ball from "12 o'clock" at the time of 
        the ball's greatest deviation from the straight line path between 
        `y0` and the front of home plate.
        """
        return float(self.element.attrib['break_angle'])

    @property
    def break_length(self):
        """Distance (in) of the ball from dead center at the time of 
        the ball's greatest deviation from the straight line path between 
        `y0` and the front of home plate.  Break magnitude.
        """
        return float(self.element.attrib['break_length'])

    @property
    def pitch_type(self):
        """Probable pitch type according to a classification algorithm 
        developed by Ross Paul of MLBAM.  Values are as follows:

        FA    Fastball
        FF    4-seam Fastball
        FT    2-seam Fastball
        FC    Cut Fastball
        FS    Split-finger Fastball
        FO    Forkball
        IN    Intentional Ball
        SI    Sinker
        SL    Slider
        CU    Curveball
        KC    Knuckle Curve
        EP    Ephuus
        CH    Change-up
        SC    Screwball
        KN    Knuckleball
        UN    Unknown
        """
        return unicode(self.element.attrib['pitch_type'])

    @property
    def type_confidence(self):
        return float(self.element.attrib['type_confidence'])

    @property
    def zone(self):
        return int(self.element.attrib['zone'])

    @property
    def nasty(self):
        """Measures "nastiness" of the pitch based on the following:

        History -- The less successful a batter is against similar pitches, 
        the greater the nastiness.

        Velocity -- The greater the pitch's velocity relative to that 
        pitcher's and the league's range of velocity for the same type of 
        pitch, the greater the nastiness.

        Sequence -- The more the pitcher mixes up his pitches, the greater 
        the nastiness.  Certain pitch sequences are nastier than others.

        Location -- The closer the pitch lands to the edges of the strike 
        zone, the greater the nastiness.

        Movement -- The greater the movement relative to that pitcher's 
        and the league's range of movement for the same type of pitch, the 
        greater the nastiness.
        """
        return int(self.element.attrib['nasty'])

    @property
    def sv_id(self):
        """Timestamp when the PITCHf/x tracking system first detects the 
        ball in the air.  Formatted `YYMMDD_hhmmss`.
        """
        return unicode(self.element.attrib['sv_id'])

    @property
    def as_dict(self):
        dct = OrderedDict()
        dct['description'] = self.description
        dct['cc'] = self.cc
        dct['pitch_id'] = self.pitch_id
        dct['result'] = self.result
        dct['timestamp'] = self.timestamp
        dct['x'] = self.x
        dct['y'] = self.y
        dct['start_speed'] = self.start_speed
        dct['end_speed'] = self.end_speed
        dct['sz_top'] = self.sz_top
        dct['sz_bot'] = self.sz_bot
        dct['pfx_x'] = self.pfx_x
        dct['pfx_z'] = self.pfx_z
        dct['px'] = self.px
        dct['pz'] = self.pz
        dct['x0'] = self.x0
        dct['y0'] = self.y0
        dct['z0'] = self.z0
        dct['vx0'] = self.vx0
        dct['vz0'] = self.vz0
        dct['vy0'] = self.vy0
        dct['ax'] = self.ax
        dct['ay'] = self.ay
        dct['az'] = self.az
        dct['spin_dir'] = self.spin_dir
        dct['spin_rate'] = self.spin_rate
        dct['break_y'] = self.break_y
        dct['break_angle'] = self.break_angle
        dct['break_length'] = self.break_length
        dct['pitch_type'] = self.pitch_type
        dct['type_confidence'] = self.type_confidence
        dct['zone'] = self.zone
        dct['nasty'] = self.nasty
        dct['sv_id'] = self.sv_id
        return dct
