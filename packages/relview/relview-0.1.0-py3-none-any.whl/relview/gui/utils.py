from Qt import QtGui


class FontMods(object):
    """An object meant to modify a certain QFont in various ways: size (via a
    scale factor), boldness, italics, and/or weight. (can of course add other
    things over time as needed) The getModified() method takes a QFont object
    and returns a new one with the desired modifications made. Instances of this
    class are typically used as class variables to aid in customizing fonts for
    different purposes/studios/etc.
    """

    def __init__(self, sizeScale=None, bold=None, italic=None, weight=None):
        self._sizeScale = sizeScale
        self._bold = bold
        self._italic = italic
        self._weight = weight

    def getModified(self, font):
        moddedFont = (
            scaleFontSizeBy(font, self._sizeScale)
            if self._sizeScale is not None
            else QtGui.QFont(font)
        )
        if self._bold is not None:
            moddedFont.setBold(bool(self._bold))
        if self._italic is not None:
            moddedFont.setItalic(bool(self._italic))
        if self._weight is not None:
            moddedFont.setWeight(int(self._weight))
        return moddedFont


def scaleFontSizeBy(font, scaleFactor):
    """Scales the given font (QFont object) by the specified scaleFactor (floating
    point value - for example 1.25 would make the font 125% its current size).
    Does the right thing if the font size is specified in points or pixels.
    """
    scaledFont = QtGui.QFont(font)
    currentPointSize = scaledFont.pointSize()
    if currentPointSize > 0:
        # negative point size, so set new font size by points
        scaledFont.setPointSize(int(currentPointSize * scaleFactor))
    else:
        # negative point size, so set new font size by pixels
        scaledFont.setPixelSize(int(scaledFont.pixelSize() * scaleFactor))
    return scaledFont


class LayoutMods(object):
    """An object meant to modify contents margins and/or spacing of a certain
    QLayout (typically QVBoxLayout or QHBoxLayout). The modify() method takes
    a QLayout object and makes the desired modifications on that object, in-place.
    Instances of this class are typically used as class variables to aid in
    customizing layouts for different purposes/studios/etc.
    """

    def __init__(self, contentsMargins=None, spacing=None):
        self._contentsMargins = contentsMargins  # note: should be 4-integer tuple
        self._spacing = spacing  # single integer

    def modify(self, layout):
        if self._contentsMargins is not None:
            layout.setContentsMargins(*self._contentsMargins)
        if self._spacing is not None:
            layout.setSpacing(self._spacing)
