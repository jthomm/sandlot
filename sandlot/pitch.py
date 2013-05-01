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
        """Horizontal movement (in) of the ball between the release
        point and home plate relative to a ball thrown at the same speed
        with no spin.  Measured at `y`=40 ft. independent of `y0` value.
        """
        return float(self.element.attrib['pfx_x'])

    @property
    def pfx_z(self):
        """Vertical movement (in) of the ball between the release
        point and home plate relative to a ball thrown at the same speed
        with no spin.  Measured at `y`=40 ft. independent of `y0` value.
        """
        return float(self.element.attrib['pfx_z'])

    @property
    def px(self):
        """Horizontal distance (ft) of the ball from the center of 
        home plate as it crosses the plate.  Negative values signify that 
        the ball was left of the center of the plate, from the catcher and 
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
        home plate at the initial point `y0`.
        """
        return float(self.element.attrib['x0'])

    @property
    def y0(self):
        """Longitudinal distance (ft) of the ball from the center of 
        home plate relative to which the PITCHf/x system calibrates its 
        initial measurements.  Sportvision uses 50.0 ft. as late as the 
        2013 season.
        """
        return float(self.element.attrib['y0'])

    @property
    def z0(self):
        """Vertical distance (ft) of the ball from the surface of 
        home plate at the initial point `y0`.
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
    def break_y(self):
        """Longitudinal distance (ft) of the ball from the front of 
        home plate at the time of the ball's greatest deviation from the 
        straight line path between the ball's release point and the front 
        of the plate.
        """
        return float(self.element.attrib['break_y'])
