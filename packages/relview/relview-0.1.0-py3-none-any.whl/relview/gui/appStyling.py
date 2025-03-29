from Qt import QtGui, QtWidgets


QT_STYLE_TYPE = "Fusion"
FONT_FAMILY = "Sans Serif"
FONT_POINT_SIZE = 10


def styleTheApplication():
    # note: currently only used for "relview", the standalone application (assumes
    # color palette & styling of host application when running elsewhere)
    appInstance = QtWidgets.QApplication.instance()
    appInstance.setPalette(getColorPalette())
    appInstance.setStyle(QtWidgets.QStyleFactory.create(QT_STYLE_TYPE))
    font = QtGui.QFont(appInstance.font())
    font.setFamily(FONT_FAMILY)
    font.setPointSize(FONT_POINT_SIZE)
    appInstance.setFont(font)


def createDefaultColorPalette():
    palette = QtGui.QPalette()
    # active and inactive colors (same)
    for group in [QtGui.QPalette.Active, QtGui.QPalette.Inactive]:
        palette.setColor(group, QtGui.QPalette.Window, QtGui.QColor(49, 49, 49, 255))
        palette.setColor(
            group, QtGui.QPalette.WindowText, QtGui.QColor(149, 149, 149, 255)
        )
        palette.setColor(group, QtGui.QPalette.Base, QtGui.QColor(44, 44, 44, 255))
        palette.setColor(
            group, QtGui.QPalette.AlternateBase, QtGui.QColor(59, 59, 59, 255)
        )
        palette.setColor(
            group, QtGui.QPalette.ToolTipBase, QtGui.QColor(246, 255, 164, 255)
        )
        palette.setColor(group, QtGui.QPalette.ToolTipText, QtGui.QColor(0, 0, 0, 255))
        palette.setColor(group, QtGui.QPalette.Text, QtGui.QColor(149, 149, 149, 255))
        palette.setColor(
            group, QtGui.QPalette.ButtonText, QtGui.QColor(162, 162, 162, 255)
        )
        palette.setColor(
            group, QtGui.QPalette.BrightText, QtGui.QColor(252, 252, 252, 255)
        )
        palette.setColor(group, QtGui.QPalette.Light, QtGui.QColor(81, 81, 81, 255))
        palette.setColor(group, QtGui.QPalette.Midlight, QtGui.QColor(71, 71, 71, 255))
        palette.setColor(group, QtGui.QPalette.Button, QtGui.QColor(61, 61, 61, 255))
        palette.setColor(group, QtGui.QPalette.Mid, QtGui.QColor(40, 40, 40, 255))
        palette.setColor(group, QtGui.QPalette.Dark, QtGui.QColor(30, 30, 30, 255))
        palette.setColor(group, QtGui.QPalette.Shadow, QtGui.QColor(0, 0, 0, 255))

        if group == QtGui.QPalette.Active:
            palette.setColor(
                group, QtGui.QPalette.Highlight, QtGui.QColor(63, 127, 202, 255)
            )
        else:  # group == QtGui.QPalette.Inactive
            palette.setColor(
                group, QtGui.QPalette.Highlight, QtGui.QColor(95, 95, 95, 255)
            )

        palette.setColor(
            group, QtGui.QPalette.HighlightedText, QtGui.QColor(235, 235, 235, 255)
        )

    # disabled colors
    group = QtGui.QPalette.Disabled
    palette.setColor(group, QtGui.QPalette.Window, QtGui.QColor(49, 49, 49, 255))
    palette.setColor(
        group,
        QtGui.QPalette.WindowText,
        QtGui.QColor(149, 149, 149, 128),
    )
    palette.setColor(group, QtGui.QPalette.Base, QtGui.QColor(44, 44, 44, 128))
    palette.setColor(
        group,
        QtGui.QPalette.AlternateBase,
        QtGui.QColor(59, 59, 59, 255),
    )
    palette.setColor(
        group,
        QtGui.QPalette.ToolTipBase,
        QtGui.QColor(246, 255, 164, 255),
    )
    palette.setColor(group, QtGui.QPalette.ToolTipText, QtGui.QColor(0, 0, 0, 255))
    palette.setColor(group, QtGui.QPalette.Text, QtGui.QColor(149, 149, 149, 128))
    palette.setColor(
        group,
        QtGui.QPalette.ButtonText,
        QtGui.QColor(162, 162, 162, 128),
    )
    palette.setColor(
        group,
        QtGui.QPalette.BrightText,
        QtGui.QColor(252, 252, 252, 128),
    )
    palette.setColor(group, QtGui.QPalette.Light, QtGui.QColor(45, 45, 45, 255))
    palette.setColor(group, QtGui.QPalette.Midlight, QtGui.QColor(71, 71, 71, 255))
    palette.setColor(group, QtGui.QPalette.Button, QtGui.QColor(61, 61, 61, 128))
    palette.setColor(group, QtGui.QPalette.Mid, QtGui.QColor(15, 15, 15, 255))
    palette.setColor(group, QtGui.QPalette.Dark, QtGui.QColor(30, 30, 30, 255))
    palette.setColor(group, QtGui.QPalette.Shadow, QtGui.QColor(0, 0, 0, 128))
    palette.setColor(group, QtGui.QPalette.Highlight, QtGui.QColor(33, 97, 172, 255))
    palette.setColor(
        group, QtGui.QPalette.HighlightedText, QtGui.QColor(235, 235, 235, 255)
    )

    return palette


APP_PALETTE = createDefaultColorPalette()


def getColorPalette():
    return QtGui.QPalette(APP_PALETTE)
