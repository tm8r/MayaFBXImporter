# -*- coding: utf-8 -*-
"""view of FBXImporter"""
from __future__ import absolute_import, division, print_function

import os

from .vendor.Qt import QtCompat
from .vendor.Qt import QtCore
from .vendor.Qt import QtWidgets

from .libs.maya import fbx
from .libs.qt.stylesheet import StyleSheet
from .libs.qt.widgets import collapse_widget
from .libs.qt.widgets import file_line_edit
from . import fbx_helper
from . import history_helper

from maya import cmds
from maya import OpenMayaUI as omui
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

try:
    long
except NameError:
    long = int


try:
    MAYA_WINDOW = QtCompat.wrapInstance(long(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
except:
    MAYA_WINDOW = None

_ID_FORMAT = "{0}.{1}"


class FBXImporter(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    """view"""

    def __init__(self, parent=MAYA_WINDOW):
        """initialize"""
        super(FBXImporter, self).__init__(parent)
        self._makeMayaStandaloneWindow()
        self.setWindowTitle("FBX Importer")
        self.setWindowFlags(QtCore.Qt.Window)
        self.setObjectName(self.window_name())
        self.setProperty("saveWindowPref", True)
        self.setStyleSheet(StyleSheet().core_css)
        self.file_line_edit = file_line_edit.QFileLineEdit()
        self.history_list_widget = QtWidgets.QListWidget()

    @classmethod
    def window_name(cls):
        return _ID_FORMAT.format(cls.__module__, cls.__name__)

    @classmethod
    def open(cls, *args):
        """open window"""
        if cmds.window(cls.window_name(), q=True, ex=True):
            cmds.deleteUI(cls.window_name())
        win = cls()
        win._create_ui()
        win.show()

    def _create_ui(self):
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        self.root_widget = QtWidgets.QFrame(self)
        self.root_widget.setObjectName("root")
        self.setMinimumSize(QtCore.QSize(480, 200))
        self.setCentralWidget(self.root_widget)

        root_layout = QtWidgets.QGridLayout(self.root_widget)
        root_layout.setObjectName("root_layout")
        root_layout.setContentsMargins(8, 8, 8, 8)

        main_layout = QtWidgets.QVBoxLayout()
        root_layout.addLayout(main_layout, 0, 0, 1, 1)

        file_path_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(file_path_layout)

        file_path_label = QtWidgets.QLabel("Path")
        file_path_label.setFixedWidth(40)
        file_path_layout.addWidget(file_path_label)

        file_path_layout.addWidget(self.file_line_edit)

        file_select_button = QtWidgets.QPushButton(u"…")
        file_select_button.setFixedWidth(30)
        file_select_button.clicked.connect(self._on_file_select_button_clicked)
        file_path_layout.addWidget(file_select_button)

        history_widget = collapse_widget.QCollapseWidget("History")
        history_widget.addWidget(self.history_list_widget)
        main_layout.addWidget(history_widget)

        recent_files = history_helper.get_recent_files()
        if recent_files:
            self.history_list_widget.addItems(recent_files)
        self.history_list_widget.currentTextChanged.connect(self._on_history_clicked)

        spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        main_layout.addSpacerItem(spacer)

        button_layout = QtWidgets.QHBoxLayout()
        root_layout.addLayout(button_layout, 1, 0, 1, 1)
        fbx_add_button = QtWidgets.QPushButton("Add")
        fbx_add_button.clicked.connect(self._fbx_add_button_clicked)
        button_layout.addWidget(fbx_add_button)

        fbx_merge_button = QtWidgets.QPushButton("Merge")
        fbx_merge_button.clicked.connect(self._fbx_merge_button_clicked)
        button_layout.addWidget(fbx_merge_button)

        fbx_ex_merge_button = QtWidgets.QPushButton("ExMerge")
        fbx_ex_merge_button.clicked.connect(self._fbx_ex_merge_button_clicked)
        button_layout.addWidget(fbx_ex_merge_button)

    def _on_file_select_button_clicked(self):
        value, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select FBX",
            "",
            "FBX(*.fbx)"
        )
        if not value:
            return
        self.file_line_edit.setText(value)

    def _on_history_clicked(self, text):
        self.file_line_edit.setText(text)

    def _fbx_add_button_clicked(self):
        if not self._validate_file():
            return
        fbx_helper.import_fbx(self.file_line_edit.text(), fbx.FBXImportMode.Add, self)
        self.close()

    def _fbx_merge_button_clicked(self):
        if not self._validate_file():
            return
        fbx_helper.import_fbx(self.file_line_edit.text(), fbx.FBXImportMode.Merge, self)
        self.close()

    def _fbx_ex_merge_button_clicked(self):
        if not self._validate_file():
            return
        fbx_helper.import_fbx(self.file_line_edit.text(), fbx.FBXImportMode.ExMerge, self)
        self.close()

    def _validate_file(self):
        path = self.file_line_edit.text()
        if not path:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please enter FBX file path.")
            return False

        if not os.path.exists(path):
            QtWidgets.QMessageBox.warning(self, "Warning", "The file does not exist.")
            return False

        _, ext = os.path.splitext(path)
        if ext != fbx.FBX_EXTENSION:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please enter FBX file path.")
            return False

        return True
