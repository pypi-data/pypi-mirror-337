import argparse
import sys
from Qt import QtWidgets
from pxr import Sdf, Usd

from .common.customizationLoader import loadRelviewCustomizations
from .gui.appStyling import styleTheApplication
from .gui.RelationshipBrowser import RelationshipBrowser


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("prims")

    args = parser.parse_args()
    stage = Usd.Stage.Open(args.file)

    assert stage, "Invalid stage specified."
    assert args.prims, "Must specify one or more prim paths."

    primPaths = [Sdf.Path(pstr) for pstr in set(args.prims.split())]
    removePaths = set()
    for primPath in primPaths:
        if not primPath:
            removePaths.add(primPath)
            continue

        if not stage.GetPrimAtPath(primPath):
            print(f"Invalid path: {primPath.pathString}\n  Ignoring.")
            removePaths.add(primPath)

    for remPath in removePaths:
        primPaths.remove(remPath)

    assert primPaths, "No valid prim paths."

    app = QtWidgets.QApplication([])
    app.setDesktopSettingsAware(False)
    styleTheApplication()
    loadRelviewCustomizations(dict(appname="relview"))
    relBrowser = RelationshipBrowser()
    relBrowser.setWindowTitle(f"{args.file} - Relationship Viewer")
    # TODO move/resize?

    relBrowser.addNewFor(stage, primPaths)
    relBrowser.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
