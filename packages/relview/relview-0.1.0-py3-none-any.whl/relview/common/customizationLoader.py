"""This is the mechanism relview uses to load customizations - or "plugins."
The function in here, loadRelviewCustomizations(), is typically called after
the QApplication instance has been created, but before any relview UI objects
have been created - making it possible to customize various aspects of the
system, register node styling, etc.

An attempt is made to import relview_sitecustomize - whichever is the first
one found on the Python path. If found and successfully imported, a function
called "customize_relview" will be called, and passed the metadata dictionary
passed to loadRelviewCustomizations(). Typically that metadata dict will contain
some information about the top-level application being run, or perhaps other
things that might inform the specifics of how customizations are done. In our
various calls to loadRelviewCustomizations() so far, we're just providing the
application name, like this:

    loadRelviewCustomizations(dict(appname="houdini"))

...and in a relview_sitecustomize.py on the Python path, a customize_relview()
function can do some setup/customization stuff like:

def customize_relview(metadataDict):
    # register our node styling if running relview standalone or in usdview
    appname = metadataDict.get("appname")
    if appname in ["relview", "usdview"]:
        registerOurNodeStyling()
"""

import traceback


def loadRelviewCustomizations(metadataDict=None):
    metadataDict = metadataDict or {}
    try:
        import relview_sitecustomize
    except ModuleNotFoundError:
        # no relview_sitecustomize module - no problem
        relview_sitecustomize = None
    except (ImportError, Exception) as exc:
        relview_sitecustomize = None
        print(f"Error loading relview_sitecustomize:", exc)
        traceback.print_exc()

    if relview_sitecustomize and hasattr(relview_sitecustomize, "customize_relview"):
        relview_sitecustomize.customize_relview(metadataDict)
