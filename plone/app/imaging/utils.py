import struct
from zope.component import getUtility
from Products.CMFCore.interfaces import IPropertiesTool

def getAllowedSizes():
    ptool = getUtility(IPropertiesTool)
    sizes = {}
    for line in ptool.imaging_properties.getProperty('allowed_sizes'):
        line = line.strip()
        if line:
            name, dims = line.split(' ', 1)
            sizes[name.strip()] = tuple(map(int, dims.split(':', 1)))
    return sizes


def scaleImage(original_file, thumbnail_file, width, height, default_format='PNG'):
    import PIL.Image
    PIL_ALGO = PIL.Image.ANTIALIAS
    ptool = getUtility(IPropertiesTool)
    PIL_QUALITY = ptool.imaging_properties.getProperty('quality', 88)

    #make sure we have valid int's
    size = int(width), int(height)
    image = PIL.Image.open(original_file)
    # consider image mode when scaling
    # source images can be mode '1','L,','P','RGB(A)'
    # convert to greyscale or RGBA before scaling
    # preserve palletted mode (but not pallette)
    # for palletted-only image formats, e.g. GIF
    # PNG compression is OK for RGBA thumbnails
    original_mode = image.mode
    if original_mode == '1':
        image = image.convert('L')
    elif original_mode == 'P':
        image = image.convert('RGBA')
    image.thumbnail(size, PIL_ALGO)
    format = image.format and image.format or default_format
    # decided to only preserve palletted mode
    # for GIF, could also use image.format in ('GIF','PNG')
    if original_mode == 'P' and format == 'GIF':
        image = image.convert('P')
    # quality parameter doesn't affect lossless formats
    image.save(thumbnail_file, format, quality=PIL_QUALITY)
    width, height = image.size
    thumbnail_file.seek(0)
    return format.lower(), width, height


def getImageInfo(stream):
    """ Stream based version of OFS.Image.getImageInfo """
    data = stream.read(25)
    size = len(data)
    height = 0
    width = 0
    content_type = 'application/octet-stream'

    # handle GIFs
    if (size >= 10) and data[:6] in ('GIF87a', 'GIF89a'):
        # Check to see if content_type is correct
        content_type = 'image/gif'
        w, h = struct.unpack("<HH", data[6:10])
        width = int(w)
        height = int(h)

    # See PNG v1.2 spec (http://www.cdrom.com/pub/png/spec/)
    # Bytes 0-7 are below, 4-byte chunk length, then 'IHDR'
    # and finally the 4-byte width, height
    elif ((size >= 24) and (data[:8] == '\211PNG\r\n\032\n')
          and (data[12:16] == 'IHDR')):
        content_type = 'image/png'
        w, h = struct.unpack(">LL", data[16:24])
        width = int(w)
        height = int(h)

    # Maybe this is for an older PNG version.
    elif (size >= 16) and (data[:8] == '\211PNG\r\n\032\n'):
        # Check to see if we have the right content type
        content_type = 'image/png'
        w, h = struct.unpack(">LL", data[8:16])
        width = int(w)
        height = int(h)

    # handle JPEGs
    elif (size >= 2) and (data[:2] == '\377\330'):
        content_type = 'image/jpeg'
        stream.seek(0, 2)
        b = stream.read(1)
        try:
            while (b and ord(b) != 0xDA):
                while (ord(b) != 0xFF): b = stream.read(1)
                while (ord(b) == 0xFF): b = stream.read(1)
                if (ord(b) >= 0xC0 and ord(b) <= 0xC3):
                    stream.read(3)
                    h, w = struct.unpack(">HH", stream.read(4))
                    break
                else:
                    stream.read(int(struct.unpack(">H", stream.read(2))[0])-2)
                b = stream.read(1)
            width = int(w)
            height = int(h)
        except: pass

    stream.seek(0,0)
    return content_type, width, height
