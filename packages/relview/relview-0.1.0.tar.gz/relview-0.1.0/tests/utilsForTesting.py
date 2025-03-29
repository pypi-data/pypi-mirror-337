from Qt import QtCore


class SignalReceiver(QtCore.QObject):
    """Simple QObject with a slot that logs the arguments it receives from
    whatever signal gets connected to it.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.clearSignalData()

    def theSlot(self, *args):
        self._signalsReceived.append(args)

    def clearSignalData(self):
        self._signalsReceived = []

    def hasReceivedAnySignals(self):
        return self.getNumSignalsReceived() > 0

    def getNumSignalsReceived(self):
        return len(self._signalsReceived)

    def getSignalData(self):
        return self._signalsReceived
