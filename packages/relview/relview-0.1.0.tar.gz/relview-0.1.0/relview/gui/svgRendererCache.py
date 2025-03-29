from Qt import QtSvg


RENDERERS_BY_PATH = {}


def getOrCreateSvgRendererFor(svgFilePath):
    """Wee bit of a cache of QSvgRenderer objects, keyed by SVG file path. Kinda
    similar to pixmapCache.getOrCreatePixmapFor(), but no size is needed, since
    the SVG painting will scale as needed, when rendered.
    """
    if svgFilePath not in RENDERERS_BY_PATH:
        RENDERERS_BY_PATH[svgFilePath] = QtSvg.QSvgRenderer(svgFilePath)

    return RENDERERS_BY_PATH[svgFilePath]
