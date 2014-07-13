from bs4 import BeautifulSoup as BS

FT_PER_PX = 2.29

teams = (('ana', '1.svg'),
         ('ari', '15.svg'),
         ('atl', '16.svg'),
         ('bal', '2.svg'),
         ('bos', '3.svg'),
         ('cha', '4.svg'),
         ('chn', '17.svg'),
         ('cin', '2602.svg'),
         ('cle', '5.svg'),
         ('col', '19.svg'),
         ('det', '2394.svg'),
         ('hou', '2392.svg'),
         ('kca', '7.svg'),
         ('lan', '22.svg'),
         ('mia', '4169.svg'),
         ('mil', '32.svg'),
         ('min', '3312.svg'),
         ('nya', '3313.svg'),
         ('nyn', '3289.svg'),
         ('oak', '10.svg'),
         ('phi', '2681.svg'),
         ('pit', '31.svg'),
         ('sdn', '2680.svg'),
         ('sea', '680.svg'),
         ('sfn', '2395.svg'),
         ('sln', '2889.svg'),
         ('tba', '12.svg'),
         ('tex', '13.svg'),
         ('tor', '14.svg'),
         ('was', '3309.svg'),)

def get_svg(team_abbr):
    with open(team_abbr.lower() + '.svg', 'rb') as f:
        return f.read()

def get_rect_front(tag):
    # Add height (not height/2) to y because we want the front of the rubber
    return {'x': float(tag['x']) + float(tag['width'])/2,
            'y': float(tag['y']) + float(tag['height']),}

def get_circle_center(tag):
    return {'x': float(tag['cx']),
            'y': float(tag['cy']),}

def find_plate(team_abbr):
    soup = BS(get_svg(team_abbr))
    viewbox = map(float, soup.find('svg')['viewbox'].split())
    rubber_tag = soup.find('rect', {'id': 'mound'})
    if rubber_tag is not None:
        rubber = get_rect_front(rubber_tag)
        x = rubber['x'] - viewbox[0]
        y = rubber['y'] - viewbox[1] + (60.5 - 8.5/12)/FT_PER_PX
        return (x, y,)
    print '[WARNING] No <rect> found with id = \'mound\' for {0}'.format(team_abbr)
    rects = soup.find_all('rect')
    if len(rects) >= 4:
        rubber = get_rect_front(rects[-4])
        x = rubber['x'] - viewbox[0]
        y = rubber['y'] - viewbox[1] + (60.5 - 8.5/12)/FT_PER_PX
        return (x, y,)
    print '[WARNING]: No <rect> found at index = -4 for {0}'.format(team_abbr)
    mound_tag = soup.find('circle', {'fill': '#A98C48'})
    if mound_tag is not None:
        mound = get_circle_center(mound_tag)
        x = mound['x'] - viewbox[0]
        y = mound['y'] - viewbox[1] + (59 - 8.5/12)/FT_PER_PX
        return (x, y,)
    else:
        print '[WARN] No circle found for {0} with fill = \'#A98C48\' for {0}'.format(team_abbr)
        return None

"""
        mound_tag = soup.find('rect': {'id': 'mound'})
        if mound_tag is not None:
            mound = get_rect_center(mound_tag)
        else:
            print '[WARN] No rect found for {0} with id = \'mound\'; guessing at mound elem'.format(team_abbr)
            mound_tag = soup.find_all('rect')[-4]
            if mound_tag is not None:
                mound = get_rect_center(mound_tag)
            else:
                print '[ERROR] No mound found for {0}'.format(team_abbr)
                return {'x': 125.59, 'y': 'foo'}
    if mound_tag is not None:
        mound = get_rect_center
    #mound_tag = soup.find('rect', {'id': 'mound'})
    #if mound_tag is None:
    #    print '[WARNING] No <rect> with id = \'mound\'; guessing at mound element'
    #    mound_tag = soup.find_all('rect')[-4]
    #mound = (float(mound_tag['x']), float(mound_tag['y']),)
    mound = (float(mound_tag['cx']), float(mound_tag['cy']),)
    plate = (mound[0], mound[1] + 60.5/FT_PER_PX,)
    return plate
    #plate = map(float, soup.find('polyline')['points'].split()[1].split(','))
    #mound_tag = soup.find_all('rect')[-4]
    #mound = (float(mound_tag['x']), float(mound_tag['y']),)
    #return {'plate': plate, 'mound': mound, 'ft_px': (plate[1] - mound[1])/60.5}
"""
