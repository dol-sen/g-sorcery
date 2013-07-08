#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    test_elpa_ebuild.py
    ~~~~~~~~~~~~~~~~~~~
    
    ELPA ebuild generator test suite
    
    :copyright: (c) 2013 by Jauhien Piatlicki
    :license: GPL-2, see LICENSE for more details.
"""

import os, unittest

from g_sorcery import package_db

from g_elpa import elpa_db, ebuild

from tests.base import BaseTest

from tests.test_elpa_db import fill_database, packages

class TestElpaEbuildGenerator(BaseTest):

    def test_generate_without_digest(self):
        edb = elpa_db.ElpaDB(os.path.join(self.tempdir.name, 'db'),
                             repo_uri = 'http://127.0.0.1:8080')
        fill_database(edb, packages, self.tempdir.name)
        ebuild_generator = ebuild.ElpaEbuildWithoutDigestGenerator(edb)
        src = ebuild_generator.generate(package_db.Package('app-emacs', 'ack', '1.2'))
        self.assertEqual(src,
                         ['# automatically generated by g-elpa',
                          '# please do not edit this file', '',
                          'EAPI=5', '', 'REPO_URI="http://127.0.0.1:8080"',
                          'PKG_TYPE="tar"', 'REALNAME="ack"', '', 'inherit g-elpa', '',
                          'DESCRIPTION="Interface to ack-like source code search tools"',
                          'HOMEPAGE="http://127.0.0.1:8080"', 'SRC_URI=""',
                          'LICENSE="GPL-2"', '', 'SLOT="0"', 'KEYWORDS="~amd64 ~x86"',
                          'IUSE=""', '', 'DEPEND=""', 'RDEPEND=""'])
        src = ebuild_generator.generate(package_db.Package('app-emacs', 'dict-tree', '0.12.8'))
        self.assertEqual(src,
                         ['# automatically generated by g-elpa',
                          '# please do not edit this file', '', 'EAPI=5', '',
                          'REPO_URI="http://127.0.0.1:8080"', 'PKG_TYPE="tar"',
                          'REALNAME="dict-tree"', '',
                          'inherit g-elpa', '', 'DESCRIPTION="Dictionary data structure"',
                          'HOMEPAGE="http://127.0.0.1:8080"', 'SRC_URI=""',
                          'LICENSE="GPL-2"', '', 'SLOT="0"',
                          'KEYWORDS="~amd64 ~x86"', 'IUSE=""', '',
                          'DEPEND="app-emacs/trie-0.2.5\napp-emacs/tNFA-0.1.1\napp-emacs/heap-0.3"',
                          'RDEPEND="app-emacs/trie-0.2.5\napp-emacs/tNFA-0.1.1\napp-emacs/heap-0.3"'])

    def test_generate_with_digest(self):
        edb = elpa_db.ElpaDB(os.path.join(self.tempdir.name, 'db'),
                             repo_uri = 'http://127.0.0.1:8080')
        fill_database(edb, packages, self.tempdir.name)
        ebuild_generator = ebuild.ElpaEbuildWithDigestGenerator(edb)
        src = ebuild_generator.generate(package_db.Package('app-emacs', 'ack', '1.2'))
        self.assertEqual(src,
                         ['# automatically generated by g-elpa',
                          '# please do not edit this file', '',
                          'EAPI=5', '', 'REPO_URI="http://127.0.0.1:8080"',
                          'PKG_TYPE="tar"', 'REALNAME="ack"', '', 'inherit g-elpa', '',
                          'DESCRIPTION="Interface to ack-like source code search tools"',
                          'HOMEPAGE="http://127.0.0.1:8080"',
                          'SRC_URI="${REPO_URI}${REALNAME}-${PV}.${SUFFIX}"',
                          'LICENSE="GPL-2"', '', 'SLOT="0"', 'KEYWORDS="~amd64 ~x86"',
                          'IUSE=""', '', 'DEPEND=""', 'RDEPEND=""'])
        src = ebuild_generator.generate(package_db.Package('app-emacs', 'dict-tree', '0.12.8'))
        self.assertEqual(src,
                         ['# automatically generated by g-elpa',
                          '# please do not edit this file', '', 'EAPI=5', '',
                          'REPO_URI="http://127.0.0.1:8080"', 'PKG_TYPE="tar"',
                          'REALNAME="dict-tree"', '',
                          'inherit g-elpa', '', 'DESCRIPTION="Dictionary data structure"',
                          'HOMEPAGE="http://127.0.0.1:8080"',
                          'SRC_URI="${REPO_URI}${REALNAME}-${PV}.${SUFFIX}"',
                          'LICENSE="GPL-2"', '', 'SLOT="0"',
                          'KEYWORDS="~amd64 ~x86"', 'IUSE=""', '',
                          'DEPEND="app-emacs/trie-0.2.5\napp-emacs/tNFA-0.1.1\napp-emacs/heap-0.3"',
                          'RDEPEND="app-emacs/trie-0.2.5\napp-emacs/tNFA-0.1.1\napp-emacs/heap-0.3"'])


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestElpaEbuildGenerator('test_generate_without_digest'))
    suite.addTest(TestElpaEbuildGenerator('test_generate_with_digest'))
    return suite