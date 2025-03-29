import functools
from pxr.Usdviewq.plugin import PluginContainer
from pxr import Tf

from .common.customizationLoader import loadRelviewCustomizations
from .gui.RelationshipBrowser import RelationshipBrowser


_relationshipBrowserWidget = None


class RelviewPluginContainer(PluginContainer):
    """
    This is the entry point for the Relationship Viewer plugin integrations in
    usdview. Note that right now we're populating the Relationship Viewer (browser)
    on prim selection changes - in the future we might want to use right-click
    context menus and/or drag & drop...
    """

    def registerPlugins(self, plugRegistry, usdviewApi_notUsed):
        """Adds plugin to registry."""
        self._launchRelBrowser = plugRegistry.registerCommandPlugin(
            "relview.usdview.launchRelationshipViewer",
            "Relationship Viewer",
            launchRelationshipViewer,
        )

    def configureView(self, plugRegistry_notUsed, plugUIBuilder):
        """Adds plugin to Window menu."""
        windowMenu = plugUIBuilder.findOrCreateMenu("Window")
        launchRelViewAction = windowMenu.addItem(self._launchRelBrowser)
        launchRelViewAction.setShortcut("Ctrl+Shift+R")


def launchRelationshipViewer(usdviewApi):
    """Creates (or shows) the Relationship Viewer in usdview."""
    global _relationshipBrowserWidget

    if _relationshipBrowserWidget is None:
        _relationshipBrowserWidget = RelationshipBrowser()
        _relationshipBrowserWidget.setWindowTitle("Relationship Viewer")
        # TODO resize/move?

        _populateRelViewWithCurrentSelection(usdviewApi)  # TODO maybe don't do this?
        _followPrimSelectionChanges(usdviewApi)

    _relationshipBrowserWidget.show()


def _populateRelViewWithCurrentSelection(usdviewApi):
    selPaths = [p.GetPath() for p in usdviewApi.selectedPrims]
    stage = usdviewApi.stage
    if stage and selPaths:
        _relationshipBrowserWidget.addNewFor(stage, selPaths)


def _followPrimSelectionChanges(usdviewApi):
    usdviewApi.dataModel.selection.signalPrimSelectionChanged.connect(
        functools.partial(_primSelectionChangedSLOT, usdviewApi)
    )


def _primSelectionChangedSLOT(usdviewApi, *args_notUsed):
    # TODO maybe only do this if _relationshipBrowserWidget is visible?
    _populateRelViewWithCurrentSelection(usdviewApi)


loadRelviewCustomizations(dict(appname="usdview"))
Tf.Type.Define(RelviewPluginContainer)
