# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from .vendor.Qt import QtWidgets

from .libs.maya import fbx
from .libs.maya import namespace
from . import history_helper


def import_fbx(path, import_mode, parent):
    """import fbx

    Args:
        path (unicode): path
        import_mode (.libs.maya.fbx.FBXImportMode): import mode
        parent (QtWidgets.QWidget): parent
    """
    namespaces = namespace.get_namespaces(return_separator=True, return_root=True)

    if len(namespaces) == 1:
        fbx.import_fbx(path, import_mode, namespaces[0])
        history_helper.add_recent_file(path)
        return

    ns, confirmed = QtWidgets.QInputDialog.getItem(parent,
                                                   "Select Namespace",
                                                   "Namespace",
                                                   namespaces,
                                                   0,
                                                   False)
    if not confirmed:
        return

    fbx.import_fbx(path, import_mode, ns)
    history_helper.add_recent_file(path)
