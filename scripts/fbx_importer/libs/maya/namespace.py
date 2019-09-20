# -*- coding: utf-8 -*-
"""namespace library"""
from __future__ import absolute_import, division, print_function

import os

from maya import cmds

ROOT_NAMESPACE = ":"
_NAMESPACE_SEPARATOR = ":"
_DEFAULT_NAMESPACES = [
    "UI",
    "shared",
    _NAMESPACE_SEPARATOR + "UI",
    _NAMESPACE_SEPARATOR + "shared"
]


def get_namespace_from_path(path):
    """get namespace from file path

    Args:
        path (unicode): file path

    Returns:
        unicode: namespace
    """
    return os.path.splitext(os.path.basename(path))[0]


def get_namespace_from_node(node, return_separator=False, return_root=False):
    """get namespace from node

    Args:
        node (unicode): target node
        return_separator(bool): return separator
        return_root (bool): return root namespace

    Returns:
        unicode: namespace
    """
    if not node:
        return ""
    node = node.split("|")[-1]

    namespace = ""
    if return_root:
        namespace = ROOT_NAMESPACE
    split = node.rsplit(":", 1)
    if len(split) == 1:
        return namespace
    namespace = split[0]
    if return_separator:
        namespace += _NAMESPACE_SEPARATOR
    return namespace


def is_default_namespace(name):
    """Returns whether this is the default"""
    return name in _DEFAULT_NAMESPACES


def get_namespaces(return_separator=False, return_root=False):
    """returns namespaces

    Args:
        return_separator(bool): return separator

    Returns:
        list of unicode: namespaces
    """
    cmds.namespace(set=ROOT_NAMESPACE)
    namespaces = set()
    if return_root:
        namespaces.add(ROOT_NAMESPACE)
    for sub_namespace in (cmds.namespaceInfo(listOnlyNamespaces=1, recurse=1, an=return_separator)):
        if not is_default_namespace(sub_namespace):
            namespaces.add(sub_namespace)
    return sorted(list(namespaces))


def delete_namespaces(targets=None):
    """delete namespace

    Args:
        targets (list of unicode): list of target namespaces
    """
    namespaces = get_namespaces()

    namespaces.sort(cmp=lambda s1, s2: cmp(len(s1), len(s2)), reverse=True)
    for x in namespaces:
        if targets is not None and x not in targets:
            continue
        cmds.namespace(removeNamespace=x, mergeNamespaceWithRoot=1)
