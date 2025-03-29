import os

from relview import icons

RELVIEW_ICON_PATH, _ = os.path.split(icons.__file__)

WINDOW_ICON_PATH = os.path.join(RELVIEW_ICON_PATH, "relview-window.svg")

AUTO_FIT_ICON_PATH = os.path.join(RELVIEW_ICON_PATH, "auto-fit.svg")
CLEAR_ICON_PATH = os.path.join(RELVIEW_ICON_PATH, "clear.svg")
FILTER_ICON_PATH = os.path.join(RELVIEW_ICON_PATH, "filter.svg")
FILTER_ACTIVE_ICON_PATH = os.path.join(RELVIEW_ICON_PATH, "filter_active.svg")
FRAME_SELECTED_ICON_PATH = os.path.join(RELVIEW_ICON_PATH, "frame-selected.svg")
GO_BACK_ICON_PATH = os.path.join(RELVIEW_ICON_PATH, "go-back.svg")
GO_FORWARD_ICON_PATH = os.path.join(RELVIEW_ICON_PATH, "go-forward.svg")
INFO_ICON_PATH = os.path.join(RELVIEW_ICON_PATH, "info.svg")
SHOW_GRID_ICON_PATH = os.path.join(RELVIEW_ICON_PATH, "show-grid.svg")
WARNING_ICON_PATH = os.path.join(RELVIEW_ICON_PATH, "warning.svg")
