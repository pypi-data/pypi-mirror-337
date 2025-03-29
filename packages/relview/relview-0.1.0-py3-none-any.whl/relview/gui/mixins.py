from Qt import QtCore, QtGui

from ..data.decorators import waitThisLongBeforeRunning


class HoverMixin(object):
    """Mixin to slightly simplify mouse hovering over the inherited widget. Sub-
    classes can implement either or both of the _handleHoverEntered() and
    _handleHoverLeft() methods, and make use of the isMouseHovering() method.
    Handy dandy.
    """

    # instance state
    _inMouseHover = False

    # public API
    def isMouseHovering(self):
        return self._inMouseHover

    #
    # QWidget overrides
    #
    def enterEvent(self, evt):
        self.__class__.enterEvent(self, evt)
        self._inMouseHover = True
        self._handleHoverEntered()

    def leaveEvent(self, evt):
        self.__class__.leaveEvent(self, evt)
        self._inMouseHover = False
        self._handleHoverLeft()

    #
    # QWidget overrides
    #
    def _handleHoverEntered(self):
        pass  # subclasses can implement this

    def _handleHoverLeft(self):
        pass  # subclasses can implement this


class RoundedCornersMixin(object):
    """Mixin to be inherited by QWidget subclasses that would like to have rounded
    corners. Probably best for "flat" widgets like QWidget and QLabel. Change
    BORDER_RADIUS to tase, or override getBorderRadius(), to answer just-in time,
    for scenarios like when the border radius depends on the widget's dimensions.
    Note that the rounded corner thing is implemented via a paintEvent() override,
    so if the inheriting QWidget subclass also has a paintEvent() implementation,
    this won't be as immediately/easily useful.

    The rounded corners are actually implemented by setting the widget's background
    to be transparent, then drawing a rounded rectangle in the widget's background
    color in the paintEvent() before proceeding with remaining painting. Note: when
    FILL_WITH_PARENT_BG is True (the default) and there's a parent widget, we first
    fill the widget's rectangle with the parent widget's background color, since
    that seems to produce better results. If that doesn't work in your application
    for some reason, try setting FILL_WITH_PARENT_BG to False. If the rounded
    corners don't look good/correct in your application, you can turn them off
    entirely (for each class that inherits this mixin) by setting BORDER_RADIUS
    to 0.

    TODO have option for painting a border line?
    """

    # class constants
    BORDER_RADIUS = 12.0
    FILL_WITH_PARENT_BG = True

    def __init__(self):
        self._setTransparentWindow()

    @waitThisLongBeforeRunning(1)
    def _setTransparentWindow(self):
        if self.BORDER_RADIUS:
            try:
                self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            except RuntimeError:
                # "wrapped C/C++ object of type <type> has been deleted" can happen
                # since we're doing this in a deferred fashion, so catch and ignore
                pass

    def getBorderRadius(self):
        return self.BORDER_RADIUS

    # QWidget overrides
    def paintEvent(self, event):
        borderRadius = self.getBorderRadius()
        if borderRadius and self.BORDER_RADIUS:  # double check in case turned off
            # draw a rounded rectangle in the current background color
            bgColor = self.palette().color(self.backgroundRole())
            painter = QtGui.QPainter(self)
            rect = self.rect()
            # fill with transparency (or parent widget's background color) first
            fillColor = QtCore.Qt.transparent
            parentWid = self.parentWidget()
            if self.FILL_WITH_PARENT_BG and parentWid:
                parentPal = parentWid.palette()
                fillColor = parentPal.color(parentWid.backgroundRole())
            painter.fillRect(rect, fillColor)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)  # smooth borders
            painter.setBrush(bgColor)
            # TODO line below something else if we're drawing a border line
            painter.setPen(QtCore.Qt.transparent)
            painter.drawRoundedRect(rect, borderRadius, borderRadius)

        self.__class__.paintEvent(self, event)


class DoOnFirstShowMixin(object):
    """Little mixin to do some activity a QWidget's first showEvent() - handy when
    things like widget sizes/positions/scale factors need to be sorted out just
    _after_ being shown for the first time, for example. Inherit this by QWidget
    subclasses and implement one or both of _doBeforeFirstShow(), _doAfterFirstShow()
    to perform first-show, only-once duties.
    """

    # instance state
    _didFirstShow = False

    # QWidget overrides
    def showEvent(self, event):
        if not self._didFirstShow:
            self._doBeforeFirstShow(event)
        self.__class__.showEvent(self, event)
        if not self._didFirstShow:
            self._doAfterFirstShow(event)
        self._didFirstShow = True

    # private helper methods - for subclasses to implement
    def _doBeforeFirstShow(self, showEvent):
        pass

    def _doAfterFirstShow(self, showEvent):
        pass


class WidgetColorMixin(object):
    """Mixin to be inherited by QWidget subclasses that provides configured,
    easily customizable colorization for the inheriting widget and its child
    widgets. We typically change the color of widget backgrounds (and soemtimes
    foregrounds) by changing their foreground/background _roles_, such that colors
    from the existing palette will be chosen. But sometimes, for various reasons,
    changing colors via roles won't work, so specifying specific colors becomes
    necessary (via palette changes).

    The class constants (defined below) are for applying color changes across-the-
    board for instances of the inheriting class, by role and/or specific color
    values. Change those as desired in the inheriting class to taste, make sure
    to call applyWidgetColors() somewhere in the constructor, and Bob's your uncle.

    For child widgets that aren't custom subclasses (like a vanilla QLabel, QLineEdit,
    etc.) we'll define class-level constants for them, then use either or both
    of setBackgroundColorOf(), setForegroundColorOf() to apply the colorization.
    Check out what RelationshipDetailViewer does for examples.
    """

    # class constants
    BACKGROUND_ROLE = None
    BACKGROUND_COLOR = None

    FOREGROUND_ROLE = None
    FOREGROUND_COLOR = None

    # public API
    def applyWidgetColors(self):
        self.setBackgroundColorOf(self, self.BACKGROUND_ROLE, self.BACKGROUND_COLOR)
        self.setForegroundColorOf(self, self.FOREGROUND_ROLE, self.FOREGROUND_COLOR)

    def setBackgroundColorOf(self, childWidget, colorRole=None, colorVal=None):
        if colorRole is not None:
            setBGFromRole(childWidget, colorRole)
        if colorVal is not None:
            setBGFromColor(childWidget, colorVal)

    def setForegroundColorOf(self, childWidget, colorRole=None, colorVal=None):
        if colorRole is not None:
            setFGFromRole(childWidget, colorRole)
        if colorVal is not None:
            setFGFromColor(childWidget, colorVal)


#
# helper functions for WidgetColorMixin, above
#
def setBackgroundColorOf(childWidget, colorRole=None, colorVal=None):
    if colorRole is not None:
        setBGFromRole(childWidget, colorRole)
    if colorVal is not None:
        setBGFromColor(childWidget, colorVal)


def setForegroundColorOf(childWidget, colorRole=None, colorVal=None):
    if colorRole is not None:
        setFGFromRole(childWidget, colorRole)
    if colorVal is not None:
        setFGFromColor(childWidget, colorVal)


def setBGFromColor(widget, colorVal):
    setColorViaPalette(widget, widget.backgroundRole(), colorVal)
    widget.setAutoFillBackground(True)


def setBGFromRole(widget, colorRole):
    widget.setBackgroundRole(colorRole)
    widget.setAutoFillBackground(True)


def setFGFromColor(widget, colorVal):
    setColorViaPalette(widget, widget.foregroundRole(), colorVal)


def setFGFromRole(widget, colorRole):
    widget.setForegroundRole(colorRole)


def setColorViaPalette(widget, colorRole, colorVal):
    palette = widget.palette()
    palette.setColor(colorRole, colorVal)
    widget.setPalette(palette)


class ClickableMixin(object):
    """Mixin that provides left mouse button click handling, via a _handleClick()
    method that subclasses should implement.
    Note: using weird-looking self.__class__.<method> in QWidget override methods
    due to this being a mixin (so super() won't work).
    """

    # class constants
    CLICK_RADIUS = 5  # TODO good value for this?

    # instance stage
    _mousePressPos = None

    def isMousePressed(self):
        return self._mousePressPos is not None

    #
    # QWidget overrides
    #
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._mousePressPos = event.pos()
            return
        self.__class__.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        if self.isMousePressed() and event.button() == QtCore.Qt.LeftButton:
            thisPoint = event.pos() - self._mousePressPos
            if thisPoint.manhattanLength() <= self.CLICK_RADIUS:
                self._handleClick(self._mousePressPos, event)

            self._mousePressPos = None
            return
        self.__class__.mouseReleaseEvent(self, event)

    def mouseDoubleClickEvent(self, event):
        self._handleDoubleClick(event.pos(), event)

    #
    # "protected" methods
    #
    def _handleClick(self, clickPos, event):
        pass  # subclasses can implement this

    def _handleDoubleClick(self, clickPos, event):
        pass  # subclasses can implement this
