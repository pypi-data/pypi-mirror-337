from Qt import QtCore, QtWidgets


class withWaitCursor(object):
    """Context manager for running the code inside with a wait cursor (typically
    then the code inside will take a little time).
    """

    WAIT_CURSOR = QtCore.Qt.BusyCursor

    def __init__(self):
        self._appInst = QtWidgets.QApplication.instance()

    def __enter__(self):
        self._appInst.setOverrideCursor(self.WAIT_CURSOR)

    def __exit__(self, type, value, traceback):
        self._appInst.restoreOverrideCursor()
