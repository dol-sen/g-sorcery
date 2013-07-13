#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    backend.py
    ~~~~~~~~~~
    
    ELPA backend
    
    :copyright: (c) 2013 by Jauhien Piatlicki
    :license: GPL-2, see LICENSE for more details.
"""

import os

from g_sorcery.backend import Backend
from g_sorcery.metadata import MetadataGenerator
from g_sorcery.eclass import EclassGenerator
from g_sorcery.fileutils import get_pkgpath

from .elpa_db import ElpaDB
from .ebuild import ElpaEbuildWithDigestGenerator, ElpaEbuildWithoutDigestGenerator


class ElpaEclassGenerator(EclassGenerator):
    def __init__(self):
        super(ElpaEclassGenerator, self).__init__(os.path.join(get_pkgpath(__file__), 'data'))
        

instance = Backend(ElpaDB,
                   ElpaEbuildWithDigestGenerator, ElpaEbuildWithoutDigestGenerator,
                   ElpaEclassGenerator, MetadataGenerator, sync_db=False)