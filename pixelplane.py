'''
Geometry of the LArPix pixel plane.

'''

class PixelPlane(object):
    '''
    The pixel plane for LArPix including pixel pads and LArPix chips.

    '''
    def __init__(self):
        self.pixels = {}
        self.chips = {}

    @classmethod
    def fromDict(cls, d):
        '''
        Create a new pixel plane using the data in the dict.

        Dict format:

        >>> {'pixels': [(pixelid, x, y, [(pad_vertex_1_x, y), ...],
        ...     [(focus_vertex_1_x, y), ...]), ...],  # list of pixels
        ...  'chips': [(chipid, [ch1_pixelid, ...,]), ...]  # list of chips
        ... }

        If the sensor pad is just a via, pass an empty list for the pad
        vertices. If there is no focusing grid, pass an empty list for
        the focus vertices.

        '''
        result = cls()
        for i, (pixelid, x, y, pad_outline, focus_outline) in enumerate(d['pixels']):
            pixel = Pixel()
            pixel.pixelid = pixelid
            pixel.x = x
            pixel.y = y
            pixel.pad_outline = pad_outline
            pixel.focus_outline = focus_outline
            result.pixels[pixelid] = pixel
        for i, (chipid, channel_connections) in enumerate(d['chips']):
            chip = GeomChip()
            chip.chipid = chipid
            for channel, pixelid in enumerate(channel_connections):
                chip.channel_connections.append(result.pixels[pixelid])
                result.pixels[pixelid].channel_connection = (chip, channel)
            result.chips[chipid] = chip
        return result

class GeomChip(object):
    '''
    A LArPix chip to associate with geometric features.

    '''
    def __init__(self):
        self.channel_connections = []
        self.chipid = None

class Pixel(object):
    '''
    A pixel pad + focusing region on the LArPix pixel plane.

    '''
    def __init__(self):
        self.pixelid = None
        self.x = 0
        self.y = 0
        self.pad_outline = []
        self.focus_outline = []
        self.channel_connection = None
