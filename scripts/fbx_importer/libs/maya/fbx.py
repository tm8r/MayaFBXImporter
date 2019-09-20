# -*- coding: utf-8 -*-
"""FBX library"""
from __future__ import absolute_import, division, print_function

from logging import getLogger
import os

from . import namespace

from maya import cmds

FBX_EXTENSION = ".fbx"

logger = getLogger(__name__)


class FBXImportMode(object):
    """FBX import mode"""

    Add = "Add"
    Merge = "Merge"
    ExMerge = "Exmerge"


def load_fbx_plugin():
    """load plugin"""
    if not cmds.pluginInfo("fbxmaya", q=True, loaded=True):
        cmds.loadPlugin("fbxmaya")
        cmds.pluginInfo("fbxmaya", e=True, autoload=True)


def import_fbx(path, mode=FBXImportMode.Add, ns=""):
    """import FBX

    Args:
        path (unicode): path
        mode (string): import mode
        ns (unicode): namespace
    """
    _, ext = os.path.splitext(path)
    if ext != FBX_EXTENSION:
        logger.error(u"Invalid extension. path={0}".format(path))
        return
    load_fbx_plugin()
    cmds.FBXImportMode("-v", mode)
    cmds.FBXImportMergeAnimationLayers("-v", True)
    cmds.FBXImportLights("-v", False)
    cmds.FBXImportConstraints("-v", False)
    if ns and ns != namespace.ROOT_NAMESPACE:
        try:
            cmds.namespace(set=ns)
            cmds.file(path, i=True, type="FBX", iv=True, ra=True, mnc=True, pr=True, itr="combine", ns=ns)
        finally:
            cmds.namespace(set=namespace.ROOT_NAMESPACE)
    else:
        cmds.FBXImport("-f", path)
