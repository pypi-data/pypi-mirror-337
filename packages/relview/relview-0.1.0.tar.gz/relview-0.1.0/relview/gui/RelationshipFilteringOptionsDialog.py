from collections import defaultdict
import functools
from Qt import QtCore, QtWidgets

from .utils import FontMods, LayoutMods
from .widgets import ClickableLabel


class RelationshipFilteringOptionsDialog(QtWidgets.QDialog):
    """Dialog for changing options on a RelationshipFilteringOptions object.
    The accept() method applies changes to the passed-in object, so no public
    API needed. Displays checkboxes for turning the "core" aspects of the passed-
    in RelationshipFilteringOptions on and off at the top, with sections for
    the different categories of RelationshipFilter objects available thereunder.
    """

    # constants for sizes of things etc.
    LAYOUT_MODS = LayoutMods()  # basically just a placeholder
    FILTERS_LABEL_FONT_MODS = FontMods(sizeScale=1.6)
    CATEGORY_LABEL_FONT_MODS = FontMods(sizeScale=1.3)
    DIVIDER_LINE_HEIGHT = 30
    CATEGORY_SECTION_SPACING = 10
    BOTTOM_SPACING = 10
    AFTER_SECTION_LABEL_SPACING = 5

    def __init__(self, filteringOptions, parent=None):
        super().__init__(parent)

        self._filteringOptions = filteringOptions

        self._buildUI()
        self._makeConnections()

    #
    # QDialog overrides
    #
    def accept(self):
        super().accept()
        self._applyChanges()

    #
    # slots
    #
    def _catNameLabelClickedSLOT(self, categoryName):
        self._checkAllInCategory(categoryName, checked=True)

    def _catNameLabelDoubleClickedSLOT(self, categoryName):
        self._checkAllInCategory(categoryName, checked=False)

    def _selectAllClickedSLOT(self):
        self._checkAllOf(
            self._getMainOptionsCheckBoxes() + self._getAllFilterCheckBoxes(), True
        )

    def _selectNoneClickedSLOT(self):
        self._checkAllOf(
            self._getMainOptionsCheckBoxes() + self._getAllFilterCheckBoxes(), False
        )

    #
    # private helper methods
    #
    def _buildUI(self):
        self.setWindowTitle("Filtering Options")

        self._layout = QtWidgets.QVBoxLayout()
        self.LAYOUT_MODS.modify(self._layout)
        self.setLayout(self._layout)

        self._filtersLabel = QtWidgets.QLabel("Filters", self)
        self._filtersLabel.setFont(
            self.FILTERS_LABEL_FONT_MODS.getModified(self.font())
        )
        self._layout.addWidget(self._filtersLabel, 0)

        self._topSectionLayout = QtWidgets.QHBoxLayout()
        self._layout.addLayout(self._topSectionLayout, 0)

        self._col1Layout = QtWidgets.QVBoxLayout()
        self._topSectionLayout.addLayout(self._col1Layout, 0)

        self._targetRelsCBox = QtWidgets.QCheckBox("Include Target Relationships", self)
        self._targetRelsCBox.setChecked(
            self._filteringOptions.shouldFollowTargetRelationships()
        )
        self._col1Layout.addWidget(self._targetRelsCBox, 0)

        self._incomingRelsCBox = QtWidgets.QCheckBox(
            "Include Incoming Relationships", self
        )
        self._incomingRelsCBox.setChecked(
            self._filteringOptions.shouldFollowIncomingRelationships()
        )
        self._col1Layout.addWidget(self._incomingRelsCBox, 0)

        self._col2Layout = QtWidgets.QVBoxLayout()
        self._topSectionLayout.addLayout(self._col2Layout, 0)

        self._primRelsCBox = QtWidgets.QCheckBox("Include Relationships to Prims", self)
        self._primRelsCBox.setChecked(
            self._filteringOptions.shouldIncludePrimRelationships()
        )
        self._col2Layout.addWidget(self._primRelsCBox)

        self._propRelsCBox = QtWidgets.QCheckBox(
            "Include Relationships to Properties", self
        )
        self._propRelsCBox.setChecked(
            self._filteringOptions.shouldIncludePropertyRelationships()
        )
        self._col2Layout.addWidget(self._propRelsCBox)

        self._dividerLine = QtWidgets.QFrame(self)
        self._dividerLine.setFrameShape(QtWidgets.QFrame.HLine)
        self._dividerLine.setFixedHeight(self.DIVIDER_LINE_HEIGHT)
        self._layout.addWidget(self._dividerLine, 0)

        self._buildCategorySections()

        self._layout.addSpacing(self.BOTTOM_SPACING)

        self._allNoneLayout = QtWidgets.QHBoxLayout()
        self._layout.addLayout(self._allNoneLayout, 0)

        self._allNoneLayout.addStretch(1)

        self._selectAllButton = QtWidgets.QPushButton("Select All", self)
        self._allNoneLayout.addWidget(self._selectAllButton, 0, QtCore.Qt.AlignVCenter)

        self._selectNoneButton = QtWidgets.QPushButton("Select None", self)
        self._allNoneLayout.addWidget(self._selectNoneButton, 0, QtCore.Qt.AlignVCenter)

        for button in [self._selectAllButton, self._selectNoneButton]:
            button.setDefault(False)
            button.setAutoDefault(False)

        self._allNoneLayout.addStretch(1)

        self._layout.addSpacing(self.BOTTOM_SPACING)

        self._buttonBox = QtWidgets.QDialogButtonBox(self)
        self._buttonBox.addButton(QtWidgets.QDialogButtonBox.Ok)
        self._buttonBox.addButton(QtWidgets.QDialogButtonBox.Cancel)
        self._layout.addWidget(self._buttonBox, 0)

        self.setFixedSize(self.sizeHint())

    def _buildCategorySections(self):
        self._filterCheckBoxesByCatName = defaultdict(list)

        self._filterCategoriesLayout = QtWidgets.QHBoxLayout()
        self._layout.addLayout(self._filterCategoriesLayout, 0)

        categoryNames = self._filteringOptions.getFilterCategoryNames()
        lastCatIdx = len(categoryNames) - 1
        for idx, categoryName in enumerate(categoryNames):
            scrollarea = QtWidgets.QScrollArea(self)
            contentWidget = QtWidgets.QWidget(scrollarea)
            scrollarea.setWidget(contentWidget)
            scrollarea.setWidgetResizable(True)
            categoryLayout = QtWidgets.QVBoxLayout(contentWidget)
            self._filterCategoriesLayout.addWidget(scrollarea)

            categoryNameLabel = ClickableLabel(categoryName, self)
            categoryNameLabel.setFont(
                self.CATEGORY_LABEL_FONT_MODS.getModified(categoryNameLabel.font())
            )
            categoryLayout.addWidget(categoryNameLabel, 0)
            categoryLayout.addSpacing(self.AFTER_SECTION_LABEL_SPACING)

            # connect to categoryNameLabel's click signals
            categoryNameLabel.clicked.connect(
                functools.partial(self._catNameLabelClickedSLOT, categoryName)
            )
            categoryNameLabel.doubleClicked.connect(
                functools.partial(self._catNameLabelDoubleClickedSLOT, categoryName)
            )

            for filterObj in self._filteringOptions.getFiltersInCategory(categoryName):
                filterCBox = RelationshipFilterCheckBox(filterObj, self)
                self._filterCheckBoxesByCatName[categoryName].append(filterCBox)
                categoryLayout.addWidget(filterCBox, 0)

            categoryLayout.addStretch(1)

            if idx < lastCatIdx:
                self._filterCategoriesLayout.addSpacing(self.CATEGORY_SECTION_SPACING)

    def _makeConnections(self):
        self._selectAllButton.clicked.connect(self._selectAllClickedSLOT)
        self._selectNoneButton.clicked.connect(self._selectNoneClickedSLOT)
        self._buttonBox.accepted.connect(self.accept)
        self._buttonBox.rejected.connect(self.reject)

    def _checkAllInCategory(self, categoryName, checked=True):
        self._checkAllOf(self._filterCheckBoxesByCatName[categoryName], checked)

    def _checkAllOf(self, checkBoxes, checked=True):
        for cBox in checkBoxes:
            cBox.setChecked(checked)

    def _getMainOptionsCheckBoxes(self):
        return [
            self._targetRelsCBox,
            self._incomingRelsCBox,
            self._primRelsCBox,
            self._propRelsCBox,
        ]

    def _getAllFilterCheckBoxes(self):
        cBoxes = []
        for cboxList in self._filterCheckBoxesByCatName.values():
            cBoxes += cboxList
        return cBoxes

    def _applyChanges(self):
        self._filteringOptions.followTargetRelationships(
            self._targetRelsCBox.isChecked()
        )
        self._filteringOptions.followIncomingRelationships(
            self._incomingRelsCBox.isChecked()
        )
        self._filteringOptions.includePrimRelationships(self._primRelsCBox.isChecked())
        self._filteringOptions.includePropertyRelationships(
            self._propRelsCBox.isChecked()
        )
        for filterCBox in self._getAllFilterCheckBoxes():
            filterCBox.getRelationshipFilter().setActive(filterCBox.isChecked())


class RelationshipFilterCheckBox(QtWidgets.QCheckBox):
    """QCheckBox with an associated RelationshipFilter object (passed in). Used
    in RelationshipFilteringOptionsDialog, above. No big whoop.
    """

    def __init__(self, filterObj, parent=None):
        super().__init__(filterObj.getName() or "(empty)", parent)
        self._filterObj = filterObj
        self.setChecked(self._filterObj.isActive())
        self.setToolTip(self._filterObj.getDescription())

    def getRelationshipFilter(self):
        return self._filterObj
